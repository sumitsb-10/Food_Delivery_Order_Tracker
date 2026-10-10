class Customer:
    def __init__(self, id, name, phone, address, created_at):
        self.id = id
        self.name = name
        self.phone = phone
        self.address = address
        self.created_at = created_at

    def __repr__(self):
        return (
            f"Customer("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"phone='{self.phone}', "
            f"address='{self.address}', "
            f"created_at='{self.created_at}')"
        )