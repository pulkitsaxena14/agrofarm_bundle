from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(20))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Id: %r, User: %r, Email: %r>' % (self.id, self.name, self.email)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Id: %r, Name: %r, Email: %r, Password: %r>' % (self.id, self.name, self.email, self.password)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    details = db.Column(db.String, nullable=False)
    asked = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)

    def __init__(self, title, details, u_id, upvotes=None, downvotes=None):
        self.title = title
        self.details = details
        self.u_id = u_id
        self.upvotes = upvotes
        self.downvotes = downvotes

    def __repr__(self):
        return '<Id: %r, Title: %r, Details: %r, Asked: %r, User_ID: %r, Upvotes: %r, Downvotes: %r' % (self.id, self.title, self.details, self.asked, self.u_id, self.upvotes, self.downvotes)


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ans = db.Column(db.String, nullable=False)
    answered = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    q_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    accepted = db.Column(db.Enum('YES', 'NO', name='ACCEPT_ANS'), default="NO")

    def __init__(self, ans, q_id, u_id, upvotes=None, downvotes=None, accepted=None):
        self.ans = ans
        self.q_id = q_id
        self.u_id = u_id
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.accepted = accepted

    def __repr__(self):
        return '<Id: %r, Answer: %r, Answered: %r, Question_Id: %r, User_ID: %r, Upvotes: %r, Downvotes: %r, Accepted: %r' % (self.id, self.ans, self.answered, self.q_id, self.u_id, self.upvotes, self.downvotes, self.accepted)


class q_votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    q_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    vote = db.Column(db.Enum('UP', 'DOWN', name='VOTE_TYPE'), default="NO")
    __table_args__ = (db.UniqueConstraint('u_id', 'q_id'),)

    def __init__(self, u_id, q_id, vote):
        self.u_id = u_id
        self.q_id = q_id
        self.vote = vote

    def __repr__(self):
        return '<Id: %r, User_ID: %r, Question_Id: %r, Vote: %r' % (self.id, self.u_id, self.q_id, self.vote)

class a_votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    a_id = db.Column(db.Integer, db.ForeignKey("answers.id"), nullable=False)
    vote = db.Column(db.Enum('UP', 'DOWN', name='VOTE_TYPE'), default="NO")
    __table_args__ = (db.UniqueConstraint('u_id', 'a_id'),)

    def __init__(self, u_id, a_id, vote):
        self.u_id = u_id
        self.a_id = a_id
        self.vote = vote

    def __repr__(self):
        return '<Id: %r, User_ID: %r, Answer_Id: %r, Vote: %r' % (self.id, self.u_id, self.a_id, self.vote)
