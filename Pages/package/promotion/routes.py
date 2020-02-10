from flask import Blueprint
from flask import render_template, request, redirect, url_for, Markup, flash
from flask_login import current_user, login_required
from package.promotion.forms import CreatePromotion, ModifyPromotion
from package.promotion.classes import Promotion
from package.promotion.utilis import save_picture
from package.utilis import check_admin, check_rights
import shelve, datetime

promotion_blueprint = Blueprint("promotion", __name__)

#* User Promotion
@promotion_blueprint.route("/promotions")
def promotion():
    #opening shelve with create
    db = shelve.open("shelve.db", "c")
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    lst=[]
    for i in Promotion_dict:
        k = Promotion_dict[i].get_applicable_to()
        if k not in lst:
            lst.append(k)
    
    conditions = ["Student", "Elderly"]
    
    # promotion_list needs a list in a list. Outer list for rows, inner list for promotions in 1 row
    return render_template("User 2/promotion.html", title="Promotions", Promotion_dict=Promotion_dict, applicabletoLst=lst, condition_list=conditions)

@promotion_blueprint.route("/promotion/<id_of_promo>")
def promotionDetail(id_of_promo):
    db = shelve.open("shelve.db", "c")
    Promotion_dict = db["promotion"]
    promo = Promotion_dict[id_of_promo]
    raw_valid_period = promo.get_valid_period().split(" to ")
    valid_period = []
    print(raw_valid_period[0])
    for date in raw_valid_period:
        date = date.split("-")
        mth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        valid_period.append(f"{int(date[2])} {mth[int(date[1]) - 1]} {date[0]}")
    valid_period_str = f"{valid_period[0]} - {valid_period[1]}"

    return render_template("User 2/promotionDetail.html", promo=promo, period=valid_period_str, title=promo.get_title().capitalize() + " Promo")


#* Admin Promotion
@promotion_blueprint.route("/admin/promotion")
@login_required
def admin_promotion():    
    check_admin()
    check_rights()
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    db.close()    
    return render_template("Admin/promotion/promotion.html", title="Promotion", Promotion_dict=Promotion_dict )

@promotion_blueprint.route("/admin/promotion/add_promotion", methods=["POST","GET"])
@login_required
def add_promotion():
    check_admin()
    check_rights()
    form = CreatePromotion()
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
        Promotion.id = list(Promotion_dict.values())[-1].get_id()
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict  
    print(form.promotion_image.data)  
    if request.method == "POST" and form.validate_on_submit():        
        promotion_title = form.promotion_title.data
        promotion_image = save_picture(form.promotion_image.data, "promotion")
        promotion_description = Markup(form.promotion_description.data)
        promotion_terms_and_conditions = form.promotion_terms_and_condition.data.split("\n")
        promotion_promoPrice = form.promotion_promoPrice.data
        promotion_period = form.promotion_valid_start_date.data + " to " + form.promotion_valid_end_date.data
        promotion_applicable_to = form.promotion_applicable_to.data
        promotion_class = Promotion(promotion_title,promotion_image,promotion_description,promotion_terms_and_conditions,promotion_period,promotion_applicable_to,promotion_promoPrice)
        promotion_id = promotion_class.get_id()
        Promotion_dict[promotion_id] = promotion_class
        db["promotion"] = Promotion_dict
        db.close()
        flash("Promotion has been added !", "success")
        return redirect(url_for("promotion.admin_promotion"))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("Some field(s) are incorrect. Please try again", "danger")
    elif request.method == "GET":
        form.promotion_title.data = ""        
        form.promotion_description.data = ""
        form.promotion_terms_and_condition.data = ""
        form.promotion_promoPrice.data = 0
        form.promotion_valid_start_date.data = ""
        form.promotion_valid_end_date.data = ""
        form.promotion_applicable_to.data = ""
    return render_template("Admin/promotion/add_promotion.html", title="Add Promotion", form=form)

@promotion_blueprint.route("/admin/promotion/modify_promotion/<promotion_id>", methods=["POST","GET"])
@login_required
def modify_promotion(promotion_id):
    check_admin()
    check_rights()
    form = ModifyPromotion()
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    promotion = Promotion_dict[promotion_id]
    image_source = promotion.get_promotion_image()
    if request.method == "POST" and form.validate_on_submit():
        promotion_title = form.promotion_title.data
        promotion_image = save_picture(form.promotion_image.data, "promotion")
        promotion_description = form.promotion_description.data
        promotion_terms_and_conditions = form.promotion_terms_and_condition.data.split("\n")
        promotion_promoPrice = form.promotion_promoPrice.data
        promotion_period = form.promotion_valid_start_date.data + " to " + form.promotion_valid_end_date.data
        promotion_applicable_to = form.promotion_applicable_to.data
        # editing class, not creating new one as id will newly be generated
        promotion_class = Promotion_dict[promotion_id]
        promotion_class.set_all_attributes(promotion_title, promotion_image, Markup(promotion_description), promotion_terms_and_conditions,promotion_period, promotion_applicable_to,promotion_promoPrice)     
        Promotion_dict[promotion_id] = promotion_class
        db["promotion"] = Promotion_dict
        db.close()
        flash("Promotion has been modified !", "success")
        return redirect(url_for("promotion.admin_promotion"))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("Some field(s) are incorrect. Please try again", "danger")
    elif request.method == "GET":
        
        form.promotion_title.data = promotion.get_title()
        form.promotion_description.data = promotion.get_description()
        form.promotion_terms_and_condition.data = "\n".join(promotion.get_terms_and_conditions())
        form.promotion_promoPrice.data = promotion.get_promoPrice()
        start_date, end_date = promotion.get_valid_period().split(" to ")
        form.promotion_valid_start_date.data = start_date
        form.promotion_valid_end_date.data = end_date
        form.promotion_applicable_to.data = promotion.get_applicable_to()
        
    return render_template("Admin/promotion/modify_promotion.html", title="Modify Promotion", form=form, image_source=image_source)

@promotion_blueprint.route("/admin/promotion/delete", methods=["GET","POST"])
@login_required
def delete_promotion():
    check_admin()
    check_rights()
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
        delete_promotion = Promotion_dict[promotion_id]                    
        Deleted_list.append([delete_promotion, datetime.date.today()])
        del Promotion_dict[promotion_id]
    db["promotion"] = Promotion_dict
    db["deleted_promotion"] = Deleted_list
    db.close()
    flash("Promotion has been deleted !", "success")
    return redirect(url_for('promotion.admin_promotion'))

