from flask import Flask, render_template, request, Markup, redirect, url_for, Markup
from Forms import CreateMovieTheatre, ModifyMovieTheatre, CreatePromotion, ModifyPromotion, CreateContactUsForm, CreateCarousel, ModifyCarousel, CreateMovieForm, ModifyMovieForm, CreateRental, ModifyRental
from classes import Promotion, Carousel, Theatre, Movie, Rental
import shelve, os, secrets, datetime
from wtforms import SelectField

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
    # form = loginform()
    return render_template("User/login.html", title="Login Page",form=form)


@app.route("/register")
def register():
    # createUserForm = CreateUserForm(request.form)
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

@app.route("/promotion/<id_of_promo>")
def promotionDetail(id_of_promo):
    db = shelve.open("shelve.db", "c")
    Promotion_dict = db["promotion"]
    promo = Promotion_dict[int(id_of_promo)]
    return render_template("User/promotionDetail.html", promo=promo, title=promo.get_title().capitalize() + " Promo")

@app.route("/contactUs")
def contactUs():
    form = CreateContactUsForm()
    return render_template("User/contactUs.html", title="Contact Us", form=form)

# admin routes
@app.route("/admin")
@app.route("/admin/home")
def admin_home():
    return render_template("Admin/index.html", title="Dashboard")

@app.route("/admin/booking")
def admin_booking():
    return render_template("Admin/booking.html", title="Booking")

#* Rent Movie 
@app.route("/admin/rental")
def admin_rental():
    db = shelve.open('shelve.db', 'c')
    try:
        Rental_dict = db["rental"]
    except:        
        Rental_dict = {}
        db["rental"] = Rental_dict
    db.close()
    return render_template("Admin/rental/rental.html", title="Rental", Rental_dict=Rental_dict)

@app.route("/admin/rental/add_rental", methods=["GET","POST"])
def add_rental():
    form = CreateRental()
    db = shelve.open('shelve.db', 'c')
    try:
        Rental_dict = db["rental"]
        Movies_dict = db["movies"]
        Rental.id = list(Rental_dict.values())[-1].get_id()
    except:        
        Rental_dict = {}
        db["rental"] = Rental_dict        
    movie_available = [("","")]    
    for key in Movies_dict:
        movie_class = Movies_dict[key]        
        movie_available.append((movie_class.get_id(), movie_class.get_movie_name()))        
    form.movie_title.choices = movie_available
    if request.method == "POST":        
        rent_period = form.rent_start_date.data + " - " + form.rent_end_date.data
        rent_price = int(form.rent_price.data)
        movie_class = Movies_dict[int(form.movie_title.data)]
        rental_class = Rental(movie_class, rent_period, rent_price)
        rental_id = rental_class.get_id()
        Rental_dict[rental_id] = rental_class
        db["rental"] = Rental_dict
        db.close()        
        return redirect(url_for("admin_rental"))
    elif request.method == "GET":
        form.movie_title.data = ""
        form.rent_start_date.data = ""
        form.rent_end_date.data = ""
        form.rent_price.data = 0
    return render_template("Admin/rental/add_rental.html", title="Add Rental", form=form)    
    
@app.route("/admin/rental/modify_rental/<rental_id>", methods=["GET","POST"])
def modify_rental(rental_id):
    rental_id = int(rental_id)
    form = ModifyRental()
    db = shelve.open('shelve.db', 'c')
    try:
        Rental_dict = db["rental"]        
        Movies_dict = db["movies"]
        Rental.id = list(Rental_dict.values())[-1].get_id()
    except:        
        Rental_dict = {}
        db["rental"] = Rental_dict        
    movie_available = [("","")]    
    for key in Movies_dict:
        movie_class = Movies_dict[key]        
        movie_available.append((movie_class.get_id(), movie_class.get_movie_name()))        
    form.movie_title.choices = movie_available
    if request.method == "POST":
        rent_period = form.rent_start_date.data + " - " + form.rent_end_date.data
        rent_price = int(form.rent_price.data)
        movie_class = Movies_dict[int(form.movie_title.data)]
        rental_class = Rental_dict[rental_id]
        rental_class.set_all_attributes(movie_class, rent_period, rent_price)
        Rental_dict[rental_id] = rental_class
        db["rental"] = Rental_dict
        db.close()
        return redirect(url_for("admin_rental"))
    elif request.method == "GET":
        rental_class = Rental_dict[rental_id]
        form.movie_title.data = str(rental_class.get_movie_class().get_id())        
        form.rent_start_date.data, form.rent_end_date.data = rental_class.get_rent_period().split(" - ")
        form.rent_price.data = rental_class.get_price()
    return render_template("Admin/rental/modify_rental.html", title="Modify Rental", form=form)    

