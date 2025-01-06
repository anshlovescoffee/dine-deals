from flask import Flask, render_template, redirect, url_for, request, make_response
from threading import Thread
from db_logic import scrape_and_update
from like_logic import like_blueprint
from dislike_logic import dislike_blueprint
import mysql.connector
from dotenv import load_dotenv
import os
import time
import uuid

load_dotenv()

# Create a Flask application
app = Flask(__name__)
app.register_blueprint(like_blueprint)
app.register_blueprint(dislike_blueprint)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Function to get promo codes from the database
def fetch_promo_codes(user_id):
    try:
        db = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),  # MySQL server address
            user=os.getenv("DATABASE_USER"),  # MySQL username
            password=os.getenv("DATABASE_PASSWORD"),  # Replace with your MySQL root password
            database=os.getenv("DATABASE_NAME")  # Database name
        )
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT 
                p.id, 
                p.promocode, 
                p.origin, 
                p.likes, 
                p.dislikes, 
                p.created_at,
                ua.action AS user_action
            FROM PromoCodes p
            LEFT JOIN UserActivity ua 
            ON p.id = ua.promocode_id AND ua.user_id = %s
            ORDER BY p.created_at DESC
        """
        cursor.execute(query, (user_id,))
        promo_codes = cursor.fetchall()
        cursor.close()
        db.close()
        return promo_codes
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return []

# Function to run the update sequence in the background
def start_update_sequence():
    while True:
        print("Scraping and updating database...")
        scrape_and_update()
        print("Update complete. Waiting for 2 minutes...")
        time.sleep(120)  # Run every 2 minutes

# Start the background scraper thread when the app starts
def start_background_tasks():
    update_thread = Thread(target=start_update_sequence)
    update_thread.daemon = True  # Ensure the thread exits when the main program stops
    update_thread.start()

# Route for the home page
@app.route('/')
def home():
    # Check if the user has a unique identifier in cookies
    user_id = request.cookies.get('user_id')
    if not user_id:
        # Generate a new unique identifier
        user_id = str(uuid.uuid4())
        print(f"Generated new user_id: {user_id}")

    # Fetch promo codes from the database
    promo_codes = fetch_promo_codes(user_id)
    
    # Set the user_id as a cookie
    response = make_response(render_template('index.html', promo_codes=promo_codes))
    response.set_cookie('user_id', user_id, max_age=60*60*24*365)  # Cookie expires in 1 year
    return response

# Start background tasks when the app module is loaded
start_background_tasks()
