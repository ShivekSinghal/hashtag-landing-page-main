from flask import Flask, request, jsonify,render_template
import os
import csv
import json
import zipfile
from ticket_generator import generate_tickets
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

app = Flask(__name__)

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)


def upload_file_to_drive(file_path):
    try:
        file_metadata = {'name': os.path.basename(file_path)}
        media = MediaFileUpload(file_path, mimetype='application/zip')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')
    except Exception as e:
        print(f"Failed to upload file to Google Drive: {e}")
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
            price = row["Price"]

            print(f"Processing tickets for {name} ({email}) for show on {show}")

            ticket_numbers, generated_paths = generate_tickets(name, first_name, last_name, phone, email, show,
                                                               number_of_tickets, price)
            attachment_paths.extend(generated_paths)

            # Add ticket details to the list
            ticket_details.append({
                "Name": name,
                "Email": email,
                "Phone": phone,
                "TicketNumbers": ticket_numbers
            })

            # Update the row with ticket numbers and status
            row["TicketNumbers"] = ", ".join(ticket_numbers)
            row["Status"] = "Generated"

        # Zip all generated ticket files
        zip_filename = "tickets.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in attachment_paths:
                zipf.write(file, os.path.basename(file))

        return zip_filename, attachment_paths, ticket_details, rows

    except Exception as e:
        print(f"Failed to generate and zip tickets: {e}")
        return None, None, None, None


@app.route('/generate_tickets', methods=['POST'])
def process_tickets_from_csv():
    try:
        csv_file_path = request.json['fcsv_file_path']

        with open(csv_file_path, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            rows = list(csv_reader)

        # Generate tickets and create zip file
        zip_filename, attachment_paths, ticket_details, updated_rows = generate_and_zip_tickets(rows)

        if zip_filename and ticket_details:
            # Upload zip file to Google Drive
            file_id = upload_file_to_drive(zip_filename)
            if file_id:
                shareable_link = generate_shareable_link(file_id)

                if shareable_link:
                    # Clean up generated tickets
                    for path in attachment_paths:
                        os.remove(path)

                    # Remove zip file
                    os.remove(zip_filename)

                    # Write updated rows back to CSV
                    with open(csv_file_path, 'w', newline='') as csvfile:
                        fieldnames = updated_rows[0].keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(updated_rows)

                    # Write ticket details to JSON
                    json_file_path = "ticket_details.json"
                    with open(json_file_path, 'w') as jsonfile:
                        json.dump(ticket_details, jsonfile, indent=4)

                    print("All tickets processed")
                    print(f"Ticket details saved to {json_file_path}")

                    return jsonify({'link': shareable_link}), 200

    except Exception as e:
        print(f"Failed to process CSV file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def success():
    return render_template('downloadticket.html')

if __name__ == '__main__':
    app.run(debug=True)
