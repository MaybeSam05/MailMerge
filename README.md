# Mail Merge Email Automation

https://mailmerge-2k00.onrender.com/
A Flask-based web application that streamlines email workflows by automating the process of sending initial and follow-up emails. The app allows users to input parameters, create personalized email content, and schedule follow-up emails automatically.

## Features

- **Platform Selection**: Supports both Mac and Windows platforms.
- **Dynamic Input Generation**: Users can specify placeholders and parameters for email personalization.
- **Automated Email Sending**: Sends initial and follow-up emails with customizable content.
- **Scheduling**: Uses `APScheduler` to schedule follow-up emails after a specified number of days.
- **Sanitized Input**: Ensures safe handling of user input to prevent injection attacks.
- **User-Friendly Interface**: Simple and intuitive forms for data input and email scheduling.

## Technologies Used

- **Flask**: Backend framework for web application development.
- **HTML/CSS**: Frontend structure and styling.
- **APScheduler**: For scheduling email follow-ups.
- **smtplib**: Python library for sending emails via SMTP.
- **Jinja2**: Templating engine for rendering dynamic HTML pages.

## Setup Instructions

1. Clone the repository.
2. Install dependencies using:
  
   pip install -r requirements.txt

3. Run the Flask app:

   python app.py

4. Open a web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

1. **Home Page**: Click "Continue" to start setting up your email automation.
2. **Parameters Page**: 
   - Select your platform (Mac or Windows).
   - Enter your Gmail key and user email.
   - Specify the number of placeholders and emails.
   - Provide initial and follow-up email content.
3. **Submit**: After filling out the form, click "Done" to start the email automation process. A confirmation page will indicate successful submission.

## File Structure

- `app.py`: Main Flask application logic.
- `main.py`: Additional script for email processing and scheduling.
- `templates/index.html`: Landing page.
- `templates/parameters.html`: Form for user input.
- `templates/confirm.html`: Confirmation page after successful email setup.
- `requirements.txt`: List of dependencies.
- `README.md`: Project documentation.

## Dependencies

- Flask==3.1.0
- APScheduler==3.11.0
- gunicorn==23.0.0
- python-dotenv==1.0.1
- smtplib (built-in)