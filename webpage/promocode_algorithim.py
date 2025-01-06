from postmates_scraper import fetch_postmates_comments
from ubereats_scraper import fetch_uber_eats_comments

common = {"WORKED", "THANKS", "THANK", "POSTED", "POSTMATES", "UBEREATS",
        "HELLO", "THANKYOU", "WORKING", "PLEASE", "LOSANGELES", "LASVEGAS", 
        "PHOENIX", "ORANGE","VEGAS", "HOUSTON", "DALLAS", "AUSTIN", "COUNTY"
        , "ANGELES", "THANKU", "THANKYOU"}

def extract_promo_codes(temp):
    codes = []
    count = 0

    #trust me this hurts my eyes more than it does yours
    #im thinking about using an ML model to find codes instead
    for c in temp:
        isValid = True
        if count > 0:
            if temp[count - 1].isupper():  # Check the preceding character
                isValid = False
        if temp[count].isupper():
            if (count + 5) < len(temp):  # Ensure there are at least 5 characters ahead
                for i in range(1, 5):  # Check the next 4 characters for uppercase letters
                    if not temp[count + i].isupper():
                        isValid = False
            else:
                isValid = False
        else:
            isValid = False
        if isValid:
            currentCode = ""
            isCap = True
            index = 0
            while isCap:
                currentCode += temp[count + index]
                if (count + index + 1) < len(temp):
                    next_char = temp[count + index + 1]
                    if not (next_char.isupper() or next_char.isdigit()):  # Allow uppercase or digit
                        isCap = False
                index += 1
            if currentCode not in common:
                codes.append(currentCode)
        count += 1

    return codes

def retrieve_codes(source):
    # Fetch comments from both threads
    if source == "postmates":     
        postmates_comments = fetch_postmates_comments()
        postmates_codes = extract_promo_codes(postmates_comments)
        return postmates_codes

    elif source == "ubereats":
        ubereats_comments = fetch_uber_eats_comments()
        ubereats_codes = extract_promo_codes(ubereats_comments)
        return ubereats_codes


    # Extract promo codes
    


