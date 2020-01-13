import re




class Register_Validation():
    
    def __init__(self, user_data):
        self.name = user_data["name"]
        self.country = user_data["country"]
        self.password = user_data["password"]
        self.email = user_data["email"]
        self.thumbnail = user_data["thumbnail"]
        self.role = user_data["role"]

    def check_input(self):
        if not (self.name and self.country and self.password and self.email and self.thumbnail and self.role):
            return [400, "Make sure you fill all the required fields"]
        elif (not isinstance(self.name, str) or not isinstance(self.password, str) or not isinstance(self.email, str) or not isinstance(self.email, str) or not isinstance(self.thumbnail, str) or not isinstance(self.role, str)):
            return [406, "Make sure to use alphabetical characters use only "]
        elif self.password.isspace() or len(self.password) < 4:
            return [406, "Make sure your password has atlest 4 letters"]
        elif not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.email) is not None:
            return [406, "Please enter a valid Email."]
        return [200, "All Good"]

        #  elif re.search('[0-9]', self.password) is None:
        #     return [406, "Make sure your password has a number in it"]
        # elif re.search('[A-Z]', self.password) is None:
        #     return [406, "Make sure your password has a capital letter in it"]


       