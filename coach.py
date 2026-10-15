from class_User import User
from JSONDatabase import JsonDatabase
class Coach(User):
    datas_classes = JsonDatabase("classes.json")

    def __init__ (self,userName, name, password, email, is_active=True):
        super().__init__(userName, name, password, email, is_active=True)
        self.__assigned_classes =self.view_assigned_classes()
    # @staticmethod
    # @property
    # def get_assigned_classes(self):
        # return self
    def give_datas_classes (self):
        # answer = []
        try:
            for dc in self.__class__.datas_classes._load_all():
                if dc.get("coach") == self._userName:
                    answer.append(dc)
                    yield dc
        except FileNotFoundError("فایل مرد نظر پیدا نشد"):
            return {}
        finally:
            yield {}
        # if len(answer)>0:
    # @staticmethod
    # def login(self, input_user_name,input_password):
    #         canLog =True
    #         while self._userName== input_user_name and self._password == input_password:
    #             print("نام و یا نام کاربری اشتباه است")
    #             input_user_name = input("نام کاربری اتان را وارد کنید")
    #             input_password = input("رمز عبور اتان را وارد کنید")
    #         if self._is_active:
    #             canLog =False
    #             print("حساب شما غیر فعال هست در نتیجه شما نمی توانید وارد شوید")
    def view_assigned_classes(self) -> list:
        """
        """
        assigned_classes =[]
        while True:
            try:
                answer = self.give_datas_classes()
                print(answer)
                if not answer:
                    break
                assigned_classes.append(answer)
            finally:
                break
        if not assigned_classes:
            print("هیچ کلاسی به شما اختصاص داده نشده است.")
            return []
        self.__assigned_classes = assigned_classes
        return assigned_classes
    def assign_workout_plan(self, gym_class, member, exercises: list[Exercise]) -> bool:
        """
        بخش ۲.۲ مستند: مدیریت برنامه تمرینی
        الزامات امنیتی و منطقی:
        ۱. کلاس باید متعلق به همین مربی باشد.
        ۲. عضو باید در همین کلاس ثبت‌نام کرده باشد.
        ۳. لیست تمرینات نباید خالی باشد.
        """
        # شرط ۱: کنترل تعلق کلاس به همین مربی
        if gym_class not in self.assigned_classes:
            raise PermissionError("خطا: شما اجازه ثبت برنامه برای کلاسی که مربی آن نیستید را ندارید.")

        # شرط ۲: کنترل حضور عضو در کلاس مشخص‌شده
        if member not in gym_class.get("members"):
            raise ValueError(f"خطا: کاربر {member} در کلاس {gym_class.get(title)} عضویت ندارد.")

        if not exercises:
            raise ValueError("خطا: برنامه تمرینی باید حداقل شامل یک حرکت باشد.")

        # ثبت برنامه تمرینی در سابقه عضو
        workout_record = {
            "trainer_username": self._userName,
            "title": gym_class.get(title),
            "exercises": exercises
        }
        # member.workout_plans.append(workout_record)
        # print(f"برنامه تمرینی با موفقیت برای '{member.full_name}' ثبت شد.")
        # return True