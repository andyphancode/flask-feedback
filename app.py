from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from app import *
from sqlalchemy.exc import IntegrityError

app = Flask(__name__) 
app.app_context().push() 
app.config['SECRET_KEY'] = 'idksecretkey' 
# debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback-users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    """Render home page."""

    return render_template('home.html')

@app.route("/register", methods=["GET","POST"])
def register():
    """Show register form or register a user if submitted"""

    form=RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username,password,email,first_name,last_name)

        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username is taken.')
            return render_template('register.html', form=form)
        session['user_username'] = new_user.username
        
        return redirect('/')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET","POST"])
def login():
    """Log a user in."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)

        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']
    
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def user_page(username):
    """Page requiring authorization."""

    if "user_username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    else:
        user = User.query.get_or_404(username)
        return render_template("user.html", user=user)
    
@app.route('/logout')
def logout():
    """Logout a user."""

    session.pop('user_username')
    flash("Goodbye!", "info")
    return redirect('/')

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete a user."""

    if username != session['user_username']:
        flash("You are not the correct user!")
        return redirect("/")
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('user_username')

    return redirect("/")

@app.route('/users/<username>/feedback/add', methods=["GET","POST"])
def feedback_form(username):
    """Display and add feedback"""

    form=FeedbackForm()

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data


        if username != session['user_username']:
            flash("You are not the correct user!")
            return redirect("/")
        
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f"/users/{username}")

    return render_template("feedback.html", form=form)

@app.route('/feedback/<feedback_id>/update', methods=["GET","POST"])
def feedback_update(feedback_id):
    """Update feedback"""

    form=FeedbackForm()
    feedback = Feedback.query.get_or_404(feedback_id)

    if form.validate_on_submit():

        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("update.html", form=form, feedback=feedback)

@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)

    if feedback.username != session['user_username']:
        flash("You are not the correct user!")
        return redirect("/")
    
    db.session.delete(feedback)
    db.session.commit()  

    
    return redirect(f"/users/{feedback.username}")