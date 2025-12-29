from typing import List, Optional
from src.domain.models.blood_type import BloodType
from src.domain.repositories.blood_type_repository import BloodTypeRepository
from src.application.dto.blood_type_dto import (
    BloodTypeCreateDTO, 
    BloodTypeResponseDTO
)


class ManageBloodTypeUseCase:
    """Use case for managing blood types"""

    def __init__(self, repository: BloodTypeRepository):
        self.repository = repository

    def create_blood_type(self, dto: BloodTypeCreateDTO) -> BloodTypeResponseDTO:
        """Create a new blood type"""
        # Check if blood type already exists
        if self.repository.exists(dto.type_name):
            raise ValueError(f"Nhóm máu {dto.type_name} đã tồn tại")

        # Create domain entity
        blood_type = BloodType(type_name=dto.type_name)
        
        # Save to repository
        saved_blood_type = self.repository.create(blood_type)
        
        # Return response DTO
        return BloodTypeResponseDTO.from_entity(saved_blood_type)

    def get_blood_type_by_id(self, blood_type_id: int) -> Optional[BloodTypeResponseDTO]:
        """Get blood type by ID"""
        blood_type = self.repository.get_by_id(blood_type_id)
        if blood_type:
            return BloodTypeResponseDTO.from_entity(blood_type)
        return None

    def get_blood_type_by_name(self, type_name: str) -> Optional[BloodTypeResponseDTO]:
        """Get blood type by name"""
        blood_type = self.repository.get_by_name(type_name)
        if blood_type:
            return BloodTypeResponseDTO.from_entity(blood_type)
        return None

    def get_all_blood_types(self) -> List[BloodTypeResponseDTO]:
        """Get all blood types"""
        blood_types = self.repository.get_all()
        return [BloodTypeResponseDTO.from_entity(bt) for bt in blood_types]

    def update_blood_type(self, blood_type_id: int, dto: BloodTypeCreateDTO) -> BloodTypeResponseDTO:
        """Update blood type"""
        # Check if blood type exists
        existing = self.repository.get_by_id(blood_type_id)
        if not existing:
            raise ValueError(f"Không tìm thấy nhóm máu với ID {blood_type_id}")

        # Check if new name already exists (for different blood type)
        existing_with_name = self.repository.get_by_name(dto.type_name)
        if existing_with_name and existing_with_name.id != blood_type_id:
            raise ValueError(f"Nhóm máu {dto.type_name} đã tồn tại")

        # Update entity
        blood_type = BloodType(
            id=blood_type_id,
            type_name=dto.type_name
        )
        
        # Save to repository
        updated_blood_type = self.repository.update(blood_type)
        
        # Return response DTO
        return BloodTypeResponseDTO.from_entity(updated_blood_type)

    def delete_blood_type(self, blood_type_id: int) -> bool:
        """Delete blood type"""
        return self.repository.delete(blood_type_id)

    def initialize_blood_types(self) -> List[BloodTypeResponseDTO]:
        """Initialize all standard blood types if they don't exist"""
        standard_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
        created_types = []

        for type_name in standard_types:
            if not self.repository.exists(type_name):
                dto = BloodTypeCreateDTO(type_name=type_name)
                created = self.create_blood_type(dto)
                created_types.append(created)

        return created_types

