from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from Summarizer.summarizer import summarizer
from web_scrapper.scrapper import scrapper
from flask_cors import CORS
from ocr.ocr import ocr
from models import error, input
app = Flask(__name__)

# to allow CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)

articles = []
url = []


class Article(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('article',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    
    def post(self):
        data = Article.parser.parse_args()
        article = input.Input(data['article'])
        articles.clear()
        articles.append(article)
        return article.mapToJSON(), 201

class Summary(Resource):
    def get(self):
        if articles[0].text:
            result = summarizer(articles[0].text)
            articles.clear()
            # print(result)
            if result:
                return {"summary": result, "error": None}, 200
        # return {"summary": None}, 404
        e = error.Error("Invalid Text")
        return {"summary": None, "error": e.error_message}, 404


class WebScraper(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url',
                        type=str,
                        # required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = WebScraper.parser.parse_args()
        url.append(data['url'])
        articles.clear()
        if url[0]:
            text = scrapper(url[0])
            url_article = input.Input(text)
            articles.append(url_article)
            # articles.append(scrapper(url[0]))
            url.clear()
            if url_article.text!="Invalid URL":       
                # return text, 201
                return {"url": text, "error": None}, 201

            else:
                e = error.Error("Invalid URL")
                return {"url": None, "error": e.error_message}, 404
        else:
            e = error.Error("No URL found")
            return {"url": None, "error": e.error_message}, 404


class Ocr(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('imageUrl',
                        type=str,
                        # required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = Ocr.parser.parse_args()
        url.append(data['imageUrl'])
        print(url[0])
        articles.clear()
        if url[0]:
            text = ocr(url[0])
            ocr_article = input.Input(text)
            articles.append(ocr_article)
            # articles.append(ocr(url[0]))
            url.clear()
            # print(article[0])
            return {"imageUrl": text, "error": None}, 201
        else:
            e = error.Error("No image found")
            return {"imageUrl": None, "error": e.error_message}, 404


api.add_resource(Article, '/article')
api.add_resource(Summary, '/summary', )
api.add_resource(WebScraper, '/scrapper', )
api.add_resource(Ocr, '/image', )

if __name__ == '__main__':
    app.run(debug=True)
