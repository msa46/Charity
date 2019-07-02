from flask_restplus import Namespace, Resource, fields, abort
import json
from flask import Response
from Utils.serializer import serializer
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

api = Namespace('NonFinancial',description='NonFinancial related operations')
non_financial_insertion_model=api.model('Adding Nonfinancial object',{
    "NCID":fields.Integer(description="Non-cash ID",required=True),
    "Value":fields.Integer(description="Amount",required=True),
    "Unit":fields.String(description="unit of the aid given"),
    "Name":fields.String(description="unit of the aid given"),
    "Number":fields.String(description='date of creation/transaction')
})

Non_financial_aid_fields=['NCID','Value','Unit','Name','Number']
@api.route('/')
@api.response(409,'There is a nonfinancial object with this NCID')
@api.response(204,'Successfully created')
@api.expect(non_financial_insertion_model)
class NonFinancial(Resource):
    def post(self):
        '''Create nonfinancial object'''
        data = api.payload
        cur.execute('''
        select * from Non_cash_aid
        where NCID=%s
        ''',(data["NCID"],))
        non_financial_object= cur.fetchall()
        if(len(non_financial_object) == 1):
            return None,409
        cur.execute('''
        insert into Non_cash_aid values(%s,%s,%s,%s,%s)
        ''',(data["NCID"],data["Value"],data["Unit"],data["Name"],data["Number"],))
        return None,204