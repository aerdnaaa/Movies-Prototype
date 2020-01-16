from flask import Blueprint
from flask import render_template,request,redirect,flash,url_for
from package.user.forms import CreateUserForm,LoginForm
import shelve
from package.user.classes import User


user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    #not working atm
    if form.validate_on_submit():
        if form.Username.data == 'test'  and form.password.data == 'test':
            flash('You have been logged in!','success')
            return redirect(url_for('carousel.home'))
        else:
            flash('Invalid username or password. Please check both fields.','danger')
    return render_template("User/login.html", title="Login Page",form=form)


@user_blueprint.route("/register",methods=['GET','POST'])
def register():
    createUserForm = CreateUserForm(request.form)
    if request.method=='POST' and createUserForm.validate():
        flash(f'Account created for {createUserForm.Username.data}!','success')
        usersDict={}
        db = shelve.open('storage.db','c')
        try:
            userDict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")
        user = User(createUserForm.firstName.data,createUserForm.lastName.data,
        createUserForm.email.data,createUserForm.password.data,createUserForm.Username.data,
        createUserForm.gender.data,createUserForm.DateofBirth.data)
        usersDict[user.get_userID()] = user
        db['Users'] = usersDict
        # userDict=db['Users']
        # user = usersDict[user.get_userID()]
        # print(f'Account for {user.get_username()} has been created with id number {user.get_userID()}')
        db.close()
        return redirect(url_for('carousel.home'))
    return render_template("User/register.html", title="Register",form=createUserForm)

@user_blueprint.route("/accountpage")
def accountpage():
    return render_template("User/accountpage.html", title="Account")
