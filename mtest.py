
import smtplib
import time
import os
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body):
    config = configparser.ConfigParser()
    config.read('config.ini')

    sender_email = config['Email']['sender_email']
    receiver_email = config['Email']['receiver_email']
    smtp_server = config['Email']['smtp_server']
    smtp_port = int(config['Email']['smtp_port'])
    smtp_username = config['Email']['smtp_username']
    smtp_password = config['Email']['smtp_password']

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add HTML content to the email body
    message.attach(MIMEText(body, 'html'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def monitor_log_file(log_file_path, log_copy_path, keywords):
    last_position = 0

    while True:
        with open(log_file_path, 'r') as log_file, open(log_copy_path, 'a') as log_copy:
            log_file.seek(last_position)
            new_content = log_file.read()
            log_copy.write(new_content)  # Write content to copied log file
            last_position = log_file.tell()

            for keyword in keywords:
                if keyword in new_content:
                    subject = f'New {keyword} in Log File'
                    # body = f'<html><body><h2>New {keyword} in Log File</h2><p>The following {keyword.lower()} was found in the log file:</p><pre>{new_content}</pre></body></html>'
                    body= f'<html><body style="border:solid 1px; background:white";><h2 style="background:blue;color:white;padding: 10px";>New {keyword} in Log File</h2><p style="padding:10px">The following {keyword.lower()} was found in the log file:</p><pre>{new_content}</pre></body></html>'
                    send_email(subject, body)

        time.sleep(60)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    log_file_path = config['Log']['log_file_path']
    log_copy_path = config['Log']['log_copy_path']
    keywords = config['Keywords']['keywords'].split(", ")

    monitor_log_file(log_file_path, log_copy_path, keywords)
