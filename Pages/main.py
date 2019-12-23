from flask import Flask, render_template, request, Markup, redirect, url_for, Markup
from Forms import CreateMovieTheatreForm, CreatePromotion, CreateContactUsForm
from classes import Promotion
import shelve, os, secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = "73892748739"

@app.route("/")
@app.route("/home")
def home():
    # carousel list will be created from Admin
    return render_template("User/home.html", title="Home", carousel_list=["carousel1.jpeg","carousel2.jpeg","carousel3.jpeg"])


# list of movies
@app.route("/movieslist")
def movieslist():
    return render_template("User/movieslist.html", title="Movies List")


@app.route("/frozenmoviedetails")
def frozenmoviedetails():
    return render_template("User/frozenmoviedetails.html", title="Frozen Movie Detail")

@app.route("/jokermoviedetails")
def jokermoviedetails():
    return render_template("User/jokermoviedetails.html", title="Joker Movie Detail")


@app.route("/bookmovie")
def bookmovie():
    return render_template("User/bookmovie.html", title="Book Movie")


@app.route("/bookmovieseats")
def bookmovieseats():
    return render_template("User/bookmovieseats.html", title="Buying Seats")


@app.route("/rentmovie")
def rentmovie():
    return render_template("User/rentmovie.html", title="Rent Movie", genreList = ["Action","Adventure","Comedy","Horror"], rentMovieList=[[]])

@app.route("/login")
def login():
    form = loginform()
    return render_template("User/login.html", title="Login Page",form=form)


@app.route("/register")
def register():
    createUserForm = CreateUserForm(request.form)
    return render_template("User/register.html", title="Register",form=createUserForm)


@app.route("/accountpage")
def accountpage():
    return render_template("User/accountpage.html", title="Account")


@app.route("/promotions")
def promotion():
    db = shelve.open("shelve.db", "c")
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    promotion_list = []
    promotion_sub_list = []
    index = 0
    main_index = 0
    list_of_promotion_classes = list(Promotion_dict.values())
    for promotion_class in list_of_promotion_classes:
        main_index += 1
        if index <= 5:
            promotion_sub_list.append(promotion_class)
            if index == 5 or main_index == len(list_of_promotion_classes):
                promotion_list.append(promotion_sub_list)
            index += 1        
            print(promotion_sub_list)
        else:
            promotion_sub_list = []
            promotion_sub_list.append(promotion_class)
            index = 1

    # promotion_list needs a list in a list. Outer list for rows, inner list for promotions in 1 row
    return render_template("User/promotion.html", title="Promotions", promotion_list=promotion_list)

@app.route("/promotion/<name_of_promo>")
def promotionDetail(name_of_promo):
    db = shelve.open("shelve.db", "c")
    Promotion_dict = db["promotion"]
    promo = Promotion_dict[name_of_promo]
    return render_template("User/promotionDetail.html", promo=promo, title=name_of_promo.capitalize() + " Promo")

@app.route("/contactUs")
def contactUs():
    form = CreateContactUsForm()
    return render_template("User/contactUs.html", title="Contact Us", form=form)

# admin routes
@app.route("/admin")
@app.route("/admin/home")
def admin_home():
    return render_template("Admin/index.html", title="Dashboard")


# @app.route("/admin/promotion", methods=["GET","POST"])
# def admin_promotion():
#     form = CreatePromotion()
#     db = shelve.open('shelve.db', 'c')
#     try:
#         Promotion_dict = db["promotion"]
#     except:        
#         Promotion_dict = {}
#         db["promotion"] = Promotion_dict
#     if form.validate_on_submit():
#         promotion_title = form.promotion_title.data
#         promotion_image = save_promotion_pic(form.promotion_image.data)
#         promotion_description = form.promotion_description.data
#         promotion_terms_and_conditions = form.promotion_terms_and_condition.data.split("\n")
#         promotion_period = form.promotion_valid_start_date.data + " - " + form.promotion_valid_end_date.data
#         promotion_applicable_to = form.promotion_applicable_to.data
#         promotion_class = Promotion(promotion_title,promotion_image,promotion_description,promotion_terms_and_conditions,promotion_period,promotion_applicable_to)
#         Promotion_dict[promotion_title] = promotion_class
#         db["promotion"] = Promotion_dict
#         db.close()
#         return redirect(url_for("admin_promotion"))
#     elif request.method == "GET":
#         promotion_title = ""        
#         promotion_description = ""
#         promtion_terms_and_conditions = ""
#         form.promotion_valid_start_date.data = ""
#         form.promotion_valid_end_date.data = ""
#         promtion_applicable_to = ""
#     return render_template("Admin/promotion.html", title="Promotion", form=form, Promotion_dict=Promotion_dict)

def save_promotion_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/promotion', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/admin/booking")
def admin_booking():
    return render_template("Admin/booking.html", title="Booking")

