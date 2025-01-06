from dotenv import load_dotenv
import os
import mysql.connector
from promocode_algorithim import retrieve_codes

load_dotenv()

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host= os.getenv("DATABASE_HOST"),  # MySQL server address
        user= os.getenv("DATABASE_USER"),       # MySQL username
        password= os.getenv("DATABASE_PASSWORD"),  # Replace with your MySQL root password
        database= os.getenv("DATABASE_NAME")    # Database name
    )

# Add a promo code to the database
def add_promo_code(db, code, origin):
    cursor = db.cursor()
    try:
        query = """
            INSERT IGNORE INTO PromoCodes (promocode, origin)
            VALUES (%s, %s);
        """
        cursor.execute(query, (code, origin))
        db.commit()
        if cursor.rowcount > 0:
            print(f"Code '{code}' from '{origin}' added successfully.")
        else:
            print(f"Code '{code}' from '{origin}' already exists.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()


# Scrape and update the database
def scrape_and_update():
    db = get_db_connection()

    # Fetch comments and extract promo codes

    postmates_codes = retrieve_codes("postmates")
    ubereats_codes = retrieve_codes("ubereats")

    # Add Postmates codes to the database
    for code in postmates_codes:
        print(code)
        add_promo_code(db, code, "Postmates")

    # Add UberEATS codes to the database
    for code in ubereats_codes:
        print(code)
        add_promo_code(db, code, "UberEATS")

    db.close()

def get_db_connection():
    return mysql.connector.connect(
        host= os.getenv("DATABASE_HOST"),  # MySQL server address
        user= os.getenv("DATABASE_USER"),       # MySQL username
        password= os.getenv("DATABASE_PASSWORD"),  # Replace with your MySQL root password
        database= os.getenv("DATABASE_NAME")    # Database name
    )

def like_promo_code(db, user_id, promocode_id):
    cursor = db.cursor()
    try:
        # Check if the user has already liked or disliked this promo code
        cursor.execute(
            "SELECT action FROM UserActivity WHERE user_id = %s AND promocode_id = %s",
            (user_id, promocode_id)
        )
        result = cursor.fetchone()

        if result:
            if result[0] == 'like':
                # User already liked this code; remove the like
                cursor.execute(
                    "DELETE FROM UserActivity WHERE user_id = %s AND promocode_id = %s",
                    (user_id, promocode_id)
                )
                cursor.execute(
                    "UPDATE PromoCodes SET likes = likes - 1 WHERE id = %s",
                    (promocode_id,)
                )
            elif result[0] == 'dislike':
                # User disliked this code; switch to like
                cursor.execute(
                    "UPDATE PromoCodes SET dislikes = dislikes - 1 WHERE id = %s",
                    (promocode_id,)
                )
                cursor.execute(
                    "UPDATE PromoCodes SET likes = likes + 1 WHERE id = %s",
                    (promocode_id,)
                )
                cursor.execute(
                    "UPDATE UserActivity SET action = 'like' WHERE user_id = %s AND promocode_id = %s",
                    (user_id, promocode_id)
                )
        else:
            # User has not interacted with this code; add a like
            cursor.execute(
                "INSERT INTO UserActivity (user_id, promocode_id, action) VALUES (%s, %s, 'like')",
                (user_id, promocode_id)
            )
            cursor.execute(
                "UPDATE PromoCodes SET likes = likes + 1 WHERE id = %s",
                (promocode_id,)
            )

        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()


def dislike_promo_code(db, user_id, promocode_id):
    cursor = db.cursor()
    try:
        # Check if the user has already liked or disliked this promo code
        cursor.execute(
            "SELECT action FROM UserActivity WHERE user_id = %s AND promocode_id = %s",
            (user_id, promocode_id)
        )
        result = cursor.fetchone()

        if result:
            if result[0] == 'dislike':
                # User already disliked this code; remove the dislike
                cursor.execute(
                    "DELETE FROM UserActivity WHERE user_id = %s AND promocode_id = %s",
                    (user_id, promocode_id)
                )
                cursor.execute(
                    "UPDATE PromoCodes SET dislikes = dislikes - 1 WHERE id = %s",
                    (promocode_id,)
                )
            elif result[0] == 'like':
                # User liked this code; switch to dislike
                cursor.execute(
                    "UPDATE PromoCodes SET likes = likes - 1 WHERE id = %s",
                    (promocode_id,)
                )
                cursor.execute(
                    "UPDATE PromoCodes SET dislikes = dislikes + 1 WHERE id = %s",
                    (promocode_id,)
                )
                cursor.execute(
                    "UPDATE UserActivity SET action = 'dislike' WHERE user_id = %s AND promocode_id = %s",
                    (user_id, promocode_id)
                )
        else:
            # User has not interacted with this code; add a dislike
            cursor.execute(
                "INSERT INTO UserActivity (user_id, promocode_id, action) VALUES (%s, %s, 'dislike')",
                (user_id, promocode_id)
            )
            cursor.execute(
                "UPDATE PromoCodes SET dislikes = dislikes + 1 WHERE id = %s",
                (promocode_id,)
            )

        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
