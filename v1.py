
import smtplib
from email.message import EmailMessage
import ssl

email_sender = 'tosendmail.11@gmail.com'
email_password = "aces jltl lwfc mshp"  
email_receiver = 'thilaknakumaratunga@gmail.com'

subject = "Household Survey"
body = """Please find the QR code for today"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
        print("Email sent successfully.")
except Exception as e:
    print(f"Error: {e}")

