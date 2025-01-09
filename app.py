from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

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
    # Step 1: Collect Gmail key
    gmail_key = request.form.get('gmailKey')

    platform = request.form.get('platform')

    # Step 2: Collect Replace values
    num_params = int(request.form.get('numParams'))
    replace_values = [request.form.get(f'replace{i}') for i in range(1, num_params + 1)]

    # Step 3: Collect emails and their parameters
    num_emails = int(request.form.get('numEmails'))
    emails_data = []
    for i in range(1, num_emails + 1):
        email = request.form.get(f'email{i}')
        params = [request.form.get(f'email{i}_param{j}') for j in range(1, num_params + 1)]
        emails_data.append({"email": email, "parameters": params})

    # Step 4: Collect initial and followup email data
    initial_subject = request.form.get('initialSubject')
    initial_body = request.form.get('initialBody')
    followup_subject = request.form.get('followupSubject')
    followup_body = request.form.get('followupBody')

    # Step 5: Collect followup days
    followup_days = int(request.form.get('followupDays'))

    # Step 6: Return or process data
    data = {
        "platform": platform,
        "gmail_key": gmail_key,
        "replace_values": replace_values,
        "emails_data": emails_data,
        "initial_subject": initial_subject,
        "initial_body": initial_body,
        "followup_subject": followup_subject,
        "followup_body": followup_body,
        "followup_days": followup_days
    }

    # Print or log the data for debugging purposes
    print(data)
    # Return the data as JSON for demonstration
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
