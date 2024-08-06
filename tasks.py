from celery import Celery
from test import send_grid_ticket  # Import your functions

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def send_grid_ticket_task(name, first_name, last_name, phone, email, studio, number_of_tickets, price):
    send_grid_ticket(name, first_name, last_name, phone, email, studio, number_of_tickets, price)