@app.route("/admin/rent")
def admin_rent():
    return render_template("Admin/rent.html", title="Renting")

@app.route("/admin/composeMail")
def admin_composeMail():
    return render_template("Admin/compose.html", title="Compose Mail")

@app.route("/admin/readMail")
def admin_readMail():
    return render_template("Admin/read-mail.html", title="Read Mail")

@app.route("/admin/calendar")
def admin_calendar():
    return render_template("Admin/calendar.html", title="Calendar")

@app.route("/admin/mailbox")
def admin_mailbox():
    return render_template("Admin/mailbox.html", title="Mailbox")

@app.route("/admin/movieTheatre", methods=["GET","POST"])
def admin_movieTheatre():
    form = CreateMovieTheatreForm()
    if form.validate_on_submit():
        print("jesus is coming")
    return render_template("Admin/movie-theatre.html", title="Movie Theatre", form=form)

@app.route("/admin/movies")
def admin_movies():
    return render_template("Admin/movies.html", title="Movies")

# 2nd version of CRUD of promotions:

@app.route("/admin/promotion")
def admin_promotion():    
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    db.close()    
    return render_template("Admin/promotion.html", title="Promotion", Promotion_dict=Promotion_dict)

@app.route("/admin/promotion/add_promotion", methods=["POST","GET"])
def add_promotion():
    form = CreatePromotion()
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
        Promotion.id = list(Promotion_dict.values())[-1].get_id()
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    if form.validate_on_submit():        
        promotion_title = form.promotion_title.data
        promotion_image = save_promotion_pic(form.promotion_image.data)
        promotion_description = Markup(form.promotion_description.data)
        promotion_terms_and_conditions = form.promotion_terms_and_condition.data.split("\n")
        promotion_period = form.promotion_valid_start_date.data + " - " + form.promotion_valid_end_date.data
        promotion_applicable_to = form.promotion_applicable_to.data
        promotion_class = Promotion(promotion_title,promotion_image,promotion_description,promotion_terms_and_conditions,promotion_period,promotion_applicable_to)
        promotion_id = promotion_class.get_id()
        Promotion_dict[promotion_id] = promotion_class
        db["promotion"] = Promotion_dict
        db.close()
        return redirect(url_for("admin_promotion"))
    elif request.method == "GET":
        form.promotion_title.data = ""        
        form.promotion_description.data = ""
        form.promotion_terms_and_condition.data = ""
        form.promotion_valid_start_date.data = ""
        form.promotion_valid_end_date.data = ""
        form.promotion_applicable_to.data = ""
    return render_template("Admin/promotion/add_promotion.html", title="Add Promotion", form=form)

@app.route("/admin/promotion/modify_promotion/<promotion_id>", methods=["POST","GET"])
def modify_promotion(promotion_id):
    form = CreatePromotion()
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    if form.validate_on_submit():
        promotion_title = form.promotion_title.data
        promotion_image = save_promotion_pic(form.promotion_image.data)
        promotion_description = form.promotion_description.data
        promotion_terms_and_conditions = form.promotion_terms_and_condition.data.split("\n")
        promotion_period = form.promotion_valid_start_date.data + " - " + form.promotion_valid_end_date.data
        promotion_applicable_to = form.promotion_applicable_to.data
        # editing class, not creating new one as id will newly be generated
        promotion_class = Promotion_dict[promotion_id]
        promotion_class.set_title(promotion_title)
        promotion_class.set_promotion_image(promotion_image)
        promotion_class.set_description(Markup(promotion_description))
        promotion_class.set_valid_period(promotion_period)
        promotion_class.set_applicable_to(promotion_applicable_to)
        Promotion_dict[promotion_id] = promotion_class
        db["promotion"] = Promotion_dict
        db.close()
        return redirect(url_for("admin_promotion"))
    elif request.method == "GET":
        promotion = Promotion_dict[promotion_id]
        form.promotion_title.data = promotion.get_title()
        form.promotion_description.data = promotion.get_description()
        form.promotion_terms_and_condition.data = "\n".join(promotion.get_terms_and_conditions())
        start_date, end_date = promotion.get_valid_period().split(" - ")
        form.promotion_valid_start_date.data = start_date
        form.promotion_valid_end_date.data = end_date
        form.promotion_applicable_to.data = promotion.get_applicable_to()
        image_source = promotion.get_promotion_image()
    return render_template("Admin/promotion/modify_promotion.html", title="Modify Promotion", form=form, image_source=image_source)

@app.route("/admin/promotion/delete", methods=["GET","POST"])
def delete_promotion():    
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    list_of_to_be_deleted_promotions = request.json    
    for promotion_id in list_of_to_be_deleted_promotions:
        del Promotion_dict[int(promotion_id)]
    db["promotion"] = Promotion_dict
    db.close()    
    return redirect(url_for('admin_promotion'))


if __name__ == "__main__":
    app.run(debug=True)
