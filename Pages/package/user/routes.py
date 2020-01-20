from flask import Blueprint
from flask import render_template,request,redirect,flash,url_for
from package.user.forms import CreateUserForm,LoginForm, CreateAdminForm, ModifyAdminForm
import shelve
from package.user.classes import User, Admin
from package import bcrypt

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
    db = shelve.open('storage.db', 'c')
    try:
        Admin_dict = db['Admins']
    except:
        Admin_dict = {}
        db['Admins'] = Admin_dict
    return render_template("Admin/users/admins.html", title="Admin Accounts", Admin_dict=Admin_dict)

@user_blueprint.route("/admin/admin_accounts/add_admin", methods=["GET","POST"])
def add_admin():
    form = CreateAdminForm()
    db = shelve.open('storage.db', 'c')
    try:
        Admin_dict = db['Admins']
        Admin.id = list(Admin_dict.values())[-1].id
    except:
        Admin_dict = {}
        db['Admins'] = Admin_dict
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        administrative_rights = form.administrative_rights.data
        hashed_password = bcrypt.generate_password_hash("admin").decode('utf-8')
        admin_class = Admin(username, email, administrative_rights, hashed_password)
        Admin_dict[admin_class.id] = admin_class
        db["Admins"] = Admin_dict
        db.close()
        return redirect(url_for("user.admin_accounts"))
    elif request.method == "GET":
        form.username.data = "Admin"
        form.email.data = ""
        form.administrative_rights.data = "Super Admin"        
        db.close()
    return render_template("Admin/users/add_admin.html", title="Add Admin", form=form)
