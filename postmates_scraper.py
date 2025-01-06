import praw
import requests
from bs4 import BeautifulSoup

# Initialize the PRAW client
reddit = praw.Reddit(
    client_id='Ccc1KfuiEgX1bOLvw1O9xg',  # Replace with your Client ID
    client_secret='ADmSS4D94J6uo-ICoDqj2H1dmNC08g', 
    user_agent='postmates scraper by anshlovescoffee',  # A descriptive user agent (e.g., "RedditScraperBot/0.1 by your_username")
)

url = "https://www.reddit.com/r/postmates/comments/1ggzmcs/monthly_existing_user_promo_code_thread/"
url2 = "https://forums.dansdeals.com/index.php?topic=133042.0;prev_next=prev#new"

    
def fetch_postmates_comments():
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)  #Expand "More Comments"
    comments = ""
    for comment in submission.comments.list():
        comments += comment.body + " "
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url2, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find_all("div", class_="inner")
    c = [comment.get_text(separator=" ").strip() for comment in body]
    comments += str(c)
    return comments

    
