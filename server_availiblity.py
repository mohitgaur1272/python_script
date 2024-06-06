import subprocess
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server details
smtp_server = 'email-smtp.ap-south-1.amazonaws.com'   #replace with your ses host
smtp_port = 587  # Port number for SMTP server
smtp_username = 'your_username'    #replace with your username
smtp_password = 'your_password'    #replacw with your password

# Email details
sender_email = 'sender@gmail.com'
recipient_emails = ['recevier@gmail.com', 'recevier@@gmail.com']
subject = 'Server Down Alert'
body = 'Server <Domain_name> is down.\n I think your server is not working,So go and check your server'

# Ping interval in seconds (e.g., 60 seconds = 1 minutes)
ping_interval = 60    #replace with your desired seconds

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
        # Ping the domain
        ping_result = subprocess.run(['curl', 'Domain_name'], stdout=subprocess.DEVNULL).returncode  #replace with your domain name
        print(ping_result)
        if ping_result != 0:
            print("Domain is down. Sending email notification...")
            send_email(subject, body)
        else:
            print("Domain is properly working and your server is up.")

        # Wait for the specified interval before checking again
        time.sleep(ping_interval)

if __name__ == "__main__":
    check_domain()
