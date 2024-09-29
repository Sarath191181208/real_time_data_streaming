import dataclasses
from dataclasses import dataclass
import json
from datetime import datetime
from decimal import Decimal

@dataclass
class Coordinates:
    latitude: float
    longitude: float

@dataclass
class Timezone:
    offset: str
    description: str

@dataclass
class Street:
    number: int
    name: str

@dataclass
class Location:
    street: Street
    city: str
    state: str
    country: str
    postcode: str
    coordinates: Coordinates
    timezone: Timezone

@dataclass
class Name:
    title: str
    first: str
    last: str

@dataclass
class Login:
    uuid: str
    username: str
    password: str
    salt: str
    md5: str
    sha1: str
    sha256: str

@dataclass
class DOB:
    date: datetime
    age: int

@dataclass
class Registered:
    date: datetime
    age: int

@dataclass
class ID:
    name: str
    value: str

@dataclass
class Picture:
    large: str
    medium: str
    thumbnail: str

@dataclass
class User:
    gender: str
    name: Name
    location: Location
    email: str
    login: Login
    dob: DOB
    registered: Registered
    phone: str
    cell: str
    id: ID
    picture: Picture
    nat: str

    def __dict__(self):
        return dataclasses.asdict(self)

class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.__dict__()
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Decimal):  
            return float(obj)  
        return json.JSONEncoder.default(self, obj)

# Example usage:
if __name__ == "__main__":
    # Create an example user object
    user = User(
        gender="male",
        name=Name(title="Mr", first="John", last="Doe"),
        location=Location(street=Street(10, "Mnt. St"), city="Anytown", state="CA", postcode="12345", country="USA", coordinates=Coordinates(latitude=37.7749, longitude=-122.4194), timezone=Timezone(offset="-8:00", description="Pacific Time Zone")),
        email="john.doe@example.com",
        login=Login(uuid="abcd1234", username="johndoe", password="password123", salt="salt",
                    md5="md5", sha1="sha1", sha256="sha256"),
        dob=DOB(date=datetime(1980, 1, 1), age=42),
        registered=Registered(date=datetime(2005, 1, 1), age=17),
        phone="555-1234",
        cell="555-5678",
        id=ID(name="SSN", value="123-45-6789"),
        picture=Picture(large="https://example.com/large.jpg", medium="https://example.com/medium.jpg",
                        thumbnail="https://example.com/thumbnail.jpg"),
        nat="US"
    )
    print(user)
    print("-"*20)

    # Serialize the User object with the custom encoder
    serialized_user = json.dumps(user, cls=UserEncoder, indent=4)
    print("Serialized User Object:")
    print(serialized_user)

    print(User(**json.loads(serialized_user)))