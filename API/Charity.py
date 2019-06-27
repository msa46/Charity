from flask_restplus import Namespace, Resource, fields
import json
from flask import Response
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

api = Namespace('Charity',description='Charity related operations')

@api.route('/')
class Initial(Resource):
    def get(self):
        '''Return all Charities'''
        
        cur.execute('''
            select * from charity;
        ''')
       
        return {"Hello": "word"}


@api.route('/<id>')
@api.param('id','id of a charity')
@api.response(404,'charity not found')
class Charity(Resource):
    def get(self,id):
        '''Get members who helped this charity '''
      
        return{"Hello": id}