@app.route("/admin/rental/delete", methods=["GET","POST"])
def delete_rental():
    db = shelve.open('shelve.db', 'c')
    try:
        Rental_dict = db["rental"]
        Deleted_list = db["deleted_rental"]
        Movies_dict = db["movies"]        
    except:        
        Rental_dict = {}
        Deleted_list = []
        db["rental"] = Rental_dict
        db["deleted_rental"] = Deleted_list
    list_of_to_be_deleted_rentals = request.json
    for rental_id in list_of_to_be_deleted_rentals:
        rental_class = Rental_dict[int(rental_id)]
        Deleted_list.append([rental_class, datetime.date.today()])
        del Rental_dict[int(rental_id)]
    db["rental"] = Rental_dict
    db["deleted_rental"] = Deleted_list
    db.close()
    return redirect(url_for("admin_rental"))

@app.route("/admin/rental/rental_users")
def rental_users():
    pass


#* Movie Theatre
@app.route("/admin/movie_theatre", methods=["GET","POST"])
def admin_movie_theatre():
    db = shelve.open('shelve.db', 'c')
    try:
        Movie_theatre_dict = db["movie_theatre"]
    except:        
        Movie_theatre_dict = {}
        db["movie_theatre"] = Movie_theatre_dict
    db.close()    
    return render_template("Admin/movie_theatre/movie_theatre.html", title="Movie Theatre", Movie_theatre_dict=Movie_theatre_dict)

@app.route("/admin/movie_theatre/add_movie_theatre", methods=["GET","POST"])
def add_movie_theatre():
    form = CreateMovieTheatre()
    db = shelve.open('shelve.db', 'c')    
    try:
        Movie_theatre_dict = db["movie_theatre"]
    except:        
        Movie_theatre_dict = {}
        db["movie_theatre"] = Movie_theatre_dict      
    if form.validate_on_submit():
        theatre_name = form.theatre_name.data
        theatre_image = save_picture(form.theatre_image.data, "theatre")        
        theatre_halls = int(form.theatre_halls.data)
        movie_theatre_class = Theatre(theatre_name,theatre_image,theatre_halls)
        theatre_id = movie_theatre_class.get_id()
        Movie_theatre_dict[theatre_id] = movie_theatre_class
        db["movie_theatre"] = Movie_theatre_dict
        db.close()
        return redirect(url_for('admin_movie_theatre'))
    elif request.method == "GET":
        form.theatre_name.data = ""
        form.theatre_halls.data = 1
        db.close()
    return render_template("Admin/movie_theatre/add_movie_theatre.html", title="Add Movie Theatre", form=form)

@app.route("/admin/movie_theatre/modify_movie_theatre/<movie_theatre_id>", methods=["GET","POST"])
def modify_movie_theatre(movie_theatre_id):
    movie_theatre_id = int(movie_theatre_id)
    form = ModifyMovieTheatre()
    db = shelve.open('shelve.db', 'c')    
    try:
        Movie_theatre_dict = db["movie_theatre"]
    except:        
        Movie_theatre_dict = {}
        db["movie_theatre"] = Movie_theatre_dict 
    if form.validate_on_submit():  
        theatre_name = form.theatre_name.data
        theatre_image = save_picture(form.theatre_image.data, "theatre")        
        theatre_halls = int(form.theatre_halls.data)
        movie_theatre_class = Movie_theatre_dict[movie_theatre_id]
        movie_theatre_class.set_all_attributes(theatre_name, theatre_image, theatre_halls)
        Movie_theatre_dict[movie_theatre_id] = movie_theatre_class
        db["movie_theatre"] = Movie_theatre_dict
        db.close()
        return redirect(url_for('admin_movie_theatre'))
    elif request.method == "GET":
        movie_theatre = Movie_theatre_dict[movie_theatre_id]
        form.theatre_name.data = movie_theatre.get_theatre_name()
        form.theatre_halls.data = movie_theatre.get_number_of_halls()
        image_source = movie_theatre.get_theatre_image()
    return render_template("Admin/movie_theatre/modify_movie_theatre.html", title="Modify Movie Theatre", form=form, image_source=image_source)

