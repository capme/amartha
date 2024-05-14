from google.cloud import storage
from email.mime.text import MIMEText
from datetime import datetime
import smtplib


def list_blobs(project_id, bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client(project=project_id)

    blobs = storage_client.list_blobs(bucket_name)

    header = "<html><body>"
    body = ""

    current_dateTime = datetime.now()
    print("[{}] Start scan".format(current_dateTime))

    for blob in blobs:
        item = blob.name
        if "." in item and "/" in item:
            # containing full path of file and folder
            body = "{} - {}<br/>".format(body, item)
        elif "/" in item:
            # containing only folder
            body = "{} <br/>Folder : {}<br/>".format(body, item)
        elif "." in item:
            # containing only file
            body = "{} - {}<br/>".format(body, item)

    footer = "</body></html>"

    data = "{}{}{}".format(header, body, footer)

    current_dateTime = datetime.now()
    print("[{}] End scan".format(current_dateTime))

    return data

def send_email(subject, body, GMAIL_USERNAME, recipients, GMAIL_APP_PASSWORD):
    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = GMAIL_USERNAME
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(GMAIL_USERNAME, GMAIL_APP_PASSWORD)
       smtp_server.sendmail(GMAIL_USERNAME, recipients, msg.as_string())

    current_dateTime = datetime.now()
    print("[{}] Report sent!".format(current_dateTime))


# project and bucket data
project_id = "redacted"
bucket_name = "redacted"

# sending email properties
GMAIL_USERNAME = "redacted"
GMAIL_APP_PASSWORD = "redacted"
current_dateTime = datetime.now()
subject = "[{}] Report scan Public GCS".format(current_dateTime)
body = "This is the body of the text message"
recipients = ["redacted"]

# main code
html_data_email = list_blobs(project_id, bucket_name)
send_email(subject, html_data_email, GMAIL_USERNAME, recipients, GMAIL_APP_PASSWORD)