from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class BloodType:
    """Domain entity for blood type"""
    type_name: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self):
        """Validate blood type data"""
        if not self.type_name:
            raise ValueError("Tên nhóm máu không được để trống")
        
        valid_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
        if self.type_name not in valid_types:
            raise ValueError(f"Nhóm máu không hợp lệ. Phải là một trong: {', '.join(valid_types)}")

    def __str__(self):
        return self.type_name

