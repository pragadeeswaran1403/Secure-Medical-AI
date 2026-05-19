import smtplib

from email.message import EmailMessage


def send_email(to_email, subject, body, attachment=None):

    EMAIL = "mhprhospital@gmail.com"

    PASSWORD = "lser nfao glhn rswz"

    msg = EmailMessage()

    msg["Subject"] = subject

    msg["From"] = EMAIL

    msg["To"] = to_email

    msg.set_content(body)

    if attachment:

        msg.add_attachment(
            attachment,
            maintype="application",
            subtype="pdf",
            filename="medical_report.pdf"
        )

    try:

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:

            smtp.starttls()

            smtp.login(EMAIL, PASSWORD)

            smtp.send_message(msg)

        print("Email Sent Successfully")

    except Exception as e:

        print("Email Error:", e)    