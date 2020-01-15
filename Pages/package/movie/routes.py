from flask import Blueprint
from flask import render_template, request, redirect, url_for, Markup
from package.movie.forms import CreateMovieForm, ModifyMovieForm
from package.movie.classes import Movie
from package.movie.utilis import save_picture, save_video
import shelve, datetime

movie_blueprint = Blueprint("movie", __name__)

#* User Movie
# list of movies
@movie_blueprint.route("/movieslist")
def movieslist():
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]        
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    sorted_dict = {}
    id = 0
    for key in Movies_dict:
        if key % 6 == 1:
            list_of_movies = []
            id += 1
            list_of_movies.append(Movies_dict[key])
            sorted_dict[id] = list_of_movies
                    
        else:
            list_of_movies.append(Movies_dict[key])
            sorted_dict[id] = list_of_movies
    print(sorted_dict)

    return render_template("User/movieslist.html", title="Movies List", Movies_dict=Movies_dict)



#* Admin Promotion
@movie_blueprint.route("/admin/movies")
def admin_movies():
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    db.close()
    return render_template("Admin/movie/movies.html", title="Movies", Movies_dict=Movies_dict)

@movie_blueprint.route("/admin/movies/add_movie", methods=["POST","GET"])
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
        return redirect(url_for("movie.admin_movies"))
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

@movie_blueprint.route("/admin/movies/modify_movie/<movie_id>", methods=["POST", "GET"])
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
        return redirect(url_for("movie.admin_movies"))
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

@movie_blueprint.route("/admin/movies/delete", methods=["POST","GET"])
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
    return redirect(url_for("movie.admin_movies"))

