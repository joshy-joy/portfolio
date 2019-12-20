from app import db
from datetime import datetime
from flask_login import UserMixin

#model to store project details
class Project(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    link = db.Column(db.String(200))
    description = db.Column(db.Text)
    image = db.Column(db.String(500))

    def __init__(self, title, link, description, image):

        self.title = title
        self.link = link
        self.description = description
        self.image = image




#model to store Blog posts
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    content =  db.Column(db.Text, nullable = False)
    cover_img = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow, onupdate = datetime.utcnow)
    category = db.Column(db.String(20), nullable = False)
    tags = db.Column(db.String(20), nullable = False)
    edited = db.Column(db.Boolean, nullable = False)


    def __init__(self, tittle, category, content, cover_img, tags, edited):

        self.title = tittle
        self.content = content
        self.cover_img = cover_img
        self.category = category
        self.tags = tags
        self.edited = edited



#model for admin
class User(UserMixin ,db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(200), nullable = False)

    def __init__(self, name, password):

        self.name = name
        self.password = password




#subscribe model
class Subscribe(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(200), nullable = False)

    def __init__(self, email):

        self.email = email



#Contact Model
class Contact(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(200), nullable = False)
    lname = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    phone = db.Column(db.String(200), nullable = True)
    msg = db.Column(db.String(500), nullable = False)
    date = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)

    def __init__(self, fname, lname, email, phone, msg):

        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone = phone
        self.msg = msg



#Hire Model
class Hire(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(200), nullable = False)
    lname = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    company = db.Column(db.String(200), nullable = True)
    buz_area = db.Column(db.String(200), nullable = False)
    phone = db.Column(db.String(200), nullable = True)
    country = db.Column(db.String(200), nullable = False)
    projecttype = db.Column(db.String(200), nullable = False)
    paytype = db.Column(db.String(200), nullable = False)
    budget = db.Column(db.String(200), nullable = False)
    duration = db.Column(db.String(200), nullable = False)
    date = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)

    def __init__(self, fname, lname, email, company, buz_area, phone, country, projecttype, paytype, budget, duration):

        self.fname = fname
        self.lname = lname
        self.email = email
        self.company = company
        self.buz_area = buz_area
        self.phone = phone
        self.country = country
        self.projecttype = projecttype
        self.paytype = paytype
        self.budget = budget
        self.duration = duration

#notification model
class Logs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    event_id = db.Column(db.Integer, nullable = False)
    event = db.Column(db.String(200), nullable = False)
    msg = db.Column(db.String(200), nullable = False)
    seen = db.Column(db.Boolean, nullable = False)
    date = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)


    def __init__(self, event_id, event, msg, seen):
        self.event_id = event_id
        self.event = event
        self.msg = msg
        self.seen = seen




    
