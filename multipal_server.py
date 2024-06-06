import subprocess
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server details
smtp_server = 'email-smtp.ap-south-1.amazonaws.com'
smtp_port = 587  # Port number for SMTP server
smtp_username = ''
smtp_password = ''

# Email details
sender_email = ''
recipient_emails = ['', '']

# List of domains and their corresponding messages
domains = [
    ('hello.com', 'Server hello.com is down'),
    ('example.com', 'Server example.com is down'),
    ('anotherdomain.com', 'Server anotherdomain.com is down'),
    # Add more domains and messages here
]

# Ping interval in seconds (e.g., 60 seconds = 1 minute)
ping_interval = 5

def send_email(subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(recipient_emails)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_emails, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

def check_domain():
    while True:
        for domain, message in domains:
            # Ping the domain
            ping_result = subprocess.run(['curl', domain], stdout=subprocess.DEVNULL).returncode
            print(f"{domain}: {ping_result}")
            if ping_result != 0:
                print(f"Domain {domain} is down. Sending email notification...")
                send_email(f'Server Down Alert for {domain}', message)
            else:
                print(f"Domain {domain} is up.")

        # Wait for the specified interval before checking again
        time.sleep(ping_interval)

if __name__ == "__main__":
    check_domain()
