from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, <model classes>
from forms import <formclasses>
from app import *

app = Flask(__name__) 
app.app_context().push() 
app.config['SECRET_KEY'] = 'idksecretkey' 
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///<dbname>' app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

