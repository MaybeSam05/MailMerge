from flask import Flask, render_template, request, redirect, url_for, jsonify
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import re

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

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
    followup_subject = sanitize_input(request.form.get('followupSubject'))
    followup_body = sanitize_input(request.form.get('followupBody'))

    # Step 5: Collect follow-up days
    followup_days = int(request.form.get('followupDays'))

    # Step 6: Prepare the data for email processing
    data = {
        "user_email": user_email,
        "gmail_key": gmail_key,
        "replace_values": replace_values,
        "emails_data": emails_data,
        "initial_subject": initial_subject,
        "initial_body": initial_body,
        "followup_subject": followup_subject,
        "followup_body": followup_body,
        "followup_days": followup_days
    }

    # Send initial emails and schedule follow-ups
    refined_data = process_data(data)
    initsend(refined_data, user_email, gmail_key)
    followup_date = schedule_followup(refined_data, user_email, gmail_key, followup_days)

    # Render the success page with relevant info
    return render_template('confirm.html', num_emails=num_emails)


def process_data(data):
    """Format the email data by replacing placeholders."""
    formatted_emails = []

    for email_data in data['emails_data']:
        email = email_data['email']
        params = email_data['parameters']

        initial_subject = data['initial_subject']
        initial_body = data['initial_body']
        followup_subject = data['followup_subject']
        followup_body = data['followup_body']

        for placeholder, value in zip(data['replace_values'], params):
            initial_subject = initial_subject.replace(placeholder, value)
            initial_body = initial_body.replace(placeholder, value)
            followup_subject = followup_subject.replace(placeholder, value)
            followup_body = followup_body.replace(placeholder, value)

        formatted_emails.append({
            'email': email,
            'initial_subject': initial_subject,
            'initial_body': initial_body,
            'followup_subject': followup_subject,
            'followup_body': followup_body
        })

    return formatted_emails


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


def followupsend(data, sender, key):
    """Send follow-up emails to the recipients."""
    for entry in data:
        receiver = entry['email']
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, key)
        text = f"Subject: {entry['followup_subject']}\n\n{entry['followup_body']}"
        server.sendmail(sender, receiver, text)
        print(f"Follow-up email sent to {receiver}")
    server.quit()


def schedule_followup(data, sender, key, days):
    """Schedule the follow-up emails to be sent after a specified number of days."""
    run_time = datetime.now() + timedelta(minutes=days)
    scheduler.add_job(followupsend, 'date', run_date=run_time, args=[data, sender, key])
    print(f"Follow-up emails scheduled to run at {run_time}")


if __name__ == '__main__':
    app.run(debug=True)
