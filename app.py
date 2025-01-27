from flask import Flask, render_template, request, redirect, url_for, jsonify
import smtplib
from datetime import datetime, timedelta
import re
import csv

app = Flask(__name__)

def sanitize_input(input_str):
    """Remove special characters from input to prevent issues."""
    if input_str:
        return re.sub(r'[^\w\s@.]+', '', input_str)
    return input_str

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('parameters'))
    return render_template('index.html')

@app.route('/parameters', methods=['GET', 'POST'])
def parameters():
    return render_template('parameters.html')

@app.route('/csvparameters', methods=['GET', 'POST'])
def csvparameters():
    return render_template('csvparameters.html')

@app.route('/upload', methods=['POST'])
def handle_csvdata():
    response = upload_file()

    file = getFileName(response)
    gmail_key = sanitize_input(request.form.get('gmailKey'))
    user_email = sanitize_input(request.form.get('userEmail'))
    initial_subject = sanitize_input(request.form.get('initialSubject'))
    initial_body = sanitize_input(request.form.get('initialBody'))

    emailData, num_emails = csvprocess(file, initial_subject, initial_body)
    sendCsvEmails(emailData, user_email, gmail_key)

    return render_template('confirm.html', num_emails=num_emails)

@app.route('/submit', methods=['POST'])
def submit():
    # Step 1: Collect and sanitize Gmail key and user email
    gmail_key = sanitize_input(request.form.get('gmailKey'))
    user_email = sanitize_input(request.form.get('userEmail'))

    # Step 2: Collect and sanitize Replace values
    num_params = int(request.form.get('numParams'))
    replace_values = [sanitize_input(request.form.get(f'replace{i}')) for i in range(1, num_params + 1)]

    # Step 3: Collect and sanitize emails and their parameters
    num_emails = int(request.form.get('numEmails'))
    emails_data = []
    for i in range(1, num_emails + 1):
        email = sanitize_input(request.form.get(f'email{i}'))
        params = [sanitize_input(request.form.get(f'email{i}_param{j}')) for j in range(1, num_params + 1)]
        emails_data.append({"email": email, "parameters": params})

    # Step 4: Collect and sanitize initial and follow-up email data
    initial_subject = sanitize_input(request.form.get('initialSubject'))
    initial_body = sanitize_input(request.form.get('initialBody'))

    # Step 6: Prepare the data for email processing
    data = {
        "user_email": user_email,
        "gmail_key": gmail_key,
        "replace_values": replace_values,
        "emails_data": emails_data,
        "initial_subject": initial_subject,
        "initial_body": initial_body,
        #"followup_subject": followup_subject,
        #"followup_body": followup_body,
        #"followup_days": followup_days
    }

    # Send initial emails and schedule follow-ups
    refined_data = process_data(data)
    initsend(refined_data, user_email, gmail_key)
    #followup_date = schedule_followup(refined_data, user_email, gmail_key, followup_days)

    # Render the success page with relevant info
    return render_template('confirm.html', num_emails=num_emails)

def upload_file():
    if 'csvFile' not in request.files:
        return "No file part", 400

    file = request.files['csvFile']
    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.csv'):
        file.save(f"{file.filename}")  
        return {"message": "File uploaded successfully!", "file_name": file.filename}, 200

    return "Invalid file type", 400

def getFileName(response):
    if isinstance(response, tuple): 
        message, status_code = response
        if status_code == 200:
            file_name = message['file_name'] 
            return file_name
        else:
            return f"Error: {message}"
    else:
        return f"Unexpected response: {response}"


def process_data(data):
    """Format the email data by replacing placeholders."""
    formatted_emails = []

    for email_data in data['emails_data']:
        email = email_data['email']
        params = email_data['parameters']

        initial_subject = data['initial_subject']
        initial_body = data['initial_body']

        for placeholder, value in zip(data['replace_values'], params):
            initial_subject = initial_subject.replace(placeholder, value)
            initial_body = initial_body.replace(placeholder, value)

        formatted_emails.append({
            'email': email,
            'initial_subject': initial_subject,
            'initial_body': initial_body,
        })

    return formatted_emails

def csvprocess(csvfile, emailSubject, emailBody):
    filePath = "/uploads/" + csvfile
    
    formattedEmails = {}

    with open(filePath, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        parameters = headers[1:]  # all parameters
        
        for row in csv_reader:
            email = row[0]
            param_dict = dict(zip(parameters, row[1:]))
            
            formatted_subject = emailSubject
            formatted_body = emailBody
            for param, value in param_dict.items():
                formatted_subject = formatted_subject.replace(param, value)
                formatted_body = formatted_body.replace(param, value)
            
            formattedEmails[email] = (formatted_subject, formatted_body)
    
    return formattedEmails, len(formattedEmails)


def initsend(data, sender, key):
    """Send initial emails to the recipients."""
    for entry in data:
        receiver = entry['email']
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, key)
        text = f"Subject: {entry['initial_subject']}\n\n{entry['initial_body']}"
        server.sendmail(sender, receiver, text)
        print(f"Initial email sent to {receiver}")
    server.quit()

def sendCsvEmails(data, sender, key):
    """Send csv emails to the recipients."""
    for email, (subject, body) in data.items():
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, key)
        text = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender, email, text)
        print(f"Initial email sent to {email}")
    server.quit()

if __name__ == '__main__':
    app.run(debug=True)