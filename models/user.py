class User:
    def __init__(self, user_id, name, age, gender, address, phone, email, aadhar_number):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address
        self.phone = phone
        self.email = email
        self.aadhar_number = aadhar_number

    def __str__(self):
        return f"{self.name} ({self.email})"