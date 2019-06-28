from flask_restplus import Namespace, Resource, fields, abort
import json
from flask import request
from flask import Response
from Utils.serializer import serializer
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()


api = Namespace('Campaign',description='Champaign related operations')
campaign_insertion_model=api.model('Adding a campaign',{
        "CID":fields.Integer(description='Campaign ID', required=True),
        "Name": fields.String(description='Name of campaign', required=True),
        "Bank_account": fields.String(description='Banc account of campaign', required=True),
        "Address": fields.String(description='Address of campaign', required=True),
        "Purpose": fields.String(description='Purpose of campaign', required=True),        
        "COID":fields.Integer(description='Charity ID',required=True),
        "GoalID":fields.Integer(description='Goal ID',required=True),     
})
campaign_fields=['CID','Name','Bank_account_number','Address','Purposs','COID','GoalID']
@api.route('/Add')
@api.expect(campaign_insertion_model)
@api.response(204,'successfully added')
@api.response(409,'there is a campaign with this CID')
@api.response(400,'there is no charity with this COID')
@api.response(406,'there is no financial goal with this GoalID')
class Add(Resource):
    def post(self):
        '''add a new campaign '''
        data = api.payload
        cur.execute('''
        select * from campaign
        where CID = %s        
        ''',(data["CID"],))
        campaign = cur.fetchall()
        if len(campaign) == 1:
            return None, 409
        
        cur.execute('''
        select * from charity_organization
        where COID = %s        
        ''',(data["COID"],))
        charity = cur.fetchall()
        if len(charity) == 0:
            return None, 400

        cur.execute('''
        select * from financial_aid
        where FID = %s        
        ''',(data["GoalID"],))
        charity = cur.fetchall()
        if len(charity) == 0:
            return None, 406
        
        cur.execute('''
        insert into campaign values (%s, %s, %s, %s, %s, %s, %s);
        ''',(data['CID'],data['Name'],data['Bank_account'],data['Address'],data['Purpose'],data['COID'],data['GoalID']))
        conn.commit()
        print(data)
        return None,204