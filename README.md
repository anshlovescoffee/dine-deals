# DineDeals App

This is an open-source Flask application for scraping and displaying promo codes.

## Features

- Scrape promo codes from multiple sources.
- Allow users to like or dislike codes.
- View and interact with promo codes in real time.

## Installation

1. Clone the repository:
   ```bash
    git clone https://https://github.com/anshlovescoffee/dine-deals.git
    cd dine-deals-main

2. Create a virtual environment:
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies:
    pip install -r requirements.txt

4. Set up the database:
    Create a MySQL database named PromoCodeDB 
    THE DATABASE NAME IS CASE SENSITIVE 
    For more help visit: https://dev.mysql.com/doc/mysql-getting-started/en/

    Add the required tables:
   ```bash
   CREATE TABLE `PromoCodes` (
   `id` int NOT NULL AUTO_INCREMENT,
   `promocode` varchar(50) NOT NULL,
   `origin` enum('Postmates','UberEATS') NOT NULL,
   `likes` int DEFAULT '0',
   `dislikes` int DEFAULT '0',
   `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `promocode` (`promocode`,`origin`)
    ) ENGINE=InnoDB AUTO_INCREMENT=14296 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

    CREATE TABLE `UserActivity` (
    `id` int NOT NULL AUTO_INCREMENT,
    `user_id` varchar(255) NOT NULL,
    `promocode_id` int NOT NULL,
    `action` enum('like','dislike') NOT NULL,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_id` (`user_id`,`promocode_id`),
    UNIQUE KEY `unique_user_action` (`user_id`,`promocode_id`),
    KEY `promocode_id` (`promocode_id`),
    KEY `idx_user_promo` (`user_id`,`promocode_id`),
    CONSTRAINT `useractivity_ibfk_1` FOREIGN KEY (`promocode_id`) REFERENCES `PromoCodes` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

5. Create a .env file inside the webpage file.
Your .env file should look like this:

    FLASK_SECRET_KEY=your_secret_key
    DATABASE_USER=root
    DATABASE_PASSWORD=your_password 
    DATABASE_HOST=localhost
    DATABASE_NAME=PromoCodeDB 
    
    

6. Run the app:

    python3 webpage/app.py

    ## Contributing
    Contributions are welcome! Please fork the repository and submit a pull request.

    ## FAQ

    1. Why do I only see only a handful of entries in my database?

    The program is designed to track promo codes within a specific timeframe, focusing on those that have been posted within the past month. This approach ensures that the data remains relevant and up-to-date for users.

    If the program has not been running continuously or was recently started, it might not have had enough time to scrape and collect a significant number of entries. As a result, the database may contain only a handful of entries or even none, depending on when the program started and how frequently new codes are posted.

    To populate the database with more entries, ensure the program is running consistently over time. This allows it to periodically scrape and store promo codes as they become available.

    2. How often does the program scrape for new promo codes?
    The program runs a scraping routine every 2 minutes (or your defined interval) to fetch the latest promo codes. This frequency can be adjusted in the program configuration to meet specific needs.
    The scraping interval is defined in the time.sleep() function within the start_update_sequence method. To change it, modify the number of seconds in this line:

    time.sleep(120)  # Adjust this value for a new interval

    3. Can I add other platforms for promo code scraping?
    Yes, the program can be extended to support additional platforms. To add a new platform, a scraping function tailored to that platform’s structure must be implemented and integrated into the program.

    4. How are duplicate promo codes handled?
    The program uses a database query to check for existing promo codes before inserting new ones. If a promo code already exists, it is ignored to avoid duplication.

    6. Why can’t I like or dislike a promo code multiple times?
    To maintain fairness and prevent spam, each user is allowed to interact with a promo code (like or dislike) only once. The program identifies users using unique user_ids stored in cookies.

    7. How do I reset the database or clear all entries?

    ```bash
    TRUNCATE TABLE PromoCodes;
    TRUNCATE TABLE UserActivity;

    ## Be cautious, as this will delete ALL existing data permanently.

