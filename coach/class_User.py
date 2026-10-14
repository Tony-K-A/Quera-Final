import re
import json
from JSONDatabase import JsonDatabase
class User:
    file_user = JsonDatabase()
    setUsername =file_user.get_all_a_val_key_set()
    def __init__(self, name, userName, password, email, role, is_active):
        self._userName = userName
        self._name = name
        self._password = password
        self._email = email
        self._role = role
        self._is_active = is_active
    @property
    def name(self) ->str:
        return self._name
    @property
    def userName(self) ->str:
        return self._userName
    @property
    def password(self) ->str:
        return self._password
    @property
    def email(self) ->str:
        return self._email
    @property
    def role(self) ->str:
        return self._role
    @property
    def is_active(self) ->bool:
        return self._is_active

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
    # @classmethod
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
            self._name = value
    # @classmethod
    @userName.setter
    def userName(self , value) :
        validateAnswer = self.validate_username(value)
        if validateAnswer:
            # if value in setUsername:
            while  value in self.__class__.setUsername:
                print("نام کاربری از قبل در پایگاه داده وجود دارد و از قبل استفاده شده است نام کاربری دیگری وارد کنید")
                value = input()
            self._userName = value
            self.__class__.setUsername.add(value)
    @password.setter
    def password(self , value):
        validateAnswer = self.validate_password(value)
        if validateAnswer:
            self._password = value
    @email.setter
    def email(self , value) :
        validateAnswer = self.validate_email(value)
        if validateAnswer:
            self._email = value
    @role.setter
    def role(self , value) :
        validateAnswer = self.validate_role(value)
        if validateAnswer:
            self._role = value
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