import cx_Oracle
import logging

logging.basicConfig(level=logging.DEBUG)

# Connect to the Oracle database
try:
    conn = cx_Oracle.connect('redis', '******', 'orcl11g-scan.*****.oraclevcn.com:1521/orcl11g******.oraclevcn.com')
    logging.debug("Successfully connected to the Oracle database")
except cx_Oracle.DatabaseError as e:
    logging.error(f"Error connecting to the Oracle database: {e}")
    exit(1)

# Create a new user
def create_user(user_id: int, name: str):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, name) VALUES (:user_id, :name)", user_id=user_id, name=name)
        conn.commit()
        logging.debug(f"Successfully inserted user with ID {user_id} and name {name}")
    except cx_Oracle.DatabaseError as e:
        logging.error(f"Error inserting user: {e}")
        conn.rollback()


# Read a user
def get_user(user_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE user_id = :user_id", user_id=user_id)
        name = cursor.fetchone()[0]
        logging.debug(f"Successfully retrieved user with ID {user_id}")
        return name
    except cx_Oracle.DatabaseError as e:
        logging.error(f"Error retrieving user: {e}")


# Update a user
def update_user(user_id: int, new_name: str):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = :new_name WHERE user_id = :user_id", new_name=new_name, user_id=user_id)
        conn.commit()
        logging.debug(f"Successfully updated user with ID {user_id} to have name {new_name}")
    except cx_Oracle.DatabaseError as e:
        logging.error(f"Error updating user: {e}")
        conn.rollback()


# Delete a user
def delete_user(user_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = :user_id", user_id=user_id)
        conn.commit()
        logging.debug(f"Successfully deleted user with ID {user_id}")
    except cx_Oracle.DatabaseError as e:
        logging.error(f"Error deleting user: {e}")
        conn.rollback()
