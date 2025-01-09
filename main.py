import smtplib

def main():
    data = {
    'platform': 'mac',
    'user_email': 'verma.samarth05@gmail.com',
    'gmail_key': 'Blah Blah',
    'replace_values': ['{name}', '{color}'],
    'emails_data': [
        {'email': 'hello@gmail.com', 'parameters': ['John', 'Black']},
        {'email': 'bye@gmail.com', 'parameters': ['Franklin', 'Yellow']},
        {'email': 'yellow@gmail.com', 'parameters': ['Joseph', 'Orange']}
    ],
    'initial_subject': 'Hello {name} and I am {color}',
    'initial_body': 'Hello {name} I love {color}',
    'followup_subject': 'Goodbye {name} and I am not {color}',
    'followup_body': 'Goodbye {name} I hate {color}',
    'followup_days': 1
    }
    
    platform = data['platform']

    if platform == "mac":
        Mac(data)
    else:
        Windows(data)

def Mac(data):
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

    # Output the result
    for email in formatted_emails:
        print(f"Email: {email['email']}")
        print(f"Initial Subject: {email['initial_subject']}")
        print(f"Initial Body: {email['initial_body']}")
        print(f"Follow-Up Subject: {email['followup_subject']}")
        print(f"Follow-Up Body: {email['followup_body']}")
        print("-" * 40)

def Windows(data):
    print("Hi")


if __name__ == "__main__":
    main()