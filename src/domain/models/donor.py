from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime
import re


@dataclass
class Donor:
    """Domain entity for Donor"""
    full_name: str
    gender: str
    phone: str
    user_id: int
    blood_type_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self):
        """Validate donor data"""
        # Validate full name
        if not self.full_name or not self.full_name.strip():
            raise ValueError("Họ tên không được để trống")
        
        if len(self.full_name) < 2 or len(self.full_name) > 100:
            raise ValueError("Họ tên phải từ 2 đến 100 ký tự")

        # Validate gender
        valid_genders = ['male', 'female', 'other']
        if self.gender not in valid_genders:
            raise ValueError(f"Giới tính không hợp lệ. Phải là một trong: {', '.join(valid_genders)}")

        # Validate phone
        if not self.phone or not self.phone.strip():
            raise ValueError("Số điện thoại không được để trống")
        
        # Vietnamese phone number validation (10-11 digits, starts with 0)
        phone_pattern = r'^0\d{9,10}$'
        if not re.match(phone_pattern, self.phone):
            raise ValueError("Số điện thoại không hợp lệ. Định dạng: 0XXXXXXXXX (10-11 số)")

        # Validate date of birth
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            
            if age < 18:
                raise ValueError("Người hiến máu phải từ 18 tuổi trở lên")
            
            if age > 65:
                raise ValueError("Người hiến máu phải dưới 65 tuổi")

        # Validate user_id
        if not self.user_id or self.user_id <= 0:
            raise ValueError("User ID không hợp lệ")

    def get_age(self) -> Optional[int]:
        """Calculate age from date of birth"""
        if not self.date_of_birth:
            return None
        
        today = date.today()
        age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        return age

    def __str__(self):
        return self.full_name

