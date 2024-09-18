from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
socketio = SocketIO(app)

# Gmail credentials
GMAIL_USERNAME = os.environ.get('GMAIL_USERNAME')
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']

    # Send email
    send_email(sender, recipient, message)

    # Broadcast the message to all connected clients
    emit('message', data, broadcast=True)

def send_email(sender, recipient, message):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'Message from ChatApp'

    body = f"Message: {message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print('Error sending email:', str(e))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)