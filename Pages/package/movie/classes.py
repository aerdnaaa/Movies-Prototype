class Movie:
    id = 0
    def __init__(self, movie_name, poster, description, genre, casts, director, fullvideo, trailer, duration, release_date, language, subtitles):
        Movie.id += 1
        self.__id = Movie.id
        self.__movie_name = movie_name
        self.__poster = poster
        self.__description = description
        self.__genre = genre
        self.__casts = casts
        self.__fullvideo = fullvideo
        self.__trailer = trailer
        self.__duration = duration
        self.__release_date = release_date
        self.__language = language
        self.__subtitles = subtitles
        self.__director = director

    def get_id(self):
        return self.__id

    def get_movie_name(self):
        return self.__movie_name

    def get_poster(self):
        return self.__poster

    def get_description(self):
        return self.__description

    def get_genre(self):
        return self.__genre

    def get_casts(self):
        return self.__casts

    def get_movie_fullvideo(self):
        return self.__fullvideo

    def get_trailer(self):
        return self.__trailer

    def get_duration(self):
        return self.__duration

    def get_release_date(self):
        return self.__release_date

    def get_language(self):
        return self.__language

    def get_subtitles(self):
        return self.__subtitles

    def get_director(self):
        return self.__director

    def set_movie_name(self, movie_name):
        self.__movie_name = movie_name

    def set_poster(self, poster):
        self.__poster = poster

    def set_description(self, description):
        self.__description = description

    def set_genre(self, genre):
        self.__genre = genre

    def set_casts(self, casts):
        self.__casts = casts

    def set_movie_fullvideo(self, movie_fullvideo):
        self.__movie_fullvideo = movie_fullvideo

    def set_trailer(self, trailer):
        self.__trailer = trailer

    def set_duration(self, duration):
        self.__duration = duration

    def set_release_date(self, release_date):
        self.__release_date = release_date

    def set_language(self, language):
        self.__language = language

    def set_subtitles(self, subtitles):
        self.__subtitles = subtitles

    def set_director(self, director):
        self.__director = director
    
    def set_all_attributes(self, movie_name, poster, description, genre, casts, fullvideo, trailer, duration, release_date, language, subtitles, director):        
        self.__movie_name = movie_name
        self.__poster = poster
        self.__description = description
        self.__genre = genre
        self.__casts = casts
        self.__fullvideo = fullvideo
        self.__trailer = trailer
        self.__duration = duration
        self.__release_date = release_date
        self.__language = language
        self.__subtitles = subtitles
        self.__director = director
