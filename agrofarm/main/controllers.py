from flask import Blueprint, render_template, flash, session, jsonify
from flask import current_app, redirect, request, url_for
from agrofarm.data.models import Login, Answers, Questions, Users, q_votes, a_votes, db
from sqlalchemy import exc, text
import hashlib

# specifies the template folder for the main blueprint
main = Blueprint('main', __name__, template_folder='templates', static_folder='/static')


@main.route('/')
def index():
    view_all = db.session.execute("SELECT q.*, (SELECT count(a.q_id) as answer_count from answers a where a.q_id = q.id) from questions q order by(q.asked) desc;")
    result = []
    for row in view_all:
        result.append(dict(zip(row.keys(),row)))
    return render_template('home.html', result=result)

@main.route('account')
def account():
    if 'u_name' in session:
        return redirect(url_for('main.profile'))
    return render_template('login_signup.html')

@main.route('about')
def about():
    return render_template('about.html')

@main.route('signIn', methods=['POST'])
def signIn():
    if request.method != 'POST':
        return render_template('405.html')
    if 'u_name' in session:
        return redirect(url_for('main.profile'))

    request_data = request.get_json(force=True)
    email = request_data['email']
    password = request_data['password']
    hash_object = hashlib.md5(password.encode())
    hashed_password = hash_object.hexdigest()
    result = Users.query.filter_by(email=email).first()
    if result is None:
        response = {"status": 1, "status_msg": "User Not Found"}
        return jsonify(response), 200
    else:
        if hashed_password == result.password:
            session['u_id'] = result.id
            session['u_name'] = result.name
            session['u_email'] = result.email
            response = {"status": 0, "status_msg": "Success!"}
            return jsonify(response), 200
        else:
            response = {"status": 1, "status_msg": "Mismatch!"}
            return jsonify(response), 200

@main.route('signOut')
def signOut():
    if 'u_name' in session:
        session.pop('u_name', None)
        session.pop('u_id', None)
        return redirect(url_for('main.index'))

    return redirect(url_for('main.account'))

@main.route('signUp', methods=['POST'])
def add_new_user():
    if request.method != 'POST':
        return render_template('405.html')
    if 'u_name' in session:
        return redirect(url_for('main.profile'))

    request_data = request.get_json(force=True)
    name = request_data['name']
    email = request_data['email']
    password = request_data['password']
    hash_object = hashlib.md5(password.encode())
    hashed_password = hash_object.hexdigest()
    current_app.logger.info('Adding a new User %s: %s.', (name, email, hashed_password))
    add_user = Users(name, email, hashed_password)

    try:
        db.session.add(add_user)
        db.session.commit()
        result = Users.query.filter_by(email=email).first()
        session['u_id'] = result.id
        session['u_name'] = result.name
        response = {"status": 0, "status_msg": "Success!"}
        return jsonify(response), 201
    except exc.SQLAlchemyError as e:
        flash('Cannot Add User.')
        current_app.logger.error(e)
        response = {"status": 1, "status_msg": "User Not Added!"}
        return jsonify(response), 500

@main.route('profile')
def profile():
    if 'u_name' in session:
        u_id = session['u_id']
        question = Questions.query.filter_by(u_id=u_id).all()
        answer = Answers.query.filter_by(u_id=u_id).all()
        return render_template('profile.html', question=question, answer=answer)
    else:
        return redirect(url_for('main.account'))

@main.route('questions')
def ask_question():
        return render_template('questions.html')

@main.route('submit_question', methods=["POST"])
def submit_question():
    if request.method != 'POST':
        return render_template('405.html')
    if 'u_name' not in session:
        return redirect(url_for('main.account'))

    request_data = request.get_json(force=True)
    title = request_data['title']
    text = request_data['text']
    u_id = session['u_id']
    current_app.logger.info('Adding a new Question %s: %s.', (u_id, title, text))
    add_question = Questions(title, text, u_id)

    try:
        db.session.add(add_question)
        db.session.commit()
        response = {"status": 0, "status_msg": "Success!"}
        return jsonify(response), 201
    except exc.SQLAlchemyError as e:
        flash('Cannot Add Question.')
        current_app.logger.error(e)
        response = {"status": 1, "status_msg": "Question Not Added!"}
        return jsonify(response), 500

@main.route('view_question/<int:q_id>')
def view_question(q_id):
    result_ques = db.session.execute("SELECT Q.*, (SELECT U.NAME FROM USERS U WHERE U.ID = Q.U_ID LIMIT 1) FROM QUESTIONS Q WHERE Q.ID = :val LIMIT 1", {'val':q_id})
    question = []
    for row in result_ques:
        question = dict(zip(row.keys(), row))

    answer_accepted = Answers.query.filter_by(q_id=q_id, accepted="YES").first()
    result_ans = db.session.execute("SELECT A.*, (SELECT U.NAME FROM USERS U WHERE U.ID=A.U_ID LIMIT 1) FROM ANSWERS A WHERE A.q_id = :val AND A.accepted='NO' ORDER BY(A.UPVOTES, A.ANSWERED) DESC", {'val':q_id})
    all_answers=[]
    for row in result_ans:
        all_answers.append(dict(zip(row.keys(), row)))

    return render_template('view_question.html', question=question, answer_accepted=answer_accepted, all_answers=all_answers)


