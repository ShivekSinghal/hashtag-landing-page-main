import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import csv
from ticket_generator import generate_tickets

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

def process_tickets_from_csv(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        rows = list(csv_reader)

    for row in rows:
        name = row["Name"]
        first_name = name.split()[0]
        last_name = name.split()[1] if len(name.split()) > 1 else ''
        phone = row["Phone"]
        email = row["Email"]
        show = row["Show"]
        number_of_tickets = row["NumberOfTickets"]
        to_email = row["Email"]
        price = row["Price"]

        ticket_numbers, attachment_paths = generate_tickets(name, first_name, last_name, phone, email, show, number_of_tickets, price)

        subject = "Grid Tickets"
        body = f"Please find attached your tickets for Show on {show}."
        send_email_with_attachments(to_email, subject, body, attachment_paths)

        # Clean up generated tickets
        for path in attachment_paths:
            os.remove(path)

        # Update the row with ticket numbers
        row["TicketNumbers"] = ", ".join(ticket_numbers)

    # Write updated rows back to CSV
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

process_tickets_from_csv("ticketinput.csv")
