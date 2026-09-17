from database.database import get_connection


# ==========================================
# CREATE AUDIT LOG
# ==========================================
def log_action(
    user_id,
    action,
    resource_type,
    resource_id=None,
    description=None,
    ip_address=None
):
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO audit_logs
            (
                user_id,
                action,
                resource_type,
                resource_id,
                description,
                ip_address
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                action,
                resource_type,
                resource_id,
                description,
                ip_address
            )
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# GET AUDIT LOGS
# ==========================================
def get_audit_logs(user_id, role):
    connection = get_connection()

    try:

        if role == "admin":
            logs = connection.execute(
                """
                SELECT
                    a.id,
                    a.user_id,
                    u.username,
                    a.action,
                    a.resource_type,
                    a.resource_id,
                    a.description,
                    a.ip_address,
                    a.created_at
                FROM audit_logs a
                LEFT JOIN users u
                    ON a.user_id = u.id
                ORDER BY a.id DESC
                """
            ).fetchall()

        else:
            logs = connection.execute(
                """
                SELECT
                    a.id,
                    a.user_id,
                    u.username,
                    a.action,
                    a.resource_type,
                    a.resource_id,
                    a.description,
                    a.ip_address,
                    a.created_at
                FROM audit_logs a
                LEFT JOIN users u
                    ON a.user_id = u.id
                WHERE a.user_id = ?
                ORDER BY a.id DESC
                """,
                (user_id,)
            ).fetchall()

        return logs

    finally:
        connection.close()