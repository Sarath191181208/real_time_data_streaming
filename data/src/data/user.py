from typing import dataclasses
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

import json

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

    def json(self) -> dict:
        return obj

    # If Decimal return float 
    if isinstance(obj, Decimal):
        return float(obj)

    # Handle datetime serialization
    if isinstance(obj, datetime):
        return obj.isoformat()

    # If it's a list of SQLAlchemy models, serialize each item
    if isinstance(obj, list):
        return [serialize_model(item) for item in obj]

    # Check if the object is a SQLAlchemy model instance
    if isinstance(obj.__class__, type(Base)) and hasattr(obj, '__table__'):
        serialized_data = {}

        # Iterate through each column and serialize its value
        for column in class_mapper(obj.__class__).columns:
            value = getattr(obj, column.key)
            serialized_data[column.key] = serialize_model(value)

        # Handle relationships
        for relationship in class_mapper(obj.__class__).relationships:
            value = getattr(obj, relationship.key)

            # Avoid circular references by excluding backrefs
            if value is not None:
                if relationship.uselist:
                    serialized_data[relationship.key] = [serialize_model(item) for item in value]
                else:
                    serialized_data[relationship.key] = serialize_model(value)

        return serialized_data

    # If it's not a recognized type, return its string representation
    return str(obj)


class UserEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for nested SQLAlchemy models.
    """
    def default(self, o):
        try:
            # Use the custom serialize_model function to encode
            return serialize_model(o)
        except TypeError:
            # Fallback to the default encoding if type is not supported
            return super().default(o)


# Example of how to initialize the database and add a user
if __name__ == "__main__":
    # Create an SQLite database in memory
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # Create a new session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create example data
    street = Street(number=10, name="Mnt. St")
    coordinates = Coordinates(latitude=37.7749, longitude=-122.4194)
    timezone = Timezone(offset="-8:00", description="Pacific Time Zone")
    location = Location(street=street, city="Anytown", state="CA", country="USA", postcode="12345", coordinates=coordinates, timezone=timezone)
    name = Name(title="Mr", first="John", last="Doe")
    login = Login(uuid="abcd1234", username="johndoe", password="password123", salt="salt", md5="md5", sha1="sha1", sha256="sha256")
    dob = DOB(date=datetime(1980, 1, 1), age=42)
    registered = Registered(date=datetime(2005, 1, 1), age=17)
    id_info = SocialDetails(name="SSN", value="123-45-6789")
    picture = Picture(large="https://example.com/large.jpg", medium="https://example.com/medium.jpg", thumbnail="https://example.com/thumbnail.jpg")
    user = User(gender="male", name=name, location=location, email="john.doe@example.com", login=login, dob=dob, registered=registered, phone="555-1234", cell="555-5678", social_details=id_info, picture=picture, nat="US")

    # Add and commit the user to the database
    session.add(user)
    session.commit()

    # Query and print the user
    print("--"*10, "QUERY RES", "--"*10)
    print(session.query(User).first())
    print("---"*17)

    serialized_user = json.dumps(user, cls=UserEncoder, indent=4)
    print("Serialized User Object:")
    print(serialized_user)

    # print the decoded user 
    print(User(**json.loads(serialized_user)))

