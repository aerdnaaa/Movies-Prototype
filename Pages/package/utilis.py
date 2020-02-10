from flask import redirect, url_for, render_template, abort, request
from flask_login import current_user
from package.user.classes import Admin
import shelve
from package import bcrypt, app


def check_admin():
    print(f"{current_user.get_id()} tried to access admin pages")
    if current_user.get_id()[0] != "A":
        abort(401)

def check_if_login():
    if current_user.is_authenticated:
        abort(403)

def check_rights():
    url_path = request.path
    url_purpose = url_path.split("/")[2]  # /admin/[url_purpose]/.../...
    current_admin_rights = current_user.get_administrative_rights()
    if not "Super Admin" in current_admin_rights:
        if url_purpose == "home":
            return current_admin_rights[0]
        if url_purpose == "admin_accounts":
            if not "Manage admins" in current_admin_rights:
                abort(401)
        if url_purpose == "user_accounts":
            if not "Manage users" in current_admin_rights:
                abort(401)
        if url_purpose == "carousel":
            if not "Carousel" in current_admin_rights:
                abort(401)
        if url_purpose == "movie_theatre":
            if not "Theatres" in current_admin_rights:
                abort(401)
        if url_purpose == "movies":
            if not "Movies" in current_admin_rights:
                abort(401)
        if url_purpose == "rental":
            if not "Rental" in current_admin_rights:
                abort(401)
        if url_purpose == "showtime":
            if not "Showtime" in current_admin_rights:
                abort(401)
        if url_purpose == "promotion":
            if not "Promotion" in current_admin_rights:
                abort(401)

def check_admin_id():
    url_path = request.path
    url_admin_id = url_path.split("/")[4]
    if url_admin_id == current_user.get_id() or url_admin_id == "A0":
        abort(401)
        

def set_up_variables():
    db = shelve.open("shelve.db", "c")
    # creating admin account / ensuring a super admin account exists
    # creating genre list
    # initialize seats
    try:
        genre_list = db["genre_list"]
        if genre_list == []:
            genre_list = [("Action","Action"),("Adventure","Adventure"),("Comedy","Comedy"),("Drama","Drama"),("Fantasy","Fantasy"),("History","History"),("Horror","Horror"),("Music","Music"),("Mystery/Crime","Mystery/Crime"),("Romance","Romance"),("Sci-fi","Sci-fi")]
            db["genre_list"] = genre_list

    except:
        genre_list = [("Action","Action"),("Adventure","Adventure"),("Comedy","Comedy"),("Drama","Drama"),("Fantasy","Fantasy"),("History","History"),("Horror","Horror"),("Music","Music"),("Mystery/Crime","Mystery/Crime"),("Romance","Romance"),("Sci-fi","Sci-fi")]
        db["genre_list"] = genre_list

    try:
        user_dict = db['Users']          
        if user_dict["A0"] == None:
            user_dict["A0"] = Admin("Super Admin", "superadmin@saw.com", ["Super Admin"], bcrypt.generate_password_hash("Admin").decode("utf-8") )            
    except:        
        user_dict = {}
        user_dict["A0"] = Admin("Super Admin", "superadmin@saw.com", ["Super Admin"], bcrypt.generate_password_hash("Admin").decode("utf-8") )
        db["Users"] = user_dict 
    try:
        seat_dict = db["Seats"]   
        if seat_dict == None:
            seat_dict = {'A1': 'standard_available', 'A2': 'standard_available', 'A3': 'standard_available', 'A4': 'standard_available', 'A5': 'standard_available', 'A6': 'standard_available', 'A7': 'standard_available', 'A8': 'standard_available', 
            'B1': 'standard_available', 'B2': 'standard_available', 'B3': 'standard_available', 'B4': 'standard_available', 'B5': 'standard_available', 'B6': 'standard_available', 'B7': 'standard_available', 'B8': 'standard_available', 
            'C1': 'standard_available', 'C2': 'standard_available', 'C3': 'standard_available', 'C4': 'standard_available', 'C5': 'standard_available', 'C6': 'standard_available', 'C7': 'standard_available', 'C8': 'standard_available', 
            'D1': 'standard_available', 'D2': 'standard_available', 'D3': 'standard_available', 'D4': 'standard_available', 'D5': 'standard_available', 'D6': 'standard_available', 'D7': 'standard_available', 'D8': 'standard_available', 
            'E1': 'standard_available', 'E2': 'standard_available', 'E3': 'standard_available', 'E4': 'standard_available', 'E5': 'standard_available', 'E6': 'standard_available', 'E7': 'standard_available', 'E8': 'standard_available'}
    except:
        seat_dict = {}
        seat_dict = {'A1': 'standard_available', 'A2': 'standard_available', 'A3': 'standard_available', 'A4': 'standard_available', 'A5': 'standard_available', 'A6': 'standard_available', 'A7': 'standard_available', 'A8': 'standard_available', 
            'B1': 'standard_available', 'B2': 'standard_available', 'B3': 'standard_available', 'B4': 'standard_available', 'B5': 'standard_available', 'B6': 'standard_available', 'B7': 'standard_available', 'B8': 'standard_available', 
            'C1': 'standard_available', 'C2': 'standard_available', 'C3': 'standard_available', 'C4': 'standard_available', 'C5': 'standard_available', 'C6': 'standard_available', 'C7': 'standard_available', 'C8': 'standard_available', 
            'D1': 'standard_available', 'D2': 'standard_available', 'D3': 'standard_available', 'D4': 'standard_available', 'D5': 'standard_available', 'D6': 'standard_available', 'D7': 'standard_available', 'D8': 'standard_available', 
            'E1': 'standard_available', 'E2': 'standard_available', 'E3': 'standard_available', 'E4': 'standard_available', 'E5': 'standard_available', 'E6': 'standard_available', 'E7': 'standard_available', 'E8': 'standard_available'}
        db["Seats"] = seat_dict
    db.close()

def generate_pdf(email, receipt_id, data):
    import time, os
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    pdf_fn = receipt_id +".pdf"
    pdf_path = os.path.join(app.root_path, 'static/pdf/' , pdf_fn)
    doc = SimpleDocTemplate(pdf_path,pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    Story=[]
    # logo = app.route_path, 'static/images/logo.png'
    
    movie_theatre = data['showtime_class'].get_theatre_class().get_theatre_name()
    movie = data['showtime_class'].get_movie_class().get_movie_name()
    hall = data['showtime_class'].get_hall_number()
    list_seats = data['seats']
    seats = ",".join(list_seats)
    price = len(list_seats) * 8.5
    purchase_date = data['date']

    formatted_time = time.ctime()

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    
    ptext = '<font size=20>Saw Theatre</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    # im = Image(logo, 2*inch, 2*inch)
    # Story.append(im)
    
    ptext = '<font size=12>%s</font>' % formatted_time
    
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Dear Customer:</font>' 
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    
    ptext = f'''<font size=14>User details</font>\n<font size=12>Email: {email}</font>'''
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    
    ptext = f'<font size=14>Billing Information</font>\n<font size=12>Movie Theatre: {movie_theatre}     Movie: {movie}</font>\n<font size=12>Hall: {hall}     Seat(s) chosen: {seats}</font>\n<font size=12>Price: ${price:.2f}     Date of purchase: {purchase_date}</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ptext = f'<font size=14>Receipt ID: {receipt_id}</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
        
    ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Sincerely,</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 48))
    ptext = '<font size=12>Saw Theatre Pte Ltd</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    doc.build(Story)

