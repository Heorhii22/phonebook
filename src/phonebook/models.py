class Contact:
    def __init__(self, name: str, phone: str) -> None:
        if not name.strip():
            raise ValueError("Name can not be empty")
        elif not phone.isdigit():
            raise ValueError("Phone should contain only numbers")
        
        self.name = name
        self.phone = phone


    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "phone": self.phone}


    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Contact":
        if "name" not in data or "phone" not in data:
            raise ValueError("Object must contain name and phone keys")
        return cls(name=str(data["name"]), phone=str(data["phone"]))