from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

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
        font_path = "IMPACT.TTF"  # Update to a font path available on your system

    font_size = 50
    name_position = (387.26, 158)  # Adjust the position accordingly
    ticket_number_position = (210.43, 664.9)  # Adjust the position accordingly
    qr_position = (1063, 162)  # Adjust the position accordingly
    qr_size = 30

    event_date = ticket_number[:8]  # Extract the event date from the ticket number
    event_date_position = (386.26, 267)

    price = f"Rs. {price}"
    price_position = (834.6, 664.28)

    image = Image.open(template_path)
    image = add_text_to_image(image, name, name_position, font_path, font_size, color="white")
    image = add_text_to_image(image, ticket_number, ticket_number_position, font_path, font_size, color="white")
    image = add_text_to_image(image, event_date, event_date_position, font_path, font_size, color="white")
    image = add_text_to_image(image, price, price_position, font_path, font_size, color="white")

    image = add_qr_code_to_image(image, qr_data, qr_position, qr_size)

    image.save(output_path)

def get_current_ticket_number(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            file.write("0")
    with open(filename, "r") as file:
        current_ticket_number = int(file.read().strip())
    return current_ticket_number

def increment_ticket_number(filename):
    current_ticket_number = get_current_ticket_number(filename)
    new_ticket_number = current_ticket_number + 1
    with open(filename, "w") as file:
        file.write(str(new_ticket_number))
    return new_ticket_number

def generate_tickets(name, first_name, last_name, phone, email, show, number_of_tickets, price):
    template_path = "ticket_template.png"
    ticket_file = f"{show}_ticket_number.txt"  # Use separate files for each show

    ticket_numbers = []

    for _ in range(int(number_of_tickets)):
        ticket_number = show + str(increment_ticket_number(ticket_file))  # Get and increment the current ticket number for the specified show
        qr_data = f"https://docs.google.com/forms/d/e/1FAIpQLScLU6j8PKGlxsa5LV-PY9XHRl-Y1mr04vDgp8Eo8ApbmE4gXQ/viewform?usp=pp_url&entry.1211795223={first_name + last_name}&entry.669271916={phone}&entry.539132351={email}&entry.966328261={show}&entry.1058215280={ticket_number}"
        output_path = f"{show}_ticket_{ticket_number}.png"
        create_ticket(name, ticket_number, qr_data, template_path, output_path, price)
        ticket_numbers.append(ticket_number)

    return ticket_numbers, [f"{show}_ticket_{ticket_number}.png" for ticket_number in ticket_numbers]
