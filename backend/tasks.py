
from celery_app import  Celery
from models import Trek, Booking, User
from datetime import datetime, timedelta
import csv
import os
from flask_mail import Message 

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery.task
def send_trek_reminder():

    from app import app

    with app.app_context():

        tomorrow = datetime.now().date() + timedelta(days=1)

        treks = Trek.query.all()

        for trek in treks:

            if trek.start_date.date() == tomorrow:

                for booking in trek.bookings:

                    print(
                        f"Reminder sent to {booking.user.email} "
                        f"for trek {trek.name}"
                    )
                    from app import mail

                    msg = Message(
                        subject="Trek Reminder",
                        sender="yourgmail@gmail.com",
                        recipients=[booking.user.email]
                    )

                    msg.body = f"""
                Hello {booking.user.username},

                Your trek {trek.name} starts tomorrow.

                Location : {trek.location}

                Happy Trekking!
                """

                    mail.send(msg)
        return "Reminder Completed"

@celery.task
def generate_monthly_report():

    from app import app

    with app.app_context():

        total_treks = Trek.query.count()

        total_bookings = Booking.query.count()

        users = User.query.filter_by(role="user").count()

        report = f"""
            <html>

            <head>

            <title>Monthly Trek Report</title>

            </head>

            <body>

            <h1>Monthly Trek Report</h1>

            <hr>

            <h3>Total Treks : {total_treks}</h3>

            <h3>Total Users : {users}</h3>

            <h3>Total Bookings : {total_bookings}</h3>

            </body>

            </html>
            """

        with open("monthly_report.html","w") as f:
            f.write(report)

        print("Monthly Report Generated")

        return report

@celery.task
def export_csv(user_id):

    from app import app

    with app.app_context():

        bookings = Booking.query.filter_by(user_id=user_id).all()

        filename = f"user_{user_id}_history.csv"

        with open(filename,"w",newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Trek",
                "Location",
                "Booking Date",
                "Status"
            ])

            for booking in bookings:

                trek = Trek.query.get(booking.trek_id)

                writer.writerow([
                    trek.name,
                    trek.location,
                    booking.booking_date,
                    booking.status
                ])

        print(f"{filename} Generated")

        return filename