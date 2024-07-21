from PIL import Image, ImageDraw, ImageFont
import qrcode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

def send_grid_ticket(name, first_name, last_name, phone, email, show, number_of_tickets, to_email,price):

    def add_text_to_image(image, text, position, font_path, font_size, color="white"):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)
        draw.text(position, text, font=font, fill=color)
        return image

    def add_qr_code_to_image(image, qr_data, position, qr_size):
        qr = qrcode.QRCode(version=1, box_size=qr_size, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill='black', back_color='white')
        qr_image = qr_image.resize((qr_size * 10, qr_size * 10))
        image.paste(qr_image, position)
        return image

    def create_ticket(name, ticket_number, qr_data, template_path, output_path, price):
        font_path = "impact.ttf"  # Path to the font file
        if not os.path.exists(font_path):
            print("Font file not found. Using default font.")
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update to a font path available on your system

        font_size = 50
        name_position = (387.26, 158)  # Adjust the position accordingly
        ticket_number_position = (210.43, 664.9)  # Adjust the position accordingly
        qr_position = (1063, 162)  # Adjust the position accordingly
        qr_size = 30

        event_date = show
        event_date_position = (386.26, 267)

        price = f"Rs. {price}"
        price_position = (834.6,664.28)

        image = Image.open(template_path)
        image = add_text_to_image(image, name, name_position, font_path, font_size, color="white")
        image = add_text_to_image(image, ticket_number, ticket_number_position, font_path, font_size, color="white")
        image = add_text_to_image(image, event_date, event_date_position, font_path, font_size, color="white")
        image = add_text_to_image(image, price, price_position, font_path, font_size, color="white")

        image = add_qr_code_to_image(image, qr_data, qr_position, qr_size)

        image.save(output_path)

    def send_email_with_attachments(to_email, subject, body, attachment_paths):
        from_email = "universal@hashtag.dance"
        password = "mmowlsextvnjwkzz"

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach the body text
        msg.attach(MIMEText(body, "plain"))

        # Attach the files
        for attachment_path in attachment_paths:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
                msg.attach(part)

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())

    # Function to get the current ticket number from a file
    def get_current_ticket_number(filename):
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                file.write("0")
        with open(filename, "r") as file:
            current_ticket_number = int(file.read().strip())
        return current_ticket_number

    # Function to increment and save the current ticket number to a file
    def increment_ticket_number(filename):
        current_ticket_number = get_current_ticket_number(filename)
        new_ticket_number = current_ticket_number + 1
        with open(filename, "w") as file:
            file.write(str(new_ticket_number))
        return new_ticket_number

    # Example usage


    template_path = "ticket_template.png"
    ticket_file = f"{show}_ticket_number.txt"  # Use separate files for each show

    attachment_paths = []

    for _ in range(int(number_of_tickets)):
        ticket_number = show + str(increment_ticket_number(ticket_file))  # Get and increment the current ticket number for the specified show
        qr_data = f"https://docs.google.com/forms/d/e/1FAIpQLScLU6j8PKGlxsa5LV-PY9XHRl-Y1mr04vDgp8Eo8ApbmE4gXQ/viewform?usp=pp_url&entry.1211795223={first_name + last_name}&entry.669271916={phone}&entry.539132351={email}&entry.966328261={show}&entry.1058215280={ticket_number}"
        print(qr_data)
        print("Qr Code")
        output_path = f"{show}_ticket_{ticket_number}.png"
        create_ticket(name, ticket_number, qr_data, template_path, output_path,price)
        attachment_paths.append(output_path)

    subject = "Grid Tickets"
    body = f"Please find attached your tickets for Show on {show}."

    send_email_with_attachments(to_email, subject, body, attachment_paths)

    # Clean up generated tickets
    for path in attachment_paths:
        os.remove(path)
