from flask_restplus import Namespace, Resource, fields
import json
from flask import Response
from Utils.serializer import serializer
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

api = Namespace('Charity',description='Charity related operations')
charity_fields=['COID','Name','PostalCode','Address','PhoneNumber']
@api.route('/')
class Initial(Resource):
    def get(self):
        '''Return all Charities'''
        
        cur.execute('''
            select * from charity_organization;
        ''')
        records = cur.fetchall() 
        records = serializer(charity_fields,records)
        return records


@api.route('/<id>')
@api.param('id','id of a charity')
@api.response(404,'charity not found')
class Charity(Resource):
    def get(self,id):
        '''Get members who helped this charity '''
      
        return{"Hello": id}