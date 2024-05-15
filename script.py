from google.cloud import storage
from email.mime.text import MIMEText
from datetime import datetime
import smtplib


def list_buckets(project_id):
    storage_client = storage.Client(project=project_id)
    list_bucket = []
    for bucket in storage_client.list_buckets():
        list_bucket.append(bucket)

    return list_bucket

def list_blobs(project_id, bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client(project=project_id)

    blobs = storage_client.list_blobs(bucket_name)

    header = "<html><body>"
    body = ""

    current_dateTime = datetime.now()
    print("[{}] Start scan bucket {}".format(current_dateTime, bucket_name))

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
    print("[{}] End scan {}".format(current_dateTime, bucket_name))

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

# sending email properties
GMAIL_USERNAME = "redacted"
GMAIL_APP_PASSWORD = "redacted"
body = "This is the body of the text message"
recipients = ["redacted"]

# main code
list_bucket = list_buckets(project_id)
for item_list_bucket in list_bucket:
    html_data_email = list_blobs(project_id, item_list_bucket)
    current_dateTime = datetime.now()
    subject = "[{}] Report scan Public GCS {}".format(current_dateTime, item_list_bucket)
    send_email(subject, html_data_email, GMAIL_USERNAME, recipients, GMAIL_APP_PASSWORD)