
from premailer import transform
import base64
from email.mime.image import MIMEImage



def send_receipt(receiver_mail, rendered_html):
    my_email = "universal@hashtag.dance"
    password = 'nnmzpvnfimvoqgjk'
    smtp_server = "smtp.gmail.com"
    email_subject = "Registration Receipt Grid 2.0 '23"
    smtp_port = 587

    inlined_html = transform(rendered_html)

    msg = MIMEMultipart()
    msg["From"] = my_email
    msg["To"] = receiver_mail
    msg["Subject"] = email_subject

    body = MIMEText(inlined_html, "html")
    msg.attach(body)
    with open('./static/images/Hashtag_logo.png', 'rb') as image_file:
        image = MIMEImage(image_file.read())
        image.add_header('Content-ID', '<logo_image>')
        msg.attach(image)
    with open('./static/images/phone.png', 'rb') as image_file:
        image_phone = MIMEImage(image_file.read())
        image_phone.add_header('Content-ID', '<phone>')
        msg.attach(image_phone)
    with open('./static/images/whatsapp.png', 'rb') as image_file:
        image_whatsapp = MIMEImage(image_file.read())
        image_whatsapp.add_header('Content-ID', '<whatsapp>')
        msg.attach(image_whatsapp)
    with open('./static/images/instagram.png', 'rb') as image_file:
        image_instagram = MIMEImage(image_file.read())
        image_instagram.add_header('Content-ID', '<instagram>')
        msg.attach(image_instagram)

    with open('./static/images/email.png', 'rb') as image_file:
        image_email = MIMEImage(image_file.read())
        image_email.add_header('Content-ID', '<email>')
        msg.attach(image_email)

    with open('./static/images/pink.png', 'rb') as image_file:
        image_watermark = MIMEImage(image_file.read())
        image_watermark.add_header('Content-ID', '<watermark>')
        msg.attach(image_watermark)

    with smtplib.SMTP(smtp_server, smtp_port) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.send_message(msg)


