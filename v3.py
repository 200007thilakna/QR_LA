import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from datetime import datetime, timedelta
from base64 import urlsafe_b64encode
import qrcode
from PIL import Image


def send_daily_email(sender_email, sender_password, receiver_email, image_path):
    subject = "Household Survey"
    body = f"""Please find the QR code for {datetime.now().strftime('%Y-%m-%d')} attached."""

    em = MIMEMultipart()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.attach(MIMEText(body, 'plain'))

    with open(image_path, 'rb') as img_file:
        img_attachment = MIMEApplication(img_file.read(), _subtype="png")
        img_attachment.add_header('Content-Disposition', 'attachment', filename='qr_code.png')
        em.attach(img_attachment)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(em)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")




def generate_dynamic_qr_code(data, expiration_minutes):
    current_datetime = datetime.now()
    expiration_time = timedelta(minutes=expiration_minutes)
    expiration_datetime = current_datetime + expiration_time
    rounded_minutes = expiration_datetime.minute + 1  # Rounding up minutes
    expiration_datetime = expiration_datetime.replace(minute=rounded_minutes, second=0, microsecond=0)

    # string representation
    encoded_datetime = expiration_datetime.isoformat()

    # Encoding the string to make it URL-safe
    encoded_data = urlsafe_b64encode(encoded_datetime.encode()).decode()

    data_with_expiration = f"{data}?dynamic_qr_data={encoded_data}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_with_expiration)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image with today's date as the filename
    today_date_str = current_datetime.strftime('%Y-%m-%d')
    img_filename = f"{today_date_str}.png"
    img.save(img_filename)



    return data_with_expiration

data_to_encode = "https://www.leco.lk/index_e.php"
expiration_minutes = 1440
dynamic_qr_data = generate_dynamic_qr_code(data_to_encode, expiration_minutes)
print(f"Dynamic QR code data: {dynamic_qr_data}")

current_datetime = datetime.now()
today_date_str = current_datetime.strftime('%Y-%m-%d')
send_daily_email('tosendmail.11@gmail.com', 'aces jltl lwfc mshp', 'thilaknakumaratunga@gmail.com', f"{today_date_str}.png")
