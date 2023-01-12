import cx_Oracle
import redis
import json
import logging

logging.basicConfig(level=logging.DEBUG)

# Connect to the Oracle database
try:
    conn = cx_Oracle.connect('redis', '****', 'orcl11g****.oraclevcn.com:1521/orcl11g****.oraclevcn.com')
    logging.debug("Successfully connected to the Oracle database")
except cx_Oracle.DatabaseError as e:
    logging.error(f"Error connecting to the Oracle database: {e}")
    exit(1)

# Connect to the Redis cache
try:
    cache = redis.Redis(host='127.0.0.1',password="******",port=6379)
    logging.debug("Successfully connected to the Redis cache")
except redis.ConnectionError as e:
    logging.error(f"Error connecting to the Redis cache: {e}")
    exit(1)

# Create a new user
def create_user(user_id: int, name: str):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, name) VALUES (:user_id, :name)", user_id=user_id, name=name)
        conn.commit()
        logging.debug(f"Successfully inserted user with ID {user_id} and name {name}")
        # Cache the user in Redis
        cache.set(user_id, json.dumps({'user_id': user_id, 'name': name}))
        logging.debug(f"Successfully cached user with ID {user_id}")
    except cx_Oracle.DatabaseError as e:
        logging.error(f"Error inserting user: {e}")
        conn.rollback()

    # Read a user
def get_user(user_id: int):
    try:
        # Check the cache first
        user_cache = cache.get(user_id)
        if user_cache:
            user = json.loads(user_cache)
            logging.debug(f"Successfully retrieved user with ID {user_id} from cache")
            return user
        else:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name FROM users WHERE user_id = :user_id", user_id=user_id)
            user = cursor.fetchone()
            logging.debug(f"Successfully retrieved user with ID {user_id} from database")
            # Cache the user in Redis
            #cache.set(user_id, json.dumps(user))
            #logging.debug(f"Successfully cached user with ID {user_id}")
            #return user
    except cx_Oracle.DatabaseError as e:
        logging.error(f"Error retrieving user: {e}")
