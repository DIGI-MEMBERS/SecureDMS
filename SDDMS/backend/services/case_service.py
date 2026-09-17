from database.database import get_connection


def create_case(case_number, title, description, investigator_id):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO cases
            (case_number, title, description, investigator_id, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                case_number,
                title,
                description,
                investigator_id,
                "open"
            )
        )

        connection.commit()

        case_id = cursor.lastrowid

        case = connection.execute(
            """
            SELECT
                id,
                case_number,
                title,
                description,
                investigator_id,
                status,
                created_at,
                updated_at
            FROM cases
            WHERE id = ?
            """,
            (case_id,)
        ).fetchone()

        return case

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_cases(user_id, role):
    connection = get_connection()

    try:

        if role == "admin":
            cases = connection.execute(
                """
                SELECT
                    id,
                    case_number,
                    title,
                    description,
                    investigator_id,
                    status,
                    created_at,
                    updated_at
                FROM cases
                ORDER BY id DESC
                """
            ).fetchall()

        else:
            cases = connection.execute(
                """
                SELECT
                    id,
                    case_number,
                    title,
                    description,
                    investigator_id,
                    status,
                    created_at,
                    updated_at
                FROM cases
                WHERE investigator_id = ?
                ORDER BY id DESC
                """,
                (user_id,)
            ).fetchall()

        return cases

    finally:
        connection.close()