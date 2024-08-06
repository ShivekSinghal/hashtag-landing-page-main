import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import csv
import json
import zipfile
import time
from ticket_generator import generate_tickets
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)


def upload_file_to_drive(file_path, retries=3):
    try:
        file_metadata = {'name': os.path.basename(file_path)}
        media = MediaFileUpload(file_path, mimetype='application/zip')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')
    except Exception as e:
        if retries > 0:
            print(f"Upload failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            return upload_file_to_drive(file_path, retries - 1)
        else:
            print(f"Failed to upload file to Google Drive after multiple attempts: {e}")
            return None


def generate_shareable_link(file_id):
    try:
        request_body = {'role': 'reader', 'type': 'anyone'}
        service.permissions().create(fileId=file_id, body=request_body).execute()
        link = f"https://drive.google.com/file/d/{file_id}/view"
        return link
    except Exception as e:
        print(f"Failed to generate shareable link: {e}")
        return None


def send_email_with_attachments(to_email, subject, body, attachment_path):
    from_email = "universal@hashtag.dance"
    password = "mmowlsextvnjwkzz"

    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach the body text
        msg.attach(MIMEText(body, "plain"))

        # Attach the file
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

        print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")


def generate_and_zip_tickets(rows):
    try:
        ticket_details = []
        attachment_paths = []

        for row in rows:
            name = row["Name"]
            first_name = name.split()[0]
            last_name = name.split()[1] if len(name.split()) > 1 else ''
            phone = row.get("Phone", "")
            email = row["Email"]
            show = row["Show"]
            number_of_tickets = row["NumberOfTickets"]
            to_email = row["Email"]
            price = row["Price"]

            print(f"Processing tickets for {name} ({to_email}) for show on {show}")

            ticket_numbers, generated_paths = generate_tickets(name, first_name, last_name, phone, email, show,
                                                               number_of_tickets, price)
            attachment_paths.extend(generated_paths)

            # Update the row with ticket numbers and status
            row["TicketNumbers"] = ", ".join(ticket_numbers)
            row["Status"] = "Sent"

            # Add ticket details to the list
            ticket_details.append({
                "Name": name,
                "Email": email,
                "Phone": phone,
                "TicketNumbers": ticket_numbers
            })

        # Zip all generated ticket files
        zip_filename = "tickets.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in attachment_paths:
                zipf.write(file, os.path.basename(file))

        return zip_filename, ticket_details

    except Exception as e:
        print(f"Failed to generate and zip tickets: {e}")
        return None, None


def process_tickets_from_csv(csv_file_path):
    try:
        with open(csv_file_path, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            rows = list(csv_reader)

        # Generate tickets and create zip file
        zip_filename, ticket_details = generate_and_zip_tickets(rows)

        if zip_filename and ticket_details:
            # Upload zip file to Google Drive
            file_id = upload_file_to_drive(zip_filename)
            if file_id:
                shareable_link = generate_shareable_link(file_id)

                if shareable_link:
                    # Send email with the shareable link
                    subject = "Grid Tickets"
                    body = f"Please find your attached tickets for the show on {rows[0]['Show']}.\nYou can also download all the tickets from the following link:\n{shareable_link}"
                    send_email_with_attachments(rows[0]["Email"], subject, body, zip_filename)

                    # Clean up generated tickets
                    for path in ticket_details:
                        os.remove(path)

                    # Remove zip file
                    os.remove(zip_filename)

                    # Write updated rows back to CSV
                    with open(csv_file_path, 'w', newline='') as csvfile:
                        fieldnames = rows[0].keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(rows)

                    # Write ticket details to JSON
                    json_file_path = "ticket_details.json"
                    with open(json_file_path, 'w') as jsonfile:
                        json.dump(ticket_details, jsonfile, indent=4)

                    print("All tickets processed and emails sent")
                    print(f"Ticket details saved to {json_file_path}")

    except Exception as e:
        print(f"Failed to process CSV file: {e}")


process_tickets_from_csv("HashtagRegistrations.csv")
