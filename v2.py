
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime


email_sender = 'tosendmail.11@gmail.com'
email_password = "aces jltl lwfc mshp"  
email_receiver = 'sandevdewthilina2000@gmail.com '

subject = "Household Survey"
body = f"""Please find the QR code for {datetime.now().strftime('%Y-%m-%d')} attached."""

# Create the email message
em = MIMEMultipart()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject

# Attach plain text body
em.attach(MIMEText(body, 'plain'))

# Attach image as an attachment
with open('a.jpeg', 'rb') as img_file:
    img_attachment = MIMEApplication(img_file.read(), _subtype="png")
    img_attachment.add_header('Content-Disposition', 'attachment', filename='qr_code.png')
    em.attach(img_attachment)

context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        # Login with your App Password
        smtp.login(email_sender, email_password)
        
        # Send the email
        smtp.send_message(em)
        print("Email sent successfully.")
except Exception as e:
    print(f"Error: {e}")
