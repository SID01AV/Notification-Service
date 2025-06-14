# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import asyncio
# import aiomisc
# from asyncio import AbstractEventLoop

# class EmailService:
#     def __init__(self, smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str):
#         self.smtp_server = smtp_server
#         self.smtp_port = smtp_port
#         self.smtp_user = smtp_user
#         self.smtp_password = smtp_password

#     async def send_email(self, recipient_email: str, subject: str, body: str):
#         try:
#             # Create the email content
#             msg = MIMEMultipart()
#             msg['From'] = self.smtp_user
#             msg['To'] = recipient_email
#             msg['Subject'] = subject
#             msg.attach(MIMEText(body, 'plain'))

#             # Connect to the SMTP server
#             loop = asyncio.get_event_loop()
#             await loop.run_in_executor(None, self._send_smtp_email, msg)

#             print(f"Email sent to {recipient_email}")
#         except Exception as e:
#             print(f"Error sending email: {e}")

#     def _send_smtp_email(self, msg):
#         try:
#             # Connect to the SMTP server
#             with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
#                 server.starttls()  # Use TLS
#                 server.login(self.smtp_user, self.smtp_password)
#                 server.sendmail(msg['From'], msg['To'], msg.as_string())
#         except Exception as e:
#             print(f"Failed to send email: {e}")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self, smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_email(self, recipient_email: str, subject: str, body: str):
        try:
            # Create the email content
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Send the email
            self._send_smtp_email(msg)

            print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def _send_smtp_email(self, msg):
        try:
            # Connect to the SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Use TLS
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(msg['From'], msg['To'], msg.as_string())
        except Exception as e:
            print(f"Failed to send email: {e}")