@main.route('submit_answer/<int:q_id>', methods=["POST"])
def submit_answer(q_id):
    if request.method != 'POST':
        return render_template('405.html')
    if 'u_name' not in session:
        response = {"status": 1, "status_msg": "You need to login first to answer!"}
        return jsonify(response), 200

    request_data = request.get_json(force=True)
    ans = request_data['ans']
    u_id = session['u_id']
    current_app.logger.info('Adding a new Answer to question (%s: %s: %s).', (u_id, q_id, ans))
    add_answer = Answers(ans, q_id, u_id)

    try:
        db.session.add(add_answer)
        db.session.commit()
        response = {"status": 0, "status_msg": "Success!"}
        return jsonify(response), 201
    except exc.SQLAlchemyError as e:
        flash('Cannot Add Question.')
        current_app.logger.error(e)
        response = {"status": 1, "status_msg": "Question Not Added!"}
        return jsonify(response), 500

@main.route('help')
def help():
    return render_template('help.html')

@main.route('ans_guide')
def ans_guide():
    return render_template('ans_guide.html')

@main.route('ques_guide')
def ques_guide():
    return render_template('ques_guide.html')

@main.route('vote_guide')
def vote_guide():
    return render_template('vote_guide.html')

@main.route('vote', methods=["POST"])
def vote():
    if 'u_id' not in session:
        response = {"status": 1, "status_msg": "You need to login first to VOTE!"}
        return jsonify(response), 200

    request_data = request.get_json(force=True)
    vote = request_data['vote']
    entity_id = request_data['id']
    entity_type = request_data['type']
    u_id = session['u_id']
    if entity_type == "QUESTION":
        result = q_votes.query.filter_by(u_id=u_id,q_id=entity_id).first()
        if result is None:
            current_app.logger.info('Voting Entity (Vote_Type:%s, Entity_Type: %s, Entity_Id: %s, User_Id: %s).', (vote, entity_type, entity_id, u_id))
            add_vote = q_votes(u_id, entity_id, vote)
            try:
                db.session.add(add_vote)
                update_questions = Questions.query.filter_by(id=entity_id).first()
                if vote == "UP":
                    update_questions.upvotes += 1
                else:
                    update_questions.downvotes +=1
                db.session.commit()
                response = {"status": 0, "status_msg": "Success!"}
                return jsonify(response), 201
            except exc.SQLAlchemyError as e:
                flash('Cannot Add Vote.')
                current_app.logger.error(e)
                response = {"status": 1, "status_msg": "Error:Vote Not Added!"}
                return jsonify(response), 500
        else:
            current_app.logger.info('Removing Vote Entity (Vote_Type:%s, Entity_Type: %s, Entity_Id: %s, User_Id: %s).', (vote, entity_type, entity_id, u_id))
            update_questions = Questions.query.filter_by(id=entity_id).first()
            if result.vote != vote:
                try:
                    db.session.delete(result)
                    if vote == "DOWN":
                        update_questions.upvotes -= 1
                    else:
                        update_questions.downvotes -= 1

                    db.session.commit()
                    response = {"status": 0, "status_msg": "Success!"}
                    return jsonify(response), 201
                except exc.SQLAlchemyError as e:
                    flash('Cannot Add Vote.')
                    current_app.logger.error(e)
                    response = {"status": 1, "status_msg": "Error:Vote Not Deleted!"}
                    return jsonify(response), 500

            else:
                try:
                    db.session.delete(result)
                    if vote == "UP":
                        update_questions.upvotes -= 1
                    else:
                        update_questions.downvotes -= 1
                    db.session.commit()
                    response = {"status": 0, "status_msg": "Success!"}
                    return jsonify(response), 201
                except exc.SQLAlchemyError as e:
                    flash('Cannot Add Vote.')
                    current_app.logger.error(e)
                    response = {"status": 1, "status_msg": "Error:Vote Not Deleted!"}
                    return jsonify(response), 500

    else:
        result = a_votes.query.filter_by(u_id=u_id,a_id=entity_id).first()

        if result is None:
            current_app.logger.info('Voting Entity (Vote_Type:%s, Entity_Type: %s, Entity_Id: %s, User_Id: %s).', (vote, entity_type, entity_id, u_id))
            add_vote = a_votes(u_id, entity_id, vote)

            try:
                db.session.add(add_vote)
                update_answers = Answers.query.filter_by(id=entity_id).first()
                if vote == "UP":
                    update_answers.upvotes += 1
                else:
                    update_answers.downvotes +=1
                db.session.commit()
                response = {"status": 0, "status_msg": "Success!"}
                return jsonify(response), 201
            except exc.SQLAlchemyError as e:
                flash('Cannot Add Vote.')
                current_app.logger.error(e)
                response = {"status": 1, "status_msg": "Error:Vote Not Added!"}
                return jsonify(response), 500
        else:
            current_app.logger.info('Removing Vote Entity (Vote_Type:%s, Entity_Type: %s, Entity_Id: %s, User_Id: %s).', (vote, entity_type, entity_id, u_id))
            update_answers = Answers.query.filter_by(id=entity_id).first()
            if result.vote != vote:
                try:
                    db.session.delete(result)
                    if vote == "DOWN":
                        update_answers.upvotes -= 1
                    else:
                        update_answers.downvotes -= 1

                    db.session.commit()
                    response = {"status": 0, "status_msg": "Success!"}
                    return jsonify(response), 201
                except exc.SQLAlchemyError as e:
                    flash('Cannot Add Vote.')
                    current_app.logger.error(e)
                    response = {"status": 1, "status_msg": "Error:Vote Not Deleted!"}
                    return jsonify(response), 500

            else:
                try:
                    db.session.delete(result)
                    if vote == "UP":
                        update_answers.upvotes -= 1
                    else:
                        update_answers.downvotes -= 1
                    db.session.commit()
                    response = {"status": 0, "status_msg": "Success!"}
                    return jsonify(response), 201
                except exc.SQLAlchemyError as e:
                    flash('Cannot Add Vote.')
                    current_app.logger.error(e)
                    response = {"status": 1, "status_msg": "Error:Vote Not Deleted!"}
                    return jsonify(response), 500
