import re
import json
class User:
    def __init__(self, name, userName, password, email, role, is_active):
        self.__userName = userName
        self.__name = name
        self.__password = password
        self.__email = email
        self.__role = role
        self.__is_active = is_active
    @property
    def name(self) ->str:
        return self.__name
    @property
    def userName(self) ->str:
        return self.__userName
    @property
    def password(self) ->str:
        return self.__password
    @property
    def email(self) ->str:
        return self.__email
    @property
    def role(self) ->str:
        return self.__role
    @property
    def is_active(self) ->bool:
        return self.__is_active

    @staticmethod
    def validate_name(name):
        try:
            if not re.match(r"^[a-zA-Z\u0600-\u06FF\s]{2,50}$", name.strip()):
                raise ValueError("نام وارد شده معتبر نیست.")
            # return name.strip()
            return True
        except ValueError as e:
            print(f"خطا: {e}")
            return False

    @staticmethod
    def validate_username(username):
        try:
            if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]{2,19}$", username.strip()):
                raise ValueError("نام کاربری معتبر نیست.")
            # return username.strip()
            return True
        except ValueError as e:
            print(f"خطا: {e}")
            return False

    @staticmethod
    def validate_password(password):
        try:
            # حداقل یک حرف انگلیسی، یک رقم و یکی از کاراکترهای @ یا &
            pattern = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@&]).{6,}$"
            if not re.match(pattern, password):
                raise ValueError("رمز عبور باید حداقل شامل یک حرف انگلیسی، یک رقم و یکی از نمادهای @ یا & باشد.")
            # return password
            return True
        except ValueError as e:
            print(f"خطا: {e}")
            return False

    @staticmethod
    def validate_email(email):
        try:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(pattern, email.strip()):
                raise ValueError("ایمیل وارد شده معتبر نیست.")
            # return email.strip()
            return True
        except ValueError as e:
            print(f"خطا: {e}")
            return False

    @staticmethod
    def validate_role(role):
        try:
            valid_roles = {"manager", "coach", "gym_member"}
            if role.lower() not in valid_roles:
                raise ValueError(f"نقش نامعتبر است. نقش‌های مجاز: {valid_roles}")
            # return role.lower()
            return True
        except ValueError as e:
            print(f"خطا: {e}")
            return False

    @staticmethod
    def validate_is_active(is_active):
        try:
            if not isinstance(is_active, bool):
                raise TypeError("وضعیت کاربر (is_active) باید یک مقدار بولی (True/False) باشد.")
            # return is_active
            return True
        except ValueError as e:
            print(f"خطا: {e}")
            return False

    @name.setter
    def name(self, value) :
        validateAnswer = self.validate_name(value)
        if validateAnswer:
            self.__name = value
    @userName.setter
    def userName(self , value) :
        validateAnswer = self.validate_username(value)
        if validateAnswer:
            self.__userName = value
    @password.setter
    def password(self , value) :
        validateAnswer = self.validate_password(value)
        if validateAnswer:
            self.__password = value
    @email.setter
    def email(self , value) :
        validateAnswer = self.validate_email(value)
        if validateAnswer:
            self.__email = value
    @role.setter
    def role(self , value) :
        validateAnswer = self.validate_role(value)
        if validateAnswer:
            self.__role = value
    @is_active.setter
    def is_active(self , value) :
        validateAnswer = self.validate_is_active(value)
        if validateAnswer:
            self.__is_active = value

    @name.deleter
    def name(self, value) :
        pass
    @userName.deleter
    def userName(self , value) :
        pass
    @password.deleter
    def password(self , value) :
        pass
    @email.deleter
    def email(self , value) :
        pass
    @role.deleter
    def role(self , value) :
        pass
    @is_active.deleter
    def is_active(self , value) :
        pass
     
    @staticmethod
    def show_panel():
        pass