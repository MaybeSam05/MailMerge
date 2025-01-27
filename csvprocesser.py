import csv
import sys

# structure of csv 
# email , [parameter1], [parameter2], ...
# email2 , [parameter1], [parameter2], ...


# manual input: 
# user email, email key, subject, body

def main():
    emailSubject = "Hello {name} I am a {title}"
    emailBody = "Hi, it's {name} from {company} as a {title} and I'm feeling {color}"
    
    formattedEmails = []  # Use a list to store all email data
    
    with open('input.csv', 'r') as file:
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
            
            formattedEmails.append({
                "email": email,
                "initial_subject": formatted_subject,
                "initial_body": formatted_body
            })
    
    # Print results
    for entry in formattedEmails:
        print(f"\nEmail: {entry['email']}")
        print(f"Subject: {entry['initial_subject']}")
        print(f"Body: {entry['initial_body']}")
    
    print(f"Total entries: {len(formattedEmails)}")

if __name__ == "__main__": 
    main()
