from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, connect_db, Feedback
from forms import UserRegisterForm, UserLoginForm, EditFeedbackForm, AddFeedbackForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chicken123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """ Redirect to /register. """
    return redirect('/register')

# Routes for users. 

@app.route('/register', methods=["GET", "POST"])
def register():
    """ Show the form to register new users. """ 
    # Get the form to add new user.
    form = UserRegisterForm()

    # If request is a post and form submitted with valid csrf token. 
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        email = form.email.data 
        first_name = form.first_name.data
        last_name = form.last_name.data 

        user = User.register(name, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.username 

        # Upon successful login, redirect to secret page. 
        return redirect(f'/users/{user.username}')
        
    return render_template('register_form.html', form=form)

@app.route('/users/<username>')
def secret(username):
    """ Secret area!. """
    if 'user_id' not in session:
        flash('You must be logged in to view!')
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        return render_template('secret.html', user=user)

@app.route('/users/<username>/delete')
def delete_user(username):
    """ Remove the user from database and delete all their feedback. """
    if 'user_id' in session:
        db.session.delete(User.query.get_or_404(username))
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    """ User Login. """
    
    form = UserLoginForm()

    # If request is a post and form submitted with valid csrf token. 
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, password)

        if user:
            session['user_id'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():
    """ Logout the user. """
    session.pop('user_id')
    return redirect('/login')

# Routes for feedbacks and users.

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def show_add_feedback_form(username):
    """ Display a form to add feedback for the, if and only if, user. """
    
    if 'user_id' in session:
        form = AddFeedbackForm()
        user = User.query.get_or_404(username)
    
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data 

            new_feedback = Feedback(title=title, content=content, username=user.username)
            db.session.add(new_feedback)
            db.session.commit()

            # Upon successful feedback add, redirect back to user details. 
            return redirect(f'/users/{username}')
        else:
            return render_template('feedback_add_form.html', form=form, user=user)
    else:
        return redirect('/')

# Routes for feedbacks. 

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def show_edit_feedback_form(feedback_id):
    """ Display a form to edit feedback. """

    feedback = Feedback.query.get_or_404(feedback_id)
    
    if 'user_id' in session and session['user_id'] == feedback.username:
        form = EditFeedbackForm(obj=feedback)
        
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data 
            db.session.commit()

            # Upon successful feedback add, redirect back to user details. 
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template('feedback_edit_form.html', form=form, feedback=feedback)
    else:
        return redirect('/')


@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """ Delete feedback. """
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'user_id' in session and session['user_id'] == feedback.username:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')    
    else:
        return redirect('/')