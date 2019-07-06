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
        "Name": fields.String(description='Name of campaign', required=True),
        "Bank_account": fields.String(description='Banc account of campaign', required=True),
        "Address": fields.String(description='Address of campaign', required=True),
        "Purpose": fields.String(description='Purpose of campaign', required=True),        
        "COID":fields.Integer(description='Charity ID',required=True),
        "GoalID":fields.Integer(description='Goal ID',required=True),     
})
campaign_fields=['CID','Name','Bank_account_number','Address','Purposs','COID','GoalID']
Non_financial_aid_fields=['NCID','Value','Unit','Name','Number']
Financial_aid_fields=['FID','Amount','Unit','Date']
Destitute_fields=['SSN','First_name','Last_name','Date_of_birth','Care_taker_ID','Campaign_ID']
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
            order by CID desc limit 1
        ''')
        CID = cur.fetchall()[0][0] + 1
        
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
        ''',(CID,data['Name'],data['Bank_account'],data['Address'],data['Purpose'],data['COID'],data['GoalID']))
        conn.commit()
        return None,204


@api.route('/<id>/helps')
@api.param('id','id of a campaign')
@api.response(404,'campaign not found')
class helps(Resource):
    def get(self,id):
        'Get campaign informations and financial helps to a campaign'
        cur.execute('''
        select campaign.*,sum(financial_aid.amount) from campaign natural join fdonate natural join financial_aid
        where campaign.cid = %s group by campaign.cid ;
        ''',(id, ))
        helps = cur.fetchall()
        if (len(helps) == 0):
            abort(400,custom='no helps')
        added_field = campaign_fields + ['Helps']
        helps = serializer(added_field,helps)
        return helps

@api.route('/<id>/nonfinancial')
@api.param('id','id of a campaign')
@api.response(404,'campaign not found')
class Non_financial(Resource):
    def get(self,id):
        'Get campaign informations and financial helps to a campaign'
        cur.execute('''
        select campaign.*,sum(financial_aid.amount) from campaign natural join fdonate natural join financial_aid
        where campaign.cid = %s group by campaign.cid ;
        ''',(id, ))
        helps = cur.fetchall()
        if(len(helps) == 0):
            abort(400,custom='no need')
        helps = serializer(Non_financial_aid_fields,helps)
        return helps

@api.route('/<id>/financial')
@api.param('id','id of a campaign')
@api.response(404,'campaign not found')
class financial(Resource):
    def get(self,id):
        'Get financial helps to a campaign'
        cur.execute('''
        select financial_aid.* from financial_aid natural join fdonate natural join campaign
        where campaign.cid = %s;
        ''',(id, ))
        helps = cur.fetchall()
        if(len(helps) == 0):
            abort(400,custom='no helps')
        helps = serializer(Financial_aid_fields,helps)
        return helps

@api.route('/<id>/destitute')
@api.param('id','id of a campaign')
@api.response(404,'campaign not found')
class Destitute(Resource):
    def get(self,id):
        '''get destitutes under a campaign'''
        cur.execute('''
        select * from campaign
        where CID = %s        
        ''',(id,))
        campaign = cur.fetchall()
        if(len(campaign) ==0 ):
            return None,404
        cur.execute('''
            select destitute.* from destitute 
            where destitute.campaignid = %s ;
        ''',(id,))
        destitutes = cur.fetchall()
        if(len(destitutes) == 0):
            abort(400,custom='no destitutes')
        destitutes=serializer(Destitute_fields,destitutes)
        return destitutes