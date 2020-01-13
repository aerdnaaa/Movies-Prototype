from flask import Blueprint
from flask import render_template, request, redirect, url_for, Markup
from package.promotion.forms import CreatePromotion, ModifyPromotion
from package.promotion.classes import Promotion
from package.promotion.utilis import save_picture
import shelve, datetime

promotion_blueprint = Blueprint("promotion", __name__)

#* User Promotion
@promotion_blueprint.route("/promotions")
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

@promotion_blueprint.route("/promotion/<id_of_promo>")
def promotionDetail(id_of_promo):
    db = shelve.open("shelve.db", "c")
    Promotion_dict = db["promotion"]
    promo = Promotion_dict[int(id_of_promo)]
    return render_template("User/promotionDetail.html", promo=promo, title=promo.get_title().capitalize() + " Promo")


#* Admin Promotion
@promotion_blueprint.route("/admin/promotion")
def admin_promotion():    
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    db.close()    
    return render_template("Admin/promotion/promotion.html", title="Promotion", Promotion_dict=Promotion_dict)

@promotion_blueprint.route("/admin/promotion/add_promotion", methods=["POST","GET"])
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
        return redirect(url_for("promotion.admin_promotion"))
    elif request.method == "GET":
        form.promotion_title.data = ""        
        form.promotion_description.data = ""
        form.promotion_terms_and_condition.data = ""
        form.promotion_valid_start_date.data = ""
        form.promotion_valid_end_date.data = ""
        form.promotion_applicable_to.data = ""
    return render_template("Admin/promotion/add_promotion.html", title="Add Promotion", form=form)

@promotion_blueprint.route("/admin/promotion/modify_promotion/<promotion_id>", methods=["POST","GET"])
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
        return redirect(url_for("promotion.admin_promotion"))
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

@promotion_blueprint.route("/admin/promotion/delete", methods=["GET","POST"])
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
    return redirect(url_for('promotion.admin_promotion'))

