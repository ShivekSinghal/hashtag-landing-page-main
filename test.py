from PIL import Image, ImageDraw, ImageFont
import qrcode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

def send_grid_ticket(name, show, number_of_tickets, to_email):

    def add_text_to_image(image, text, position, font_path, font_size):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)
        draw.text(position, text, font=font, fill="black")
        return image

    def add_qr_code_to_image(image, qr_data, position, qr_size):
        qr = qrcode.QRCode(version=1, box_size=qr_size, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill='black', back_color='white')
        qr_image = qr_image.resize((qr_size * 10, qr_size * 10))
        image.paste(qr_image, position)
        return image

    def create_ticket(name, ticket_number, qr_data, template_path, output_path):
        font_path = "arial.ttf"  # Path to the font file
        if not os.path.exists(font_path):
            print("Font file not found. Using default font.")
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update to a font path available on your system

        font_size = 20
        name_position = (50, 50)  # Adjust the position accordingly
        ticket_number_position = (50, 100)  # Adjust the position accordingly
        qr_position = (300, 50)  # Adjust the position accordingly
        qr_size = 10

        image = Image.open(template_path)
        image = add_text_to_image(image, f"Name: {name}", name_position, font_path, font_size)
        image = add_text_to_image(image, f"Ticket #: {ticket_number}", ticket_number_position, font_path, font_size)
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
    # name = "John Doe"
    # number_of_tickets = 3  # Number of tickets the person has booked
    # show = "show1"  # Specify the show here ("show1" or "show2")
    ticket_file = f"{show}_ticket_number.txt"  # Use separate files for each show

    attachment_paths = []

    for _ in range(number_of_tickets):
        ticket_number = show + str(increment_ticket_number(ticket_file))  # Get and increment the current ticket number for the specified show
        qr_data = f"Ticket #: {ticket_number}\nName: {name}\nShow: {show}"
        output_path = f"{show}_ticket_{ticket_number}.png"
        create_ticket(name, ticket_number, qr_data, template_path, output_path)
        attachment_paths.append(output_path)

    # to_email = "singhalshivek24@gmail.com"
    subject = "Your Event Tickets"
    body = f"Please find attached your tickets for {show}."

    send_email_with_attachments(to_email, subject, body, attachment_paths)

    # Clean up generated tickets
    for path in attachment_paths:
        os.remove(path)