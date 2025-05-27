from faker import Faker
from sqlalchemy.orm import Session
from db import SyncSessionLocal
from user.models import User, Preference, Address, Role, UserRole
import random

fake = Faker()

def create_roles(session):
    """Ensure predefined roles exist in the database."""
    role_names = ["Admin", "User", "Editor"]
    existing_roles = {role.name for role in session.query(Role).all()}

    for role_name in role_names:
        if role_name not in existing_roles:
            role = Role(name=role_name, slug=role_name.lower())
            session.add(role)
    
    session.commit()

def create_fake_user(session: Session):
    """Creates a fake user with related preferences, addresses, and assigns roles."""
    user = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
    )
    user.set_password("password123")  # Set a default password

    session.add(user)
    session.commit()  # Save user to get ID

    # Create a fake preference
    preference = Preference(
        language=random.choice(["en", "es", "fr", "de"]),
        currency_code=random.choice(["USD", "EUR", "GBP"]),
        user_id=user.id,
    )
    session.add(preference)

    # Create a few fake addresses
    for _ in range(random.randint(1, 3)):  
        address = Address(
            road_name=fake.street_name(),
            post_code=fake.postcode(),
            city=fake.city(),
            user_id=user.id,
        )
        session.add(address)

    # Assign random roles (1-2 per user)
    roles = session.query(Role).all()
    assigned_roles = random.sample(roles, k=random.randint(1, 2))  # Assign 1-2 roles
    
    for role in assigned_roles:
        user_role = UserRole(user_id=user.id, role_id=role.id)
        session.add(user_role)

    session.commit()

def seed_database(num_users=10):
    """Seed the database with fake users and roles."""
    session = SyncSessionLocal()

    # Ensure roles exist before assigning them
    create_roles(session)

    for _ in range(num_users):
        create_fake_user(session)

    session.close()
    print(f"Seeded {num_users} fake users with roles.")

if __name__ == "__main__":
    seed_database(10)  # Generate 10 fake users
