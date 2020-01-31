from flask import Blueprint, jsonify
from flask import render_template, request, redirect, url_for
from package.carousel.forms import CreateCarousel, ModifyCarousel
from package.carousel.classes import Carousel
from package.carousel.utilis import save_picture
from flask_login import login_required
import shelve, datetime

carousel_blueprint = Blueprint("carousel", __name__)


#* Home Page contains carousel
@carousel_blueprint.route("/")
@carousel_blueprint.route("/home")
def home():
    db = shelve.open("shelve.db")
    try:
        Carousel_dict = db['carousel']
    except:
        Carousel_dict = {}
        db['carousel'] = Carousel_dict
    return render_template("User 2/index.html", title="Home", Carousel_dict=Carousel_dict )

#* Admin Carousel
@login_required
@carousel_blueprint.route("/admin/carousel")
def admin_carousel():
    db = shelve.open('shelve.db', 'c')
    try:
        Carousel_dict = db['carousel']
    except:
        Carousel_dict = {}
        db['carousel'] = Carousel_dict
    db.close()
    return render_template("Admin/carousel/carousel.html", title="Carousel", Carousel_dict=Carousel_dict)

@carousel_blueprint.route("/admin/carousel/add_carousel", methods=["POST","GET"])
def add_carousel():
    form = CreateCarousel()
    db = shelve.open('shelve.db', 'c')
    try:
        Carousel_dict = db['carousel']
        Carousel.id = list(Carousel_dict.values())[-1].get_id()
    except:        
        Carousel_dict = {}
        db['carousel'] = Carousel_dict
    if request.method == "POST":        
        category = form.carousel_category.data
        carousel_title_list = form.carousel_title.data
        db = shelve.open("shelve.db", 'c')
        try:
            title_dict = db[category]
        except:
            title_dict = {}
            db[category] = title_dict
        for key in carousel_title_list:
            value = title_dict[key]
            if category == "movies":
                carousel_class = Carousel(value.get_movie_name(), "movie poster/" + value.get_poster())
            else:
                carousel_class = Carousel(value.get_title(), "promotion/" + value.get_promotion_image())
            carousel_id = carousel_class.get_id()
            Carousel_dict[carousel_id] = carousel_class
        db["carousel"] = Carousel_dict
        db.close()
        return redirect(url_for("carousel.admin_carousel"))
    elif request.method == "GET":
        form.carousel_category.data = "movies" 
        db = shelve.open("shelve.db", 'c')
        try:
            title_dict = db["movies"]
        except:
            title_dict = {}
            db["movies"] = title_dict
        tuple_list = []
        for key , value in title_dict.items():            
            tuple_list.append((key, value.get_movie_name()))

        form.carousel_title.choices = tuple_list
    return render_template("Admin/carousel/add_carousel.html", title="Add Carousel", form=form)

@carousel_blueprint.route("/admin/carousel/modify_carousel/<carousel_id>", methods=["POST","GET"])
def modify_carousel(carousel_id):
    form = ModifyCarousel()
    db = shelve.open('shelve.db', 'c')
    try:
        Carousel_dict = db['carousel']
    except:        
        Carousel_dict = {}
        db['carousel'] = Carousel_dict
    if form.validate_on_submit():
        carousel_title = form.carousel_title.data             
        carousel_category = form.carousel_category.data
        carousel_class = Carousel_dict[carousel_id]
        carousel_class.set_all_attributes(carousel_title, carousel_category)        
        Carousel_dict[carousel_id] = carousel_class
        db["carousel"] = Carousel_dict
        db.close()
        return redirect(url_for("carousel.admin_carousel"))
    elif request.method == "GET":
        pass
    return render_template("Admin/carousel/modify_carousel.html", title="Modify Carousel", form=form)
@carousel_blueprint.route("/admin/carousel/delete", methods=["GET","POST"])
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
        delete_carousel = Carousel_dict[carousel_id]                    
        Deleted_list.append([delete_carousel, datetime.date.today()])
        del Carousel_dict[carousel_id]
    db["carousel"] = Carousel_dict
    db["deleted_carousel"] = Deleted_list
    db.close()
    return redirect(url_for('carousel.admin_carousel'))

@carousel_blueprint.route("/admin/carousel_title/<category>")
def return_carousel_title(category):
    db = shelve.open("shelve.db", 'c')
    try:
        title_dict = db[category]
    except:
        title_dict = {}
        db[category] = title_dict
    title_new_dict = {}
    for key , value in title_dict.items():
        if category == "movies":
            title_new_dict[key] = value.get_movie_name()
        else:
            title_new_dict[key] = value.get_title()
    print(title_new_dict)
    db.close()
    return jsonify({"carousel_title":title_new_dict})
