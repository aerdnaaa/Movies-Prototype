from flask import Blueprint
from flask import render_template,request,redirect,flash,url_for
from package.user.forms import CreateUserForm,LoginForm
import shelve
from package.user.classes import User


user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    print('test')
    usersDict = {}
    db = shelve.open('storage.db','r')
    usersDict = db['Users']
    db.close()
    if form.validate_on_submit() and request.method=='GET':
        if form.Username.data == 'test' and form.password.data =='password':
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
        userDict={}
        db = shelve.open('storage.db','c')
        try:
            userDict = db['Users']
        except:
            userDict = {}
            print("Error in retrieving Users from storage.db.")

        user = User(createUserForm.firstName.data,createUserForm.lastName.data,
        createUserForm.email.data,createUserForm.password.data,createUserForm.Username.data,
        createUserForm.gender.data,createUserForm.DateofBirth.data)
        userDict[user.get_userID()] = user
        db['Users'] = userDict

        userDict=db['Users']
        user = userDict[user.get_userID()]
        print(f'Account for {user.get_username()} has been created with id number {user.get_userID()}')
        db.close()
        return redirect(url_for('carousel.home'))
    return render_template("User/register.html", title="Register",form=createUserForm)

@user_blueprint.route("/accountpage")
def accountpage():
    uDict = {}
    user=User('r1','r2','r3','r4','r5','r6','r7')
    uDict={
        user.get_userID : user
    }
    userlist =  list(uDict.values())
    db = shelve.open('storage.db','r')
    usersDict = db['Users']
    return render_template("User/accountpage.html", title="Account")

@user_blueprint.route("/admin/admin_accounts")
def admin_accounts():
    return render_template("Admin/users/admins.html")