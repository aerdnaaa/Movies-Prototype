class Carousel:
    id = "C0"
    def __init__(self, title, carousel_image):
        Carousel.id = Carousel.id[0] + str(int(Carousel.id[1:])+1)
        self.__id = Carousel.id
        self.__title = title
        self.__carousel_image = carousel_image

    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_carousel_image(self):
        return self.__carousel_image

    def set_title(self, title):
        self.__title = title

    def set_carousel_image(self, carousel_image):
        self.__carousel_image = carousel_image

    def set_all_attributes(self, title, carousel_image):
        self.__title = title      
        self.__carousel_image = carousel_image
