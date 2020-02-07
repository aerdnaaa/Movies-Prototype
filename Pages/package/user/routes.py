from flask import Blueprint
from flask import render_template,request,redirect,flash,url_for, jsonify
from package.user.forms import CreateUserForm,LoginForm, CreateAdminForm, ModifyAdminForm, ModifyAdminAccount, UpdateContactDetails, UpdatePassword, UpdateProfilePicture
import shelve
from package.user.classes import User, Admin
from package import bcrypt, login_manager
from package.user.utilis import load_user, return_emails, is_correct_password, return_user_id, save_picture
from flask_login import login_user, logout_user, login_required, current_user
from package.utilis import check_admin, check_if_login
import datetime

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/login", methods=['GET','POST'])
def login():
    check_if_login()
    form = LoginForm()        
    db = shelve.open('shelve.db','r')    
    try:
        userDict = db['Users']
    except:
        userDict = {}
        db['Users'] = userDict
    print(db["Users"])             
    db.close()                
    if request.method=='POST':        
        if form.email.data in return_emails(userDict) and is_correct_password(form.email.data, form.password.data, userDict):            
            login_user(load_user(return_user_id(form.email.data, userDict)), remember=form.rememberMe.data, duration=datetime.timedelta(minutes=5))            
            flash('You have been logged in!','success')
            if current_user.get_id()[0] == "U":
                return redirect(url_for('user.accountpage'))
            else:
                return redirect(url_for('other.admin_home'))
        else:
            flash('Invalid username or password. Please check both fields.','danger')        
    return render_template("User 2/signin.html", title="Login Page",form=form)

@login_required
@user_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('carousel.home'))

@user_blueprint.route("/register",methods=['GET','POST'])
def register():
    check_if_login()
    createUserForm = CreateUserForm()
    db = shelve.open('shelve.db','c')
    try:
        userDict = db['Users']
        user_key_list = []
        # for key in userDict:
        #     if key[0] == "U":
        #         user_key_list.append(key)
        # if user_key_list:
        #     User.id = user_key_list[-1].get_id()
        # else:
        #     User.id = "U-1"            
    except:
        userDict = {}
        db['Users'] = userDict   
    if request.method=='POST' and createUserForm.validate():
        flash(f'Account created for {createUserForm.username.data}!','success')        
        user = User(createUserForm.fullName.data,
        createUserForm.email.data,bcrypt.generate_password_hash(createUserForm.password.data).decode('utf-8'),createUserForm.username.data,
        createUserForm.gender.data,createUserForm.dateOfBirth.data)
        userDict[user.get_id()] = user
        db['Users'] = userDict    
        return redirect(url_for('user.login'))        
    db.close()
    return render_template("User 2/signup.html", title="Register",form=createUserForm)

@user_blueprint.route("/accountpage")
@login_required
def accountpage():
    UCDform = UpdateContactDetails()
    UPform = UpdatePassword()
    UPPform = UpdateProfilePicture()
    db = shelve.open('shelve.db', 'w')
    try:
        userDict = db["Users"]
    except:
        userDict = {}
        db["Users"] = userDict
    user_class = userDict[current_user.get_id()]
    if request.method == 'POST' and UCDform.validate():
        flash(f'You have successfully changed your contact details.', 'success')
        user_fullName = UCDform.fullName.data
        user_email = UCDform.email.data
        user_dateOfBirth = UCDform.dateOfBirth.data
        user_username = UCDform.username.data
        user_gender = UCDform.gender.data

        user_class.set_fullname(user_fullName)
        user_class.set_email(user_email)
        user_class.set_DateofBirth(user_dateOfBirth)
        user_class.set_username(user_username)
        user_class.set_gender(user_gender)

        db["Users"] = userDict
        db.close()
        return redirect(url_for('user.accountpage'))
    if request.method =='POST' and UPform.validate():
        flash(f'You have successfully changed your password.','success')
        user_password = UPform.password.data
        user_class.set_password(user_password)
        db['Users'] =userDict
        db.close()
        return redirect(url_for('user.accountpage'))
    if request.method == 'POST' and UPPform.validate():
        pass #need to set directory for uploaded images
        return redirect(url_for('user.accountpage'))
    return render_template("User 2/accountpage.html", UCDform=UCDform, UPform=UPform,UPPform=UPPform, title="My Account Page")