@app.route("/admin/movie_theatre/delete", methods=["GET","POST"])
def delete_movie_theatre():
    db = shelve.open('shelve.db', 'c')    
    try:
        Movie_theatre_dict = db["movie_theatre"]
        Deleted_list = db["deleted_movie_theatre"]
    except:        
        Movie_theatre_dict = {}
        Deleted_list = []
        db["movie_theatre"] = Movie_theatre_dict
        db["deleted_movie_theatre"] = Deleted_list

    list_of_to_be_deleted_theatres = request.json       
    for theatre_id in list_of_to_be_deleted_theatres: 
        delete_theatre = Movie_theatre_dict[int(theatre_id)]                    
        Deleted_list.append([delete_theatre, datetime.date.today()])
        del Movie_theatre_dict[int(theatre_id)]
    db["movie_theatre"] = Movie_theatre_dict
    db["deleted_movie_theatre"] = Deleted_list
    db.close()    
    return redirect(url_for('admin_movie_theatre'))

#* Movies
@app.route("/admin/movies")
def admin_movies():
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    db.close()
    return render_template("Admin/movie/movies.html", title="Movies", Movies_dict=Movies_dict)

@app.route("/admin/movies/add_movie", methods=["POST","GET"])
def add_movie():
    form = CreateMovieForm()
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
        Movie.id = list(Movies_dict.values())[-1].get_id()
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    if form.validate_on_submit():        
        movie_name = form.movie_name.data
        movie_poster = save_picture(form.movie_poster.data, "movie poster")
        movie_description = form.movie_description.data
        movie_genre = form.movie_genre.data
        movie_casts = form.movie_casts.data
        movie_director = form.movie_director.data
        movie_fullvideo = save_video(form.movie_fullvideo.data, "movie fullvideo")
        movie_trailer = save_video(form.movie_trailer.data, "movie trailer")
        movie_duration = form.movie_duration.data
        movie_release_date = form.movie_release_date.data
        movie_language = form.movie_language.data
        movie_subtitles = form.movie_subtitles.data
        movie_class = Movie(movie_name, movie_poster, movie_description, movie_genre, movie_casts, movie_director, movie_fullvideo, movie_trailer, movie_duration, movie_release_date, movie_language, movie_subtitles)
        movie_id = movie_class.get_id()    
        Movies_dict[movie_id] = movie_class
        db["movies"] = Movies_dict        
        db.close()
        return redirect(url_for("admin_movies"))
    elif request.method == "GET":
        form.movie_name.data = ""
        form.movie_description.data = ""
        form.movie_genre.data = ""
        form.movie_casts.data = ""
        form.movie_director.data = ""
        form.movie_duration.data = ""
        form.movie_release_date.data = ""
        form.movie_language.data = "English"
        form.movie_subtitles.data = "Chinese"
        db.close()
    return render_template("Admin/movie/add_movie.html", title="Add Movie", form=form)

