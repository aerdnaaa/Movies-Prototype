from flask import Blueprint
from flask import render_template, request, redirect, url_for
from package.carousel.forms import CreateCarousel, ModifyCarousel
from package.carousel.classes import Carousel
from package.carousel.utilis import save_picture
import shelve, datetime

carousel_blueprint = Blueprint("carousel", __name__)


#* Home Page contains carousel
@carousel_blueprint.route("/")
@carousel_blueprint.route("/home")
def home():
    db = shelve.open("shelve.db")
    return render_template("User 2/index.html", title="Home", carousel_list=["carousel1.jpeg","carousel2.jpeg","carousel3.jpeg"], )

#* Admin Carousel
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
    if form.validate_on_submit():        
        carousel_title = form.carousel_title.data
        carousel_image = save_picture(form.carousel_image.data, "carousel")              
        carousel_category = form.carousel_category.data
        carousel_class = Carousel(carousel_title,carousel_category,carousel_image)
        carousel_id = carousel_class.get_id()
        Carousel_dict[carousel_id] = carousel_class
        db["carousel"] = Carousel_dict
        db.close()
        return redirect(url_for("carousel.admin_carousel"))
    elif request.method == "GET":
        form.carousel_title.data = ""        
        form.carousel_category.data = ""
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
        return redirect(url_for("carousel.admin_carousel"))
    elif request.method == "GET":
        carousel = Carousel_dict[carousel_id]
        form.carousel_title.data = carousel.get_title()
        form.carousel_category.data = carousel.get_category()
        form.carousel_image.data = carousel.get_carousel_image()      
        image_source = carousel.get_carousel_image()
    return render_template("Admin/carousel/modify_carousel.html", title="Modify Carousel", form=form, image_source=image_source)

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
        delete_carousel = Carousel_dict[int(carousel_id)]                    
        Deleted_list.append([delete_carousel, datetime.date.today()])
        del Carousel_dict[int(carousel_id)]
    db["carousel"] = Carousel_dict
    db["deleted_carousel"] = Deleted_list
    db.close()
    return redirect(url_for('carousel.admin_carousel'))
