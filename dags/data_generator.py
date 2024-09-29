from datetime import datetime
from faker import Faker
import random
import json

from data.user import User, UserEncoder

# Initialize Faker object
fake = Faker()


def generate_fake_user() -> User:
    gender = random.choice(["male", "female"])

    bday = fake.iso8601()
    age = datetime.now().year - int(bday.split("-")[0])

    reg_date = fake.date_time_this_decade()
    reg_age = datetime.now().year - reg_date.year

    user_data = {
        "gender": gender,
        "name": {
            "title": "Mr" if gender == "male" else "Ms",
            "first": (
                fake.first_name_male() if gender == "male" else fake.first_name_female()
            ),
            "last": fake.last_name(),
        },
        "location": {
            "street": {"number": fake.building_number(), "name": fake.street_name()},
            "city": fake.city(),
            "state": fake.state(),
            "country": fake.country(),
            "postcode": fake.postcode(),
            "coordinates": {"latitude": fake.latitude(), "longitude": fake.longitude()},
            "timezone": {"offset": fake.timezone(), "description": fake.city_suffix()},
        },
        "email": fake.email(),
        "login": {
            "uuid": fake.uuid4(),
            "username": fake.user_name(),
            "password": fake.password(),
            "salt": fake.password(length=8),
            "md5": fake.md5(),
            "sha1": fake.sha1(),
            "sha256": fake.sha256(),
        },
        "dob": {
            "date": bday,
            "age": age,
        },
        "registered": {"date": reg_date, "age": reg_age},
        "phone": fake.phone_number(),
        "cell": fake.phone_number(),
        "id": {"name": "INSEE", "value": fake.ssn()},
        "picture": {
            "large": fake.image_url(),
            "medium": fake.image_url(),
            "thumbnail": fake.image_url(),
        },
        "nat": fake.country_code(representation="alpha-2"),
    }

    return User(**user_data)


if __name__ == "__main__":
    # Generate a fake user
    fake_user = generate_fake_user()

    # Print the generated user data
    data = json.loads(json.dumps(fake_user, cls=UserEncoder, indent=4))
    print(data)

    # print the type 
    print(type(data))
    
    __import__('pprint').pprint(User(**data))
