import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import sys

scheduler = BackgroundScheduler()
scheduler.start()

def main():
    data = {
    'platform': 'mac',
    'user_email': 'verma.samarth05@gmail.com',
    'gmail_key': 'yxegikcvfyzyrwfp',
    'replace_values': ['{name}', '{color}'],
    'emails_data': [
        {'email': 'verma.samarth05@gmail.com', 'parameters': ['John', 'Black']},
        {'email': 'verma.samarth05@gmail.com', 'parameters': ['Franklin', 'Yellow']},
        {'email': 'verma.samarth05@gmail.com', 'parameters': ['Joseph', 'Orange']}
    ],
    'initial_subject': 'Hello {name} and I am {color}',
    'initial_body': 'Hello {name} I love {color}',
    'followup_subject': 'Goodbye {name} and I am not {color}',
    'followup_body': 'Goodbye {name} I hate {color}',
    'followup_days': 1
    }
    
    sender = data['user_email']
    key = data['gmail_key']
    days = data['followup_days']

    refined_data = process_data(data)

    initsend(refined_data, sender, key)

    schedule_followup(refined_data, sender, key, days)

def process_data(data):
    formatted_emails = []

    # Loop through each email and its parameters
    for email_data in data['emails_data']:
        email = email_data['email']
        params = email_data['parameters']
        
        # Copy the initial templates
        initial_subject = data['initial_subject']
        initial_body = data['initial_body']
        followup_subject = data['followup_subject']
        followup_body = data['followup_body']
        
        # Replace placeholders with actual parameters
        for placeholder, value in zip(data['replace_values'], params):
            initial_subject = initial_subject.replace(placeholder, value)
            initial_body = initial_body.replace(placeholder, value)
            followup_subject = followup_subject.replace(placeholder, value)
            followup_body = followup_body.replace(placeholder, value)
        
        # Append the formatted email data
        formatted_emails.append({
            'email': email,
            'initial_subject': initial_subject,
            'initial_body': initial_body,
            'followup_subject': followup_subject,
            'followup_body': followup_body
        })

    return formatted_emails

        # NOTE TO SELF :: POSTTEXT KEEPS CHAGING AFTER EVERY ITERATION
        # APPEND TO AN ARRAY AND RETURN THE ARRAY? ALSO YOU NEED THE EMAILS BUT I THINK THATS IN AN ARRAY CALLED formatted_emails
        # POSSIBLE TO RETURN formatted_EMAILS and put all this in a function and then have mac/windows functions
        
        #server = smtplib.SMTP("smtp.gmail.com",587)
        #server.starttls()
        #server.login(sender, key)
        #server.sendmail(sender, email['email'], text)

def initsend(data, sender, key):
    
    for entry in data:
        receiver = entry['email']
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(sender, key)
        text = f"Subject: {entry['initial_subject']}\n\n{entry['initial_body']}"
        server.sendmail(sender, receiver, text)
        print("An email has been sent")
    server.quit()

def followupsend(data, sender, key):

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
    
    run_time = datetime.now() + timedelta(minutes=5)
    scheduler.add_job(followupsend, 'date', run_date=run_time, args=[data, sender, key])
    print(f"Follow-up emails scheduled to run at {run_time}")

if __name__ == "__main__":
    main()