# this sets the attributes and methods of a promotion

class Promotion:
    def __init__(self, title, promotion_image, description, terms_and_conditions):
        self.__title = title
        self.__promotion_image = promotion_image
        self.__description = description
        self.__terms_and_conditions = terms_and_conditions

    def get_title(self):
        return self.__title

    def get_promotion_image(self):
        return self.__promotion_image

    def get_description(self):
        return self.__description

    def get_terms_and_conditions(self):
        return self.__terms_and_conditions

    def set_title(self, title):
        self.__title = title

    def set_promotion_image(self, promotion_image):
        self.__promotion_image = promotion_image

    def set_description(self, description):
        self.__description = description

    def set_terms_and_conditions(self, terms_and_conditions):
        self.__terms_and_conditions = terms_and_conditions