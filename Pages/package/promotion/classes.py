class Promotion:
    id = "P0"
    def __init__(self, title, promotion_image, description, terms_and_conditions, valid_period, applicable_to):
        Promotion.id = Promotion.id[0] + str(int(Promotion.id[1:])+1)
        self.__id = Promotion.id
        self.__title = title
        self.__promotion_image = promotion_image
        self.__description = description
        self.__terms_and_conditions = terms_and_conditions
        self.__valid_period = valid_period
        self.__applicable_to = applicable_to        

    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_promotion_image(self):
        return self.__promotion_image

    def get_description(self):
        return self.__description

    def get_terms_and_conditions(self):
        return self.__terms_and_conditions
        
    def get_valid_period(self):
        return self.__valid_period

    def get_applicable_to(self):
        return self.__applicable_to

    def set_title(self, title):
        self.__title = title

    def set_promotion_image(self, promotion_image):
        self.__promotion_image = promotion_image

    def set_description(self, description):
        self.__description = description

    def set_terms_and_conditions(self, terms_and_conditions):
        self.__terms_and_conditions = terms_and_conditions
    
    def set_valid_period(self, valid_period):
        self.__valid_period = valid_period
    
    def set_applicable_to(self, applicable_to):
        self.__applicable_to = applicable_to

    def set_all_attributes(self, title, promotion_image, description, terms_and_conditions, valid_period, applicable_to):
        self.__title = title
        self.__promotion_image = promotion_image
        self.__description = description
        self.__terms_and_conditions = terms_and_conditions
        self.__valid_period = valid_period
        self.__applicable_to = applicable_to
    