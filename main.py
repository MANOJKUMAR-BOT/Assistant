from wtforms import StringField, validators
from flask_wtf import FlaskForm


class TopicForm(FlaskForm):
    query = StringField('Query', [validators.length(min=2, max=50)])
from bs4 import BeautifulSoup
import requests
import random

user_agents = [

            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',

]

def web_request(query):
    google_base_link = 'https://www.google.com/search?ei=LBEuYI-mEMyAyAPx26uICA&q={}&oq={}&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAELEDMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAOgoIABDqAhC0AhBDOgoILhDqAhC0AhBDOgQIABBDOgoIABCxAxCDARBDOggIABCxAxCDAToCCC46BwguEEMQkwI6BwgAELEDEEM6BAguEEM6BwgAEMkDEEM6BQgAEJIDOgUIABCRAjoECAAQA1DNcViwhAFggYYBaAFwAngAgAGXAogBnhKSAQYwLjEzLjKYAQCgAQGqAQdnd3Mtd2l6sAEKwAEB&sclient=gws-wiz&ved=0ahUKEwiP7Kbs7vLuAhVMAHIKHfHtCoEQ4dUDCA0&uact=5'
    header = {
        'User-Agent': random.choice(user_agents)
    }
    google_response = requests.get(google_base_link.format(query, query), headers=header, allow_redirects=True)
    return google_response.text


def scrape_data(response):
    page_object = BeautifulSoup(response, 'html.parser')
    head_response = page_object.find_all('div', {'class': 'xpdopen'})

    try:
        side_response = page_object.find('div', {'class': 'kno-rdesc'})
        question_response = side_response.find_all('span')[0].text

    except AttributeError:
        question_response = "Try with other keywords"

    return question_response    
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from Form import TopicForm
from Scraper import web_request, scrape_data



app = Flask(__name__)
app.config.from_mapping(SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
Bootstrap(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = TopicForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        query = form.query.data
        query_result = web_request(query)
        query_resonse = scrape_data(query_result)
        print(query_resonse)
        return render_template('Main.html', form=form, result=query_resonse)
    return render_template('Main.html', form=form)


if __name__ == '__main__':
    app.run()
