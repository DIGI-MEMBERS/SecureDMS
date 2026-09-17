from database.database import get_connection, initialize_database
from services.auth_service import hash_password


def seed_users():
    connection = get_connection()

    users = [
        ("admin", hash_password("Admin@123"), "admin"),
        ("investigator", hash_password("Investigator@123"), "investigator"),
        ("viewer", hash_password("Viewer@123"), "viewer")
    ]

    try:
        for username, password_hash, role in users:
            connection.execute(
                """
                INSERT OR IGNORE INTO users
                (username, password_hash, role)
                VALUES (?, ?, ?)
                """,
                (username, password_hash, role)
            )

        connection.commit()
        print("Demo users inserted successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    seed_users()
    print("Database seeding completed.")