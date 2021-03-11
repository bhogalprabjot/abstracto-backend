from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from Summarizer.code import summarizer
app = Flask(__name__)

api = Api(app)

article = []
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
            # print(result)
            if result:
                return {"summary": result}, 200
        return {"summary": None}, 404


api.add_resource(Article, '/article')
api.add_resource(Summary, '/summary',)

if __name__ == '__main__':
    app.run(debug=True)
