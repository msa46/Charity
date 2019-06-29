from flask_restplus import Namespace, Resource, fields, abort
import json
from flask import Response
from Utils.serializer import serializer
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

api = Namespace('Destitue', description='Destitute related operation')

destitute_insertion_model=api.model('Adding a destitue',{
            "SSN":fields.Integer(description="Social security number",required=True),
            "First_name": fields.String(description="First name",required=True),
            "Last_name":fields.String(description="Last name", required=True) ,
            "Date_of_birth":fields.String(description="Date of birth", required=True) ,
            "Care_takerID":fields.Integer(description="Care taker social security number",required=True) ,
            "CampaignID":fields.Integer(description="Campaign ID which Destitute is under",required=True)
})

Destitute_fields=['SSN','First_name','Last_name','Date_of_birth','Care_taker_ID','Campaign_ID']

@api.route('/Add')
@api.expect(destitute_insertion_model)
@api.response(409,'there is a destitute with this SSN')
@api.response(400,'there is no destitute with this SSN(as caretaker)')
@api.response(406,'there is no campaign with this CID')
class Add(Resource):
    def post(self):
        '''Add a new destitute'''
        data = api.payload
        cur.execute('''
        select * from destitute
        where SSN = %s        
        ''',(data["SSN"],))
        destitute = cur.fetchall()
        if len(destitute) == 1:
            return None, 409

        cur.execute('''
        select * from campaign
        where CID = %s        
        ''',(data["CampaignID"],))
        campaign = cur.fetchall()
        if len(campaign) == 0:
            return None, 406
        
        cur.execute('''
        select * from destitute
        where SSN = %s        
        ''',(data["Care_takerID"],))
        care_taker = cur.fetchall()
        if len(care_taker) == 0:
            return None, 400
        
        cur.execute('''
        insert into destitute values (%s, %s, %s, %s, %s, %s);
        ''',(data['SSN'],data['First_name'],data['Last_name'],data['Date_of_birth'],data['Care_takerID'],data['CampaignID']))
        conn.commit()

        return None,204
@api.route('/<id>/care_taker')
@api.param('id','id of a detitute')
@api.response(404,'Destitute not found')
class care_taker(Resource):
    def get(self,id):
        '''Get destitutes under a certin care taker'''
        cur.execute('''
        select d.* from destitute d inner join destitute dr on d.ssn =dr.care_takerid
        where d.care_takerid = %s;
        ''',(id, ))
        care_taker=cur.fetchall()
        if(len(care_taker) == 0):
            abort(400,custom='no destitute')
        care_taker=serializer(Destitute_fields,care_taker)
        return care_taker

@api.route('/<id>/reason')
@api.param('id','id of a detitute')
@api.response(404,'Destitute not found')
class Reason(Resource):
    def get(self,id):
        '''Get destitutes reason for being in campaign'''
        cur.execute('''
        select destitute.* ,destitute_reason.reason from destitute natural join destitute_reason
        where destitute.ssn = %s;
        ''',(id, ))
        reason=cur.fetchall()
        if(len(reason) == 0):
            abort(400,custom='no reason mentioned')
        reason_fields = Destitute_fields + ["Reason"]
        reason=serializer(reason_fields,reason)
        return reason
