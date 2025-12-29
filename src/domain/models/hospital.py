class Hospital:
    def __init__(self, id: int, user_id: int, name: str, phone: str, address: str, username: str = None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.address = address
        self.username = username