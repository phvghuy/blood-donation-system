class BloodRequest:
    def __init__(self, id, hospital_name, blood_type_name, quantity, status, request_date):
        self.id = id
        self.hospital_name = hospital_name
        self.blood_type_name = blood_type_name
        self.quantity = quantity
        self.status = status
        self.request_date = request_date