from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User

users = [
    {
        "username": "user",
        "email": "user@stockflow.local",
        "role": "USER",
    },
    {
        "username": "viewer",
        "email": "viewer@stockflow.local",
        "role": "VIEWER",
    },
]


def main():
    db = SessionLocal()

    try:
        for data in users:
            existing = db.scalar(select(User).where(User.username == data["username"]))

            if existing:
                print(f"{data['username']} already exists")
                continue

            user = User(
                username=data["username"],
                avatar="",
                email=data["email"],
                password_hash=hash_password("TestPassword123!"),
                role=data["role"],
                is_active=True,
            )

            db.add(user)

        db.commit()
        print("Test users created.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
