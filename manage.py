from flask import Flask
from API import api
app = Flask(__name__)
app.config['SWAGGER_UI_JSONEDITOR'] = True
api.init_app(app)

app.run(debug=True)


# api = Api(app)

# grammer=[{"word": "hello"}]
# accepted_grammer = api.model('My_grammer',{'Word': fields.String('The word.')})
# @api.route('/hello')
# class HelloWorld(Resource):
#     @api.marshal_with(accepted_grammer,envelope='the_data')
#     def get(self):
#         return grammer, 201
#     @api.expect(accepted_grammer)
#     def post(self):
#         new_word = api.payload
#         grammer.append(new_word)
#         return {'result': 'Word added.'}, 201
# if __name__ == '__main__':
#     app.run(debug=True)
