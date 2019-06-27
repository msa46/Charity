from flask_restplus import Namespace, Resource, fields, abort
import json
from flask import Response
from Utils.serializer import serializer
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

api = Namespace('Charity',description='Charity related operations')
charity_fields=['COID','Name','PostalCode','Address','PhoneNumber']
member_fields=['SSN','User_name','First_name','Last_name','Date_of_birth','Email', 'Password']
campaign_fields=['CID','Name','Bank_account_number','Address','Purposs','COID','GoalID']
@api.route('/<id>/campaigns')
@api.param('id','id of a charity')
@api.response(404,'charity not found')
class initial(Resource):
    def get(self,id):
        '''Get all campaigns of a charity'''
        
        cur.execute('''
                select campaign.* from campaign inner  join  charity_organization co on campaign.coid = co.coid
                where co.coid = %s;
        ''',(id,))
        records = cur.fetchall() 
        records = serializer(campaign_fields,records)
        return records


@api.route('/<id>/helpers')
@api.param('id','id of a charity')
@api.response(404,'charity not found')
class Charity(Resource):
    def get(self,id):
        '''Get members who helped this charity '''

        cur.execute('''
            select member.* from   member natural join fdonate natural  join campaign inner  join  charity_organization co on campaign.coid = co.coid
            where co.coid = %s;
        ''',(id,))
        members=cur.fetchall()
        if(len(members) == 0):
            abort(400,custom='no members')
        members = serializer(member_fields,members)
        return members


    