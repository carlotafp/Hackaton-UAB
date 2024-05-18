

class User():

    def __init__(self, name, email, password, DNI):
        self._name = name
        self._email = email
        self._password = password
        self._DNI = DNI
        self._allergens = []
        self._minusvalid = False
        self._privileged = False
        self._traveling = False
        self._dislexic = False
        self._dog_allergy = False
    
    def add_allegen(self, allergen):
        self._allergens.append(allergen)
    
    def add_allergens(self, allerges):
        self._allergens.extend(allerges)
    
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name
    
    def get_allergens(self):
        return self._allergens
    
    def set_allegens(self, allergens):
        self._allergens = allergens

    def get_DNI(self):
        return self._DNI

    def set_DNI(self, DNI):
        self._DNI = DNI

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def get_minusvalid(self):
        return self._minusvalid

    def set_minusvalid(self, minusvalid):
        self._minusvalid = minusvalid

    def get_privileged(self):
        return self._privileged

    def set_privileged(self, privileged):
        self._privileged = privileged

    def get_traveling(self):
        return self._traveling

    def set_traveling(self, traveling):
        self._traveling = traveling
    
    def get_dislexic(self):
        return self._dislexic
    
    def set_dislexic(self, dislexic):
        self._dislexic = dislexic
    
    def get_dog_allergy(self):
        return self._dog_allergy
    
    def set_dog_allergy(self, dog_allergy):
        self._dog_allergy = dog_allergy
    

