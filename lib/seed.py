from faker import Faker
from models import Role, Audition, session
import random

faker = Faker()


def create_fake_roles(n):
    roles = []
    for _ in range(n):
        role = Role(character_name=faker.job())
        session.add(role)
        roles.append(role)
    session.commit()
    return roles


def create_fake_auditions(n, roles):
    for _ in range(n):
        audition = Audition(
            role=random.choice(roles),
            actor=faker.name(),
            date=faker.date_time_this_year()
        )
        session.add(audition)
    session.commit()


roles = create_fake_roles(5)
create_fake_auditions(20, roles)
