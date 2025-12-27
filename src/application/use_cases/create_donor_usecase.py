from django.contrib.auth.models import User
from django.db import transaction
from src.domain.models.donor import Donor
from src.domain.repositories.donor_repository import DonorRepository
from src.domain.repositories.blood_type_repository import BloodTypeRepository
from src.application.dto.donor_dto import (
    DonorCreateDTO,
    DonorUpdateDTO,
    DonorResponseDTO
)


class CreateDonorUseCase:
    """Use case for donor registration"""

    def __init__(
        self, 
        donor_repository: DonorRepository,
        blood_type_repository: BloodTypeRepository
    ):
        self.donor_repository = donor_repository
        self.blood_type_repository = blood_type_repository

    @transaction.atomic
    def execute(self, dto: DonorCreateDTO) -> DonorResponseDTO:
        """Register a new donor with user account"""
        
        # Validate username
        if User.objects.filter(username=dto.username).exists():
            raise ValueError("Tên đăng nhập đã tồn tại")

        # Validate email
        if User.objects.filter(email=dto.email).exists():
            raise ValueError("Email đã được sử dụng")

        # Validate phone
        if self.donor_repository.exists_by_phone(dto.phone):
            raise ValueError("Số điện thoại đã được đăng ký")

        # Validate blood type if provided
        if dto.blood_type_id:
            blood_type = self.blood_type_repository.get_by_id(dto.blood_type_id)
            if not blood_type:
                raise ValueError("Nhóm máu không hợp lệ")

        # Create user account
        user = User.objects.create_user(
            username=dto.username,
            email=dto.email,
            password=dto.password
        )

        try:
            # Create donor entity
            donor = Donor(
                user_id=user.id,
                full_name=dto.full_name,
                gender=dto.gender,
                phone=dto.phone,
                date_of_birth=dto.date_of_birth,
                address=dto.address,
                blood_type_id=dto.blood_type_id
            )

            # Save donor
            saved_donor = self.donor_repository.create(donor)

            # Get blood type name if available
            blood_type_name = None
            if saved_donor.blood_type_id:
                blood_type = self.blood_type_repository.get_by_id(saved_donor.blood_type_id)
                if blood_type:
                    blood_type_name = blood_type.type_name

            # Return response
            return DonorResponseDTO.from_entity(saved_donor, user, blood_type_name)

        except Exception as e:
            # Rollback: delete user if donor creation fails
            user.delete()
            raise e

    def get_donor_by_id(self, donor_id: int) -> DonorResponseDTO:
        """Get donor by ID"""
        donor = self.donor_repository.get_by_id(donor_id)
        if not donor:
            raise ValueError("Không tìm thấy người hiến máu")

        user = User.objects.get(id=donor.user_id)
        
        blood_type_name = None
        if donor.blood_type_id:
            blood_type = self.blood_type_repository.get_by_id(donor.blood_type_id)
            if blood_type:
                blood_type_name = blood_type.type_name

        return DonorResponseDTO.from_entity(donor, user, blood_type_name)

    def get_donor_by_user_id(self, user_id: int) -> DonorResponseDTO:
        """Get donor by user ID"""
        donor = self.donor_repository.get_by_user_id(user_id)
        if not donor:
            raise ValueError("Không tìm thấy thông tin người hiến máu")

        user = User.objects.get(id=user_id)
        
        blood_type_name = None
        if donor.blood_type_id:
            blood_type = self.blood_type_repository.get_by_id(donor.blood_type_id)
            if blood_type:
                blood_type_name = blood_type.type_name

        return DonorResponseDTO.from_entity(donor, user, blood_type_name)

    @transaction.atomic
    def update_donor(self, donor_id: int, dto: DonorUpdateDTO) -> DonorResponseDTO:
        """Update donor information"""
        # Get existing donor
        existing_donor = self.donor_repository.get_by_id(donor_id)
        if not existing_donor:
            raise ValueError("Không tìm thấy người hiến máu")

        # Validate phone if changed
        if dto.phone and dto.phone != existing_donor.phone:
            if self.donor_repository.exists_by_phone(dto.phone):
                raise ValueError("Số điện thoại đã được đăng ký")

        # Validate blood type if provided
        if dto.blood_type_id:
            blood_type = self.blood_type_repository.get_by_id(dto.blood_type_id)
            if not blood_type:
                raise ValueError("Nhóm máu không hợp lệ")

        # Update donor entity
        updated_donor = Donor(
            id=donor_id,
            user_id=existing_donor.user_id,
            full_name=dto.full_name if dto.full_name else existing_donor.full_name,
            gender=dto.gender if dto.gender else existing_donor.gender,
            phone=dto.phone if dto.phone else existing_donor.phone,
            date_of_birth=dto.date_of_birth if dto.date_of_birth else existing_donor.date_of_birth,
            address=dto.address if dto.address is not None else existing_donor.address,
            blood_type_id=dto.blood_type_id if dto.blood_type_id is not None else existing_donor.blood_type_id
        )

        # Save updated donor
        saved_donor = self.donor_repository.update(updated_donor)

        # Get user and blood type info
        user = User.objects.get(id=saved_donor.user_id)
        
        blood_type_name = None
        if saved_donor.blood_type_id:
            blood_type = self.blood_type_repository.get_by_id(saved_donor.blood_type_id)
            if blood_type:
                blood_type_name = blood_type.type_name

        return DonorResponseDTO.from_entity(saved_donor, user, blood_type_name)

