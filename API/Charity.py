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
Worker_fields=['SSN','Date_of_entry','Field','CID']
Financial_aid_fields=['FID','Amount','Unit','Date']
Non_financial_aid_fields=['NCID','Value','Unit','Name','Number']
Destitute_fields=['SSN','First_name','Last_name','Date_of_birth','Care_taker_ID','Campaign_ID']
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

@api.route('/<id>/workers')
@api.param('id','id of a charity')
@api.response(404,'charity not found')
class Workers(Resource):
    def get(self,id):
        '''Get workers who work at this charity '''

        cur.execute('''
            select worker.* from  worker natural join campaign inner join charity_organization co on campaign.coid = co.coid
            where co.coid = %s;
        ''',(id,))
        workers=cur.fetchall()
        if(len(workers) == 0):
            abort(400,custom='no members')
        workers = serializer(Worker_fields,workers)
        print(workers)
        return workers
@api.route('/<id>/financial')
@api.param('id','id of a charity')
@api.response(404,'charity not found')
class Financial(Resource):
    def get(self,id):
        '''Get financial aids to a charity '''

        cur.execute('''
            select financial_aid.* from financial_aid natural join fdonate natural join campaign inner join charity_organization co on campaign.coid = co.coid
            where co.coid=%s ;
        ''',(id,))
        financial_aid=cur.fetchall()
        if(len(financial_aid) == 0):
            abort(400,custom='no members')
        financial_aid = serializer(Financial_aid_fields,financial_aid)
        return financial_aid

@api.route('/<id>/nonfinancial')
@api.param('id','id of a charity')
@api.response(404,'charity not found')
class Non_financial_aid(Resource):
    def get(self,id):
        '''Get non financial aids to a charity '''

        cur.execute('''
            select non_cash_aid.* from non_cash_aid natural join ncdonate inner join campaign c on ncdonate.cid = c.cid inner join charity_organization co on c.coid = co.coid
            where co.coid=%s;
        ''',(id,))
        non_financial_aid=cur.fetchall()
        if(len(non_financial_aid) == 0):
            abort(400,custom='no members')
        non_financial_aid = serializer(Non_financial_aid_fields,non_financial_aid)
        return non_financial_aid

@api.route('/<id>/destitute')
@api.param('id','id of a charity')
@api.response(404,'charity not found')
class Destitue(Resource):
    def get(self,id):
        '''Get destitute under a charity '''

        cur.execute('''
            select destitute.* from destitute natural join campaign inner join  charity_organization co on campaign.coid = co.coid
            where co.coid = %s;
        ''',(id,))
        destitutes=cur.fetchall()
        if(len(destitutes) == 0):
            abort(400,custom='no destitue')
        destitutes = serializer(Destitute_fields,destitutes)
        return destitutes




    