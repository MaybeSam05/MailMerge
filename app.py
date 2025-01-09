from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/parameters', methods=['POST'])
def parameters():
    selected_platform = request.form['platform']
    return render_template('parameters.html', platform=selected_platform)

if __name__ == '__main__':
    app.run(debug=True)
