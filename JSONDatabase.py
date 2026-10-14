import json
import os

class JsonDatabase:
    def __init__(self, filepath="users.json"):
        self.filepath = filepath
        self._ensure_file_exists()
    def _ensure_file_exists(self):
        """اگر فایل وجود نداشت، یک لیست خالی داخل آن می‌سازد."""
        if not os.path.exists(self.filepath):
            self._save_all([])

    def _load_all(self) -> list:
        """خواندن کل داده‌ها از فایل"""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_all(self, data: list):
        """ذخیره کل داده‌ها در فایل با فرمت خوانا"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ------------------ CREATE / INSERT ------------------
    def insert(self, new_record: dict, unique_key: str = None) -> bool:
      records = self._load_all()
      if unique_key:
          val = new_record.get(unique_key)
          if val is not None and any(r.get(unique_key) == val for r in records):
              return False
      records.append(new_record)
      self._save_all(records)
      return True

    # ------------------ READ / SELECT / SEARCH ------------------
    def select_all(self) -> list:
        """دریافت تمام دیکشنری‌ها"""
        return self._load_all()

    def search_by(self, key: str, value) -> list:
        """
        یافتن تمام رکوردهایی که مقدار یک کلید خاص آنها برابر value است.
        مثال: تمام کاربرانی که active_status آنها True است.
        """
        records = self._load_all()
        return [r for r in records if r.get(key) == value]

    def find_one(self, key: str, value):
        """یافتن اولین رکوردی که با شرط همخوانی دارد (مثلاً برای username یکتا)"""
        records = self._load_all()
        for r in records:
            if r.get(key) == value:
                return r
        return None

    def get_field_where(self, filter_key: str, filter_val, target_key: str):
        """
        اگر مقدار filter_key برابر filter_val بود، مقدار target_key را بدهد.
        مثال: نام کاربری بده، ایمیلش را بگیر.
        """
        records = self._load_all()
        results = []
        for r in records:
            if r.get(filter_key) == filter_val:
                # اگر کلید هدف وجود داشت، برمی‌گرداند (یا None در صورت نبود)
                results.append(r.get(target_key))
        return results
    def get_all_a_val_key_set(self,val_key="username"):
        answer=set()
        records = self._load_all()
        for r in records:
            try:
                key_val=r.get(val_key)
                if key_val != None:
                    answer.add(key_val)
            except:
                continue
        return answer

    # ------------------ UPDATE ------------------
    def update(self, filter_key: str, filter_val, update_data: dict) -> int:
        """
        بروزرسانی رکوردهایی که با شرط همخوانی دارند.
        update_data یک دیکشنری از فیلدهایی است که باید تغییر کنند یا اضافه شوند.
        """
        records = self._load_all()
        updated_count = 0

        for r in records:
            if r.get(filter_key) == filter_val:
                r.update(update_data)  # کلیدهای جدید یا تغییر یافته را با متود بروزرسانی خود کتابخانه هااعمال می‌کند
                updated_count += 1

        if updated_count > 0:
            self._save_all(records)
        return updated_count

    # ------------------ DELETE ------------------
    def delete(self, filter_key: str, filter_val) -> int:
        """حذف رکورد(هایی) که مقدار مشخصی دارند"""
        records = self._load_all()
        initial_len = len(records)
        
        # نگه‌داشتن آیتم‌هایی که شرط را ندارند
        filtered_records = [r for r in records if r.get(filter_key) != filter_val]
        
        deleted_count = initial_len - len(filtered_records)
        if deleted_count > 0:
            self._save_all(filtered_records)
        return deleted_count