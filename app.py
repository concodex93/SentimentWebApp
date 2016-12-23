from flask import Flask, render_template, request
import re

from flask import flash
from textblob import TextBlob
from flask import redirect, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "C:\\Users\conor\PycharmProjects\SentimentWebApp"
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class WhatsApp:
    name = ""
    message = ""

    def __init__(self, name, message):
        self.name = name
        self.message = message

    def get_name(self):
        return self.name

    def get_message(self):
        return self.message


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        #print("A")
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')

            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            text = read_file()
            m_list = split_at_regex(text)
            sentiment_value = sentiment_eval(m_list)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return render_template("complete.html", sentiment_value=sentiment_value)


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    print(text)

    return text


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def read_file():
    file = open(UPLOAD_FOLDER + "/" + "WhatsApp_Chat_with_Connie_3.txt", encoding="utf8")
    text = file.read()
    print(text)

    return text


def split_at_regex(text):
    whats_app_list = []
    content = text
    pattern = r"\d{2}\/\d{2}\/\d{4}, \d{2}:\d{2} - "
    temp_list = re.split(pattern, content)

    for t in temp_list:
        index = t.find(":")
        name = t[:index]
        message = t[index + 1:]
        whats_app = WhatsApp(name, message)
        whats_app_list.append(whats_app)

        #print("name: " + str(name))
        #print("message: " + str(message))

    return whats_app_list


def sentiment_eval(m_list1):

    name_to_analyze = my_form_post()
    print(name_to_analyze)
    text = ""
    error_message = "The name you entered was not found :/"

    for o in m_list1:
        if o.get_name() == name_to_analyze:
            text = text + o.get_message()
            print(text)

    if text == "":
        value = error_message
        print("X")
    else:
        tb1 = TextBlob(text)
        value = tb1.sentiment
        print("Y")
    return value


if __name__ == '__main__':
    app.run(debug=True)
