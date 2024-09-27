from dataclasses import dataclass
from typing import List, Dict

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
    date: str
    age: int

@dataclass
class Registered:
    date: str
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
