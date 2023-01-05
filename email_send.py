import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendEmail(receiver: str, link: str):
    sender_email = "hoang.nicolas2409@gmail.com"


    receiver_email = receiver
    password = "smgbevkdudfvvzpv"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your email."
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
Dear valued customer,

Thank you for registering with our service. In order to fully activate your account and access all of our features, we require that you verify your email address.

Please follow the link below to complete the email verification process:

{link}

If you have any issues or questions regarding this process, please don't hesitate to reach out to our customer support team.

Thank you for choosing our service, and we look forward to providing you with a positive experience.

Sincerely,
Vietnam Electronic Art (Veart)
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
