from google.cloud import storage
from email.mime.text import MIMEText
import smtplib


def list_blobs(project_id, bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client(project=project_id)

    blobs = storage_client.list_blobs(bucket_name)

    header = "<html><body>"
    body = ""
    for blob in blobs:
        print(blob.name)
        item = blob.name
        body = "{}{}<br/>".format(body, item)

    footer = "</body></html>"

    data = "{}{}{}".format(header, body, footer)
    
    return data

def send_email(subject, body, GMAIL_USERNAME, recipients, GMAIL_APP_PASSWORD):
    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = GMAIL_USERNAME
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(GMAIL_USERNAME, GMAIL_APP_PASSWORD)
       smtp_server.sendmail(GMAIL_USERNAME, recipients, msg.as_string())
    print("Message sent!")


# project and bucket data
project_id = "redacted"
bucket_name = "redacted"

# sending email properties
GMAIL_USERNAME = "redacted"
GMAIL_APP_PASSWORD = "redacted"
subject = "Email Subject"
body = "This is the body of the text message"
recipients = ["redacted"]

# main code
html_data_email = list_blobs(project_id, bucket_name)
send_email(subject, html_data_email, GMAIL_USERNAME, recipients, GMAIL_APP_PASSWORD)