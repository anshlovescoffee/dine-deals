import praw

# Initialize the PRAW client
reddit = praw.Reddit(
    client_id='Ccc1KfuiEgX1bOLvw1O9xg',  # Replace with your Client ID
    client_secret='ADmSS4D94J6uo-ICoDqj2H1dmNC08g', 
    user_agent='ubereats scraper by anshlovescoffee',  # A descriptive user agent (e.g., "RedditScraperBot/0.1 by your_username")
)

url = "https://www.reddit.com/r/UberEATS/comments/1hrqgh5/monthly_existing_user_promo_code_thread/"


def fetch_uber_eats_comments():
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)  #Expand "More Comments"
    comments = ""
    for comment in submission.comments.list():
        comments += comment.body + " "
    return comments
