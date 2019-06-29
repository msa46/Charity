from flask_restplus import Namespace, Resource, fields, abort
import json
from flask import Response
from Utils.serializer import serializer
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

api = Namespace('Financial',description='Financial related operations')
financial_general_insertion_model=api.model('Adding financial object(general)',{
    "FID":fields.Integer(description="Financial ID",required=True),
    "Amount":fields.Integer(description="Amount",required=True),
    "Unit":fields.String(description="unit of the aid given"),
    "Date":fields.String(description='date of creation/transaction')
})

Financial_fields=["FID","Amount","Unit","Date"]
@api.route('/')
@api.response(409,'There is a financial object with this FID')
@api.response(204,'Successfully created')
class Financial(Resource):
    @api.expect(financial_general_insertion_model)
    def post(self):
        '''Create a Financial Object'''
        data = api.payload
        cur.execute('''
        select * from financial_aid
        where FID=%s
        ''',(data["FID"],))
        financial_object = cur.fetchall()
        if(len(financial_object) == 1):
            return None,409
        cur.execute('''
            insert into financial_aid values(%s,%s,%s,%s)
        ''',(data["FID"],data["Amount"],data["Unit"],data["Date"]))
        conn.commit()
        return None,204
