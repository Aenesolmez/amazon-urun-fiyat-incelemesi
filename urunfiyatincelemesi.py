import requests
from bs4 import BeautifulSoup
import time
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SENDER_EMAIL = 'göndericininmaili@example.com'
SENDER_PASSWORD = 'güvenlikkodu'
RECEIVER_EMAIL = 'alıcımaili@example.com'


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


PRODUCT_URL = 'ürün sitesinin linki'

HEADERS = {"User-Agent": "cihazınızın bilgileri"}

CHECK_INTERVAL_SECONDS = 60 * 10 


last_known_price = None

def send_email_notification(subject: str, body: str) -> None:
    """
    Sends an email notification with the given subject and body.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        print(f"Email successfully sent: '{subject}'")
    except Exception as e:
        print(f"Error sending email: {e}")
        print("Please check your email settings (address, password, SMTP server/port).")
        print("If you're using Gmail, you might need to generate an 'App Password'.")

def get_product_details(url: str, headers: dict) -> tuple[str, int | None]:
    """
    Fetches product name and price from the given URL.

    Args:
        url (str): The URL of the product page.
        headers (dict): HTTP headers to use for the request.

    Returns:
        tuple[str, int | None]: A tuple containing the product name and its price as an integer,
                                or None if the price cannot be extracted.
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL: {e}")
        return "Product Name Not Found", None

    soup = BeautifulSoup(response.content, 'html.parser')


    product_name_element = soup.find(id='productTitle') #buraya ürününüzün isminin id'sini girin
    product_name = product_name_element.get_text().strip() if product_name_element else "Product Name Not Found"


    price_element = soup.find('span', class_='a-offscreen')
    current_price = None
    if price_element:
        price_str = price_element.get_text().strip()

        numeric_part_match = re.search(r'(\d[\d\.,]*)', price_str)
        if numeric_part_match:
            raw_price_str = numeric_part_match.group(1)

            cleaned_price_str = raw_price_str.replace('.', '').replace(',', '.')
            try:

                current_price = int(float(cleaned_price_str))
            except ValueError:
                print(f"Warning: Could not convert price '{cleaned_price_str}' to a number.")
        else:
            print(f"Warning: Could not extract numeric value from price text: {price_str}")
    else:
        print("Warning: Product price element not found on the page.")

    return product_name, current_price

def check_product_price() -> None:
    """
    Checks the product price, compares it to the last known price,
    and sends an email notification if the price changes or if it's the first check.
    """
    global last_known_price

    product_name, current_price = get_product_details(PRODUCT_URL, HEADERS)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')

    if current_price is not None:
        if last_known_price is None:

            subject = f"AMAZON PRICE TRACKING STARTED: {product_name}"
            body = f"""
Hello,

Price tracking for "{product_name}" has started.
Initial price detected: {current_price} TL

Product link: {PRODUCT_URL}

Check Time: {current_time}
"""
            print(f"[{current_time}] Price tracking started. Current price for {product_name} is {current_price} TL.")
            send_email_notification(subject, body)
        elif current_price != last_known_price:

            subject = f"AMAZON PRICE CHANGE: {product_name}"
            
            if current_price < last_known_price:
                price_status = "PRICE DECREASED!"
                body = f"""
Hello,

The price for "{product_name}" has changed!
New price: {current_price} TL
Old price: {last_known_price} TL
{price_status}

Product link: {PRODUCT_URL}

Check Time: {current_time}
"""
            else:
                price_status = "PRICE INCREASED!"
                body = f"""
Hello,

The price for "{product_name}" has changed!
New price: {current_price} TL
Old price: {last_known_price} TL
{price_status}

Product link: {PRODUCT_URL}

Check Time: {current_time}
"""
            print(f"--- PRICE CHANGE ({current_time}) ---")
            print(f"{product_name}: New price **{current_price} TL** (was {last_known_price} TL).")
            print(price_status)
            print("------------------------------------------")
            
            send_email_notification(subject, body)
        else:

            print(f"[{current_time}] {product_name}: Price remains {current_price} TL.")
        

    else:
        print(f"[{current_time}] Could not retrieve price information for {product_name}.")


if __name__ == "__main__":
    print("Starting Amazon price tracker...")
    while True:
        check_product_price()
        print(f"Waiting for {CHECK_INTERVAL_SECONDS} seconds before next check...")
        time.sleep(CHECK_INTERVAL_SECONDS)