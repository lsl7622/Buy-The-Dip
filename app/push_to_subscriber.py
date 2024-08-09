<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Join the BUY THE DIP community!</title>
</head>
<body>
    <h1>Enter Email to Subscibe</h1>
    <form action="/submit" method="post">
        <label for="textInput">email dip:</label><br>
        <textarea id="textInput" name="textInput" rows="4" cols="50"></textarea><br><br>
        <input type="submit" value="Submit">
    </form>
</body>

from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Load HTML file content
with open('index.html', 'r') as file:
    html_content = file.read()

@app.route('/', methods=['GET'])
def index():
    return render_template_string(html_content)

@app.route('/submit', methods=['POST'])
def submit():
    text_input = request.form['textInput']

    # Write the text input to a .txt file
    with open('subscriber.txt', 'a') as f:
        f.write(text_input + '\n')

    return 'Text added to file! <a href="/">Go back</a>'

if __name__ == '__main__':
    app.run(debug=True)

python app.py

