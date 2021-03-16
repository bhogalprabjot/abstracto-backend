from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from Summarizer.code import summarizer
from web_scrapper.scrapper import scrapper

app = Flask(__name__)

api = Api(app)

article = []
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
        article.append(data['article'])
        return data, 201


class Summary(Resource):
    def get(self):
        if article:
            result = summarizer(article[0])
            print(result)
            if result:
                return {"summary": result}, 200
        return {"summary": None}, 404


class web_scrapper(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = web_scrapper.parser.parse_args()
        url.append(data['url'])
        article.append(scrapper(url[0]))
        return article[0], 201


api.add_resource(Article, '/article')
api.add_resource(Summary, '/summary', )
api.add_resource(web_scrapper, '/scrapper', )

if __name__ == '__main__':
    app.run(debug=True)
