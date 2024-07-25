import csv
import json

# Path to your CSV file
csv_file_path = 'GridPromoCode.csv'

# Function to clean and count emails
def clean_and_count_emails(email_str):
    emails = [email.strip() for email in email_str.split(',')]
    return list(set(emails)), len(emails)

# Read the CSV file
with open(csv_file_path, newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    json_list = []
    email_count = {}

    for row in csv_reader:
        email_str = row["Email"]
        cleaned_emails, num_emails = clean_and_count_emails(email_str)

        for email in cleaned_emails:
            email_count[email] = email_count.get(email, 0) + 1

            if email_count[email] <= 2:
                json_item = {
                    "promo_code": row["Promo Code"],
                    "expiry": "2024-07-30 23:59:59",  # Setting the new expiry date
                    "name": row["Name"],
                    "email": email,
                    "phone": "9999799357",  # Assuming this is a placeholder and not in CSV
                    "amount": row["Amount"]
                }
                json_list.append(json_item)

# Save the JSON to a file
with open('grid_promocode.json', 'w') as jsonfile:
    json.dump(json_list, jsonfile, indent=4)

print("JSON data has been saved to grid_promocode.json")
