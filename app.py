from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/parameters', methods=['GET', 'POST'])
def parameters():
    return render_template('parameters.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Step 1: Collect Gmail key
    gmail_key = request.form.get('gmailKey')

    # Step 2: Collect emails
    num_emails = int(request.form.get('numEmails'))
    emails = [request.form.get(f'email{i}') for i in range(1, num_emails + 1)]

    # Step 3: Collect parameters and replacements
    num_params = int(request.form.get('numParams'))
    param_replace_dict = {
        request.form.get(f'param{i}'): request.form.get(f'replace{i}')
        for i in range(1, num_params + 1)
    }

    # Step 4: Collect initial and followup email data
    initial_subject = request.form.get('initialSubject')
    initial_body = request.form.get('initialBody')
    followup_subject = request.form.get('followupSubject')
    followup_body = request.form.get('followupBody')

    # Step 5: Collect followup days
    followup_days = int(request.form.get('followupDays'))

    # Step 6: Return or process data
    data = {
        "gmail_key": gmail_key,
        "emails": emails,
        "parameters_to_replace": param_replace_dict,
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
