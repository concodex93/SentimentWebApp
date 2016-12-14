from flask import Flask, render_template, request
import re
from textblob import TextBlob

app = Flask(__name__)


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
    sentiment_value = "Something ... "
    if request.method == 'POST':
        f = request.files['file']
        text = f.filename
        m_list = split_at_regex(text)
        sentiment_value = sentiment_eval(m_list)
    return render_template("complete.html", sentiment_value=sentiment_value)


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

    return whats_app_list


def sentiment_eval(m_list1):
    text = ""

    for o in m_list1:
        if o.get_name() == "Conor Byrne":
            text = text + o.get_message()
    tb1 = TextBlob(text)
    value = tb1.sentiment

    return value


if __name__ == '__main__':
    app.run(debug=True)
