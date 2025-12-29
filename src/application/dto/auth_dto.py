from dataclasses import dataclass

@dataclass
class RegisterDTO:
    username: str
    password: str
    email: str
    role: str


@dataclass
class LoginDTO:
    username: str
    password: str
