import os
from bs4 import BeautifulSoup
import requests
import smtplib

# Access variables
url = os.getenv("URL")
header = {"User-Agent": os.getenv("HEADER")}
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
recipient_email = os.getenv("RECIPIENT_EMAIL")

# Check if all required variables are present
if url and header and sender_email and sender_password and recipient_email:
    try:
        # Fetch data from URL
        response = requests.get(url, headers=header)
        print(response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract price and title
        whole_price = soup.find(class_="a-offscreen").getText()
        price = float(whole_price.split("$")[1])

        print(price)
        title = soup.find(id="productTitle").get_text().strip()
        print(title)

        # Prepare email content
        subject = "Amazon Price Alert!"
        body = f"CONGRATS!!\n {title} is now below your target price.\n You can buy the {title} at {price}."
        email_text = f"Subject: {subject}\n\n{body}\n{url}"

        # Check if price is below $100 and send email
        if price < 100:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, email_text.encode("utf-8"))
            print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to process or send email: {e}")

else:
    print("One or more required environment variables are missing. Check your configuration.")