@user_blueprint.route("/admin/admin_accounts")
@login_required
def admin_accounts():
    check_admin()
    db = shelve.open('shelve.db', 'c')
    try:
        Admin_dict = db['Users']
    except:
        Admin_dict = {}
        db['Users'] = Admin_dict
    print(Admin_dict)
    return render_template("Admin/users/admins.html", title="Admin Accounts", Admin_dict=Admin_dict)

@user_blueprint.route("/admin/admin_accounts/add_admin", methods=["GET","POST"])
@login_required
def add_admin():
    check_admin()
    form = CreateAdminForm()
    db = shelve.open('shelve.db', 'c')
    Admin_dict = db['Users']
    admin_list = []
    for key in Admin_dict:
        if key == "A":
            admin_list.append(key)
    try:
        Admin.id = admin_list[-1].get_id()   
    except:
        Admin.id = "A0"
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        administrative_rights = form.administrative_rights.data
        if not administrative_rights:
            administrative_rights = []  # In case no rights is assigned to an admin
        # hashed_password = bcrypt.generate_password_hash("admin").decode('utf-8')
        admin_class = Admin(username, email, administrative_rights, bcrypt.generate_password_hash("Admin").decode('utf-8'))
        Admin_dict[admin_class.get_id()] = admin_class
        db["Users"] = Admin_dict
        db.close()
        return redirect(url_for("user.admin_accounts"))
    elif request.method == "GET":
        form.username.data = "Admin"
        form.email.data = ""
        form.administrative_rights.data = "Super Admin"        
        db.close()
    return render_template("Admin/users/add_admin.html", title="Add Admin", form=form)

@user_blueprint.route("/admin/admin_accounts/modify_admin/<admin_id>", methods=["POST","GET"])
@login_required
def modify_admin(admin_id):
    check_admin()
    form = ModifyAdminForm()
    db = shelve.open('shelve.db', 'c')    
    Admin_dict = db["Users"]    
    admin_class = Admin_dict[admin_id]
    if form.validate_on_submit():
        admin_username = form.username.data
        admin_email = form.email.data
        admin_rights_list = form.administrative_rights.data
        if not admin_rights_list:
            admin_rights_list = []  # In case no rights is assigned to an admin
        admin_class.set_username(admin_username)
        admin_class.set_email(admin_email)
        admin_class.set_administrative_rights(admin_rights_list)
        db["Users"] = Admin_dict
        db.close()
        return redirect(url_for("user.admin_accounts"))
    elif request.method == "GET":
        form.username.data = admin_class.get_username()
        form.email.data = admin_class.get_email()
        form.administrative_rights.data = admin_class.get_administrative_rights()
        db.close()
    return render_template("Admin/users/modify_admin.html", title="Modify Admin Account", form=form)


@user_blueprint.route("/admin/admin_accounts/delete", methods=["POST","GET"])
@login_required
def delete_admin():
    check_admin()
    db = shelve.open('shelve.db', 'c')
    try:
        Admin_dict = db["Users"]
        Deleted_list = db["deleted_Admins"]
    except:
        Admin_dict = {}
        Deleted_list = []
        db["Users"] = Admin_dict
        db["deleted_Admins"] = Deleted_list
    list_of_to_be_deleted_admins = request.json
    for admin_id in list_of_to_be_deleted_admins:
        delete_admin = Admin_dict[admin_id]        
        Deleted_list.append([delete_admin, datetime.date.today()])
        del Admin_dict[admin_id]
    db["Users"] = Admin_dict
    db["deleted_Admins"] = Deleted_list
    db.close()
    return redirect(url_for("user.admin_accounts"))

@user_blueprint.route("/admin/my_account", methods=["POST","GET"])
@login_required
def my_admin_account():
    check_admin()
    form = ModifyAdminAccount()               
    print(form.validate_on_submit())
    if request.method == "POST" and form.username.errors == []:          
        db = shelve.open('shelve.db', 'c')        
        user_dict = db["Users"]        
        user_class = user_dict[current_user.get_id()]
        if form.profile_picture.data != None:
            picture_path = save_picture(form.profile_picture.data, "admin_profile_pictures/")            
            user_class.set_profile_picture(picture_path)
        if form.username.data != current_user.get_username():
            username = form.username.data
            user_class.set_username(username)
        if form.new_password.data != "":
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            user_class.set_password(hashed_password)
        print(user_class)
        user_dict[user_class.get_id()] = user_class
        db["Users"] = user_dict
        db.close()
        flash("Admin Account is updated", 'success')
        return redirect(url_for('user.my_admin_account'))
    elif request.method == "GET":
        form.username.data = current_user.get_username()        
        return render_template("Admin/users/admin_account.html", title="My Admin Account", form=form)