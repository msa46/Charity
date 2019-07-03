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
    "Number":fields.Integer(description='date of creation/transaction')
})

non_financial_need_model=api.model('Adding Nonfinancial need',{
    "NCID":fields.Integer(description="Non-cash ID",required=True),
    "CID":fields.Integer(descriptoin="Campaign ID", required=True)
})
Non_financial_aid_fields=['NCID','Value','Unit','Name','Number']
@api.route('/')
@api.response(409,'There is a nonfinancial object with this NCID')
@api.response(400,'there is no non financial object with this NCID ')
@api.response(404,'there is no campaign object with this CID ')
@api.response(204,'Successfully created')
@api.expect(non_financial_insertion_model)
@api.response(201,'Success')
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
    @api.expect(non_financial_need_model)
    @api.response(409,'there is a nc object with theese primary keys')
    def put(self):
        '''Adding non financial need for a campaign'''
        data = api.payload
        cur.execute('''
        select * from Non_cash_aid
        where NCID=%s
        ''',(data["NCID"],))
        non_financial_object= cur.fetchall()
        if(len(non_financial_object) == 0):
            return None,400
        cur.execute('''
        select * from campaign
        where CID=%s
        ''',(data["CID"],))
        campaign= cur.fetchall()
        if(len(campaign) == 0):
            return None,404
        cur.execute('''
        select * from ncneed
        where CID = %s and NCID = %s;
        ''',(data["CID"],data["NCID"],))
        ncneed = cur.fetchall()
        if(len(ncneed) == 1):
            return None,409
        cur.execute('''
        insert into NCneed values(%s,%s)
        ''',(data["CID"],data["NCID"],))
        return None,201
        