@app.route("/admin/movies/modify_movie/<movie_id>", methods=["POST", "GET"])
def modify_movie(movie_id):
    movie_id = int(movie_id)
    form = ModifyMovieForm()
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    if form.validate_on_submit():
        movie_name = form.movie_name.data
        movie_poster = save_picture(form.movie_poster.data, "movie poster")
        movie_description = form.movie_description.data
        movie_genre = form.movie_genre.data
        movie_casts = form.movie_casts.data
        movie_director = form.movie_director.data
        movie_fullvideo = save_video(form.movie_fullvideo.data, "movie fullvideo")
        movie_trailer = save_video(form.movie_trailer.data, "movie trailer")
        movie_duration = form.movie_duration.data
        movie_release_date = form.movie_release_date.data
        movie_language = form.movie_language.data
        movie_subtitles = form.movie_subtitles.data
        movie_class = Movies_dict[movie_id]
        movie_class.set_all_attributes(movie_name, movie_poster, movie_description, movie_genre, movie_casts, movie_fullvideo, movie_trailer, movie_duration, movie_release_date, movie_language, movie_subtitles, movie_director)
        Movies_dict[movie_id] = movie_class
        db["movies"] = Movies_dict        
        db.close()
        return redirect(url_for("admin_movies"))
    elif request.method == "GET":
        movie_class = Movies_dict[movie_id]
        form.movie_name.data = movie_class.get_movie_name()
        image_source = movie_class.get_poster()
        form.movie_description.data = movie_class.get_description()
        form.movie_genre.data = movie_class.get_genre()
        form.movie_casts.data = movie_class.get_casts()
        form.movie_director.data = movie_class.get_director()
        fullvideo_source = movie_class.get_movie_fullvideo()
        trailer_source = movie_class.get_trailer()
        form.movie_duration.data = movie_class.get_duration()
        form.movie_release_date.data = movie_class.get_release_date()
        form.movie_language.data = movie_class.get_language()
        form.movie_subtitles.data = movie_class.get_subtitles()
    return render_template("Admin/movie/modify_movie.html", title="Modify Movie Theatre", form=form, image_source=image_source, trailer_source=trailer_source, fullvideo_source=fullvideo_source)

@app.route("/admin/movies/delete", methods=["POST","GET"])
def delete_movie():
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
        Deleted_list = db["deleted_movies"]
    except:
        Movies_dict = {}
        Deleted_list = []
        db["movies"] = Movies_dict
        db["deleted_movies"] = Deleted_list
    list_of_to_be_deleted_movies = request.json
    for movie_id in list_of_to_be_deleted_movies:
        delete_movie = Movies_dict[int(movie_id)]        
        Deleted_list.append([delete_movie, datetime.date.today()])
        del Movies_dict[int(movie_id)]
    db["movies"] = Movies_dict
    db["deleted_movies"] = Deleted_list
    db.close()
    return redirect(url_for("admin_movies"))

#* Promotion
@app.route("/admin/promotion")
def admin_promotion():    
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    db.close()    
    return render_template("Admin/promotion/promotion.html", title="Promotion", Promotion_dict=Promotion_dict)

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
        promotion_image = save_picture(form.promotion_image.data, "promotion")
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
    promotion_id = int(promotion_id)
    form = ModifyPromotion()
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    if form.validate_on_submit():
        promotion_title = form.promotion_title.data
        promotion_image = save_picture(form.promotion_image.data, "promotion")
        promotion_description = form.promotion_description.data
        promotion_terms_and_conditions = form.promotion_terms_and_condition.data.split("\n")
        promotion_period = form.promotion_valid_start_date.data + " - " + form.promotion_valid_end_date.data
        promotion_applicable_to = form.promotion_applicable_to.data
        # editing class, not creating new one as id will newly be generated
        promotion_class = Promotion_dict[promotion_id]
        promotion_class.set_all_attributes(promotion_title, promotion_image, Markup(promotion_description), promotion_terms_and_conditions, promotion_period, promotion_applicable_to)     
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
        Deleted_list = db["deleted_promotion"]
    except:        
        Promotion_dict = {}
        Deleted_list = []            
        db["promotion"] = Promotion_dict
        db["deleted_promotion"] = Deleted_list    
    
    list_of_to_be_deleted_promotions = request.json       
    for promotion_id in list_of_to_be_deleted_promotions:                              
        delete_promotion = Promotion_dict[int(promotion_id)]                    
        Deleted_list.append([delete_promotion, datetime.date.today()])
        del Promotion_dict[int(promotion_id)]
    db["promotion"] = Promotion_dict
    db["deleted_promotion"] = Deleted_list
    db.close()
    return redirect(url_for('admin_promotion'))

