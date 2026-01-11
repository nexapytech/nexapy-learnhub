import smtplib
from email.message import EmailMessage

# Create the email
msg = EmailMessage()
msg['Subject'] = 'Test Email from Python'
msg['From'] = 'tijani@hadinaturals.com'
msg['To'] = 'samsonolaoluwa19@gmail.com'  # Change this to the actual recipient
msg.set_content('Hello,\n\nThis is a test email sent using Python SMTP.\n\nRegards,\nHadinaturals Team')

# SMTP server details
EMAIL_HOST = 'mail.hadinaturals.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tijani@hadinaturals.com'
EMAIL_HOST_PASSWORD = 'uRVT#D@0%Ks??+FD'

# Send the email
try:
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(msg)
    print("✅ Email sent successfully.")
except Exception as e:
    print("❌ Failed to send email:", e)
