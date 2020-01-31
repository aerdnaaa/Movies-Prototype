from flask import Blueprint
from flask import render_template,request,redirect,flash,url_for
from package.user.forms import CreateUserForm,LoginForm, CreateAdminForm, ModifyAdminForm
import shelve
from package.user.classes import User, Admin
from package import bcrypt, login_manager
from package.user.utilis import load_user, return_emails, is_correct_password, return_user_id
from flask_login import login_user, logout_user, login_required
import datetime

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()        
    db = shelve.open('shelve.db','c')
    try:
        userDict = db['Users']
    except:
        userDict = {}
        db['Users'] = userDict
    db.close()        
    print(userDict)
    if request.method=='POST':
        if form.email.data in return_emails(userDict) and is_correct_password(form.email.data, form.password.data, userDict):
            login_user(load_user(return_user_id(form.email.data, userDict)))
            flash('You have been logged in!','success')
            return redirect(url_for('carousel.home'))
        else:
            flash('Invalid username or password. Please check both fields.','danger')
    return render_template("User 2/signin.html", title="Login Page",form=form)

@user_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('carousel.home'))

@user_blueprint.route("/register",methods=['GET','POST'])
def register():
    createUserForm = CreateUserForm(request.form)
    db = shelve.open('shelve.db','c')
    try:
        userDict = db['Users']
        User.id = list(userDict.values())[-1].get_id()            
    except:
        userDict = {}
        db['Users'] = userDict   
    if request.method=='POST' and createUserForm.validate():
        flash(f'Account created for {createUserForm.username.data}!','success')        
        user = User(createUserForm.fullName.data,
        createUserForm.email.data,createUserForm.password.data,createUserForm.username.data,
        createUserForm.gender.data,createUserForm.dateOfBirth.data)
        userDict[user.get_userID()] = user
        db['Users'] = userDict    
        db.close()
        return redirect(url_for('user.login'))    
    return render_template("User 2/signup.html", title="Register",form=createUserForm)

@user_blueprint.route("/accountpage")
@login_required
def accountpage():
    # uDict = {}
    # user=User('r1','r2','r3','r4','r5','r6','r7')
    # uDict={
    #     user.get_userID : user
    # }
    # userlist =  list(uDict.values())
    # db = shelve.open('shelve.db','r')
    # usersDict = db['Users']
    # return render_template("User/accountpage.html", title="Account")
    return "Hi there!"

@user_blueprint.route("/admin/admin_accounts")
def admin_accounts():
    db = shelve.open('shelve.db', 'c')
    try:
        Admin_dict = db['Admins']
    except:
        Admin_dict = {}
        db['Admins'] = Admin_dict
    for key in Admin_dict:
        print(key)
    return render_template("Admin/users/admins.html", title="Admin Accounts", Admin_dict=Admin_dict)

@user_blueprint.route("/admin/admin_accounts/add_admin", methods=["GET","POST"])
def add_admin():
    form = CreateAdminForm()
    db = shelve.open('shelve.db', 'c')
    try:
        Admin_dict = db['Admins']
        Admin.id = list(Admin_dict.values())[-1].get_adminID()
    except:
        Admin_dict = {}
        db['Admins'] = Admin_dict    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        administrative_rights = form.administrative_rights.data
        hashed_password = bcrypt.generate_password_hash("admin").decode('utf-8')
        admin_class = Admin(username, email, administrative_rights, hashed_password)
        Admin_dict[admin_class.get_adminID()] = admin_class
        db["Admins"] = Admin_dict
        db.close()
        return redirect(url_for("user.admin_accounts"))
    elif request.method == "GET":
        form.username.data = "Admin"
        form.email.data = ""
        form.administrative_rights.data = "Super Admin"        
        db.close()
    return render_template("Admin/users/add_admin.html", title="Add Admin", form=form)

@user_blueprint.route("/admin/admin_accounts/modify_admin/<admin_id>", methods=["POST","GET"])
def modify_admin(admin_id):
    form = ModifyAdminForm()
    db = shelve.open('shelve.db', 'c')
    try:
        Admin_dict = db["Admins"]
    except:        
        Admin_dict = {}
        db["Admins"] = Admin_dict
    admin_class = Admin_dict[admin_id]
    administrative_rights_dict = {"1":"Super Admin", "2":"Manage admins", "3":"Carousel"}
    if form.validate_on_submit():
        admin_username = form.username.data
        admin_email = form.email.data
        admin_rights_list = form.administrative_rights.data
        admin_rights_data = []
        for rights in admin_rights_list:
            admin_rights_data.append(administrative_rights_dict[rights])
        admin_class.set_username(admin_username)
        admin_class.set_email(admin_email)
        admin_class.set_administrative_rights(admin_rights_data)
        db["Admins"] = Admin_dict
        return redirect(url_for("user.admin_accounts"))
    elif request.method == "GET":
        pass
    return render_template("Admin/promotion/modify_promotion.html", title="Modify Promotion", form=form, image_source=image_source)


@user_blueprint.route("/admin/admin_accounts/delete", methods=["POST","GET"])
def delete_admin():
    db = shelve.open('shelve.db', 'c')
    try:
        Admin_dict = db["Admins"]
        Deleted_list = db["deleted_Admins"]
    except:
        Admin_dict = {}
        Deleted_list = []
        db["Admins"] = Admin_dict
        db["deleted_Admins"] = Deleted_list
    list_of_to_be_deleted_admins = request.json
    for admin_id in list_of_to_be_deleted_admins:
        delete_admin = Admin_dict[admin_id]        
        Deleted_list.append([delete_admin, datetime.date.today()])
        del Admin_dict[admin_id]
    db["Admins"] = Admin_dict
    db["deleted_Admins"] = Deleted_list
    db.close()
    return redirect(url_for("user.admin_accounts"))