#* Carousel
@app.route("/admin/carousel")
def admin_carousel():
    db = shelve.open('shelve.db', 'c')
    try:
        Carousel_dict = db['carousel']
    except:
        Carousel_dict = {}
        db['carousel'] = Carousel_dict
    db.close()
    return render_template("Admin/carousel/carousel.html", title="Carousel", Carousel_dict=Carousel_dict)

@app.route("/admin/carousel/add_carousel", methods=["POST","GET"])
def add_carousel():
    form = CreateCarousel()
    db = shelve.open('shelve.db', 'c')
    try:
        Carousel_dict = db['carousel']
        Carousel.id = list(Carousel_dict.values())[-1].get_id()
    except:        
        Carousel_dict = {}
        db['carousel'] = Carousel_dict
    if form.validate_on_submit():        
        carousel_title = form.carousel_title.data
        carousel_image = save_picture(form.carousel_image.data, "carousel")              
        carousel_category = form.carousel_category.data
        carousel_class = Carousel(carousel_title,carousel_category,carousel_image)
        carousel_id = carousel_class.get_id()
        Carousel_dict[carousel_id] = carousel_class
        db["carousel"] = Carousel_dict
        db.close()
        return redirect(url_for("admin_carousel"))
    elif request.method == "GET":
        form.carousel_title.data = ""        
        form.carousel_category.data = ""
    return render_template("Admin/carousel/add_carousel.html", title="Add Carousel", form=form)

@app.route("/admin/carousel/modify_carousel/<carousel_id>", methods=["POST","GET"])
def modify_carousel(carousel_id):
    form = ModifyCarousel()
    db = shelve.open('shelve.db', 'c')
    try:
        Carousel_dict = db['carousel']
    except:        
        Carousel_dict = {}
        db['carousel'] = Carousel_dict
    carousel_id = int(carousel_id)
    if form.validate_on_submit():
        carousel_title = form.carousel_title.data
        carousel_image = save_picture(form.carousel_image.data, "carousel")              
        carousel_category = form.carousel_category.data
        carousel_class = Carousel_dict[carousel_id]
        carousel_class.set_all_attributes(carousel_title, carousel_category, carousel_image)        
        Carousel_dict[carousel_id] = carousel_class
        db["carousel"] = Carousel_dict
        db.close()
        return redirect(url_for("admin_carousel"))
    elif request.method == "GET":
        carousel = Carousel_dict[carousel_id]
        form.carousel_title.data = carousel.get_title()
        form.carousel_category.data = carousel.get_category()
        form.carousel_image.data = carousel.get_carousel_image()      
        image_source = carousel.get_carousel_image()
    return render_template("Admin/carousel/modify_carousel.html", title="Modify Carousel", form=form, image_source=image_source)

@app.route("/admin/carousel/delete", methods=["GET","POST"])
def delete_carousel():
    db = shelve.open('shelve.db', 'c')
    try:
        Carousel_dict = db["carousel"]
        Deleted_list = db["deleted_carousel"]
    except:        
        Carousel_dict = {}
        Deleted_list = []            
        db["carousel"] = Carousel_dict
        db["deleted_carousel"] = Deleted_list    
    
    list_of_to_be_deleted_carousels = request.json       
    for carousel_id in list_of_to_be_deleted_carousels:                              
        delete_carousel = Carousel_dict[int(carousel_id)]                    
        Deleted_list.append([delete_carousel, datetime.date.today()])
        del Carousel_dict[int(carousel_id)]
    db["carousel"] = Carousel_dict
    db["deleted_carousel"] = Deleted_list
    db.close()
    return redirect(url_for('admin_carousel'))

def save_picture(form_picture, path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/' + path, picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def save_video(form_video, path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_video.filename)
    video_fn = random_hex + f_ext
    video_path = os.path.join(app.root_path, 'static/videos/' + path, video_fn)
    form_video.save(video_path)
    return video_fn

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

if __name__ == "__main__":
    app.run(debug=True)
# dhbcdsbc