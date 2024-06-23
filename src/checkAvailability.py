import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

jerry_seinfeld_url = "https://marketplace.ticketek.com.au/purchase/searchlist/products?content_id=SEINFELD24"
benson_boone_url = (
    "https://marketplace.ticketek.com.au/purchase/searchlist?keyword=benson%20boone"
)


def check_ticket_availability(url):
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    # Add headless mode
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Specify the path to the Chrome binary (if needed)
    options.binary_location = (
        "/Applications/Google Chrome 2/Contents/MacOS/Google Chrome"
    )

    # Set up the ChromeDriver service
    service = Service(
        "/Users/jezzahonga/Desktop/projects/chromedriver-mac-arm64/chromedriver"
    )

    # Initialize the Chrome WebDriver with the service
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the URL
    driver.get(url)

    # Wait for the main content to load (adjust timeout as needed)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "main")))

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    no_tickets = soup.find_all("div", class_="search-list-item none-available")
    available_tickets = soup.find_all(
        "div", class_="search-list-item product-list-item"
    )

    driver.quit()

    if available_tickets and not no_tickets:
        return True
    else:
        return False


def send_email_alert():
    msg = MIMEText("Tickets are now available!")
    msg["Subject"] = "Ticket Alert"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = "recipient_email@example.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email@gmail.com", process.env.GMAIL_PASSWORD)
        server.send_message(msg)


if __name__ == "__main__":
    url = jerry_seinfeld_url  # or benson_boone_url
    available = check_ticket_availability(url)
    if available:
        send_email_alert()
        print("Tickets are available!")
    else:
        print("Tickets are not available.")
