from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import json
from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm.mapper import class_mapper

# Define the base class for SQLAlchemy models
Base = declarative_base()

@dataclass
class Coordinates(Base):
    __tablename__ = 'coordinates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

@dataclass
class Timezone(Base):
    __tablename__ = 'timezone'
    id = Column(Integer, primary_key=True, autoincrement=True)
    offset = Column(String, nullable=False)
    description = Column(String, nullable=False)

@dataclass
class Street(Base):
    __tablename__ = 'street'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

@dataclass
class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    street_id = Column(Integer, ForeignKey('street.id'))
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    coordinates_id = Column(Integer, ForeignKey('coordinates.id'))
    timezone_id = Column(Integer, ForeignKey('timezone.id'))

    street = relationship("Street")
    coordinates = relationship("Coordinates")
    timezone = relationship("Timezone")

@dataclass
class Name(Base):
    __tablename__ = 'name'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    first = Column(String, nullable=False)
    last = Column(String, nullable=False)

@dataclass
class Login(Base):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    md5 = Column(String, nullable=False)
    sha1 = Column(String, nullable=False)
    sha256 = Column(String, nullable=False)

@dataclass
class DOB(Base):
    __tablename__ = 'dob'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    age = Column(Integer, nullable=False)

@dataclass
class Registered(Base):
    __tablename__ = 'registered'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    age = Column(Integer, nullable=False)

@dataclass()
class SocialDetails(Base):
    __tablename__ = 'SocialDetails'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

@dataclass
class Picture(Base):
    __tablename__ = 'picture'
    id = Column(Integer, primary_key=True, autoincrement=True)
    large = Column(String, nullable=False)
    medium = Column(String, nullable=False)
    thumbnail = Column(String, nullable=False)

@dataclass
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(String, nullable=False)
    name_id = Column(Integer, ForeignKey('name.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    email = Column(String, nullable=False)
    login_id = Column(Integer, ForeignKey('login.id'))
    dob_id = Column(Integer, ForeignKey('dob.id'))
    registered_id = Column(Integer, ForeignKey('registered.id'))
    phone = Column(String, nullable=False)
    cell = Column(String, nullable=False)
    social_id_id = Column(Integer, ForeignKey('SocialDetails.id'))
    picture_id = Column(Integer, ForeignKey('picture.id'))
    nat = Column(String, nullable=False)

    name = relationship("Name")
    location = relationship("Location")
    login = relationship("Login")
    dob = relationship("DOB")
    registered = relationship("Registered")
    social_details = relationship("SocialDetails")
    picture = relationship("Picture")

def serialize_model(obj):
    """
    Custom serializer function for nested SQLAlchemy models.
    
    Args:
    obj: SQLAlchemy model instance to be serialized.
    
    Returns:
    A JSON-compatible dictionary representation of the given object.
    """
    # Return simple types directly
    if isinstance(obj, (int, float, str, bool)):
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

