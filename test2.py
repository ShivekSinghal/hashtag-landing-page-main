from datetime import datetime

# Get the current date and time
def get_date():
    now = datetime.now()

    # Print the current date and time
    print("Current date and time:", now)

    # Format the current date and time as a string
    return now.strftime("%d-%m-%Y %H:%M:%S")
