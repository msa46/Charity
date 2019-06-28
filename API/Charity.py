from flask_restplus import Namespace, Resource, fields, abort
import json
from flask import request
from flask import Response
from Utils.serializer import serializer
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

api = Namespace('Charity',description='Charity related operations')
charity_insertion_model=api.model('Adding a charity',{
        "COID":fields.Integer(description='Charity ID', required=True),
        "Name": fields.String(description='Name of charity', required=True),
        "PostalCode": fields.String(description='Postal code of charity', required=True),
        "Address": fields.String(description='Address of charity', required=True),
        "PhoneNumber": fields.String(description='Phone number of charity', required=True),
})

charity_fields=['COID','Name','PostalCode','Address','PhoneNumber']
member_fields=['SSN','User_name','First_name','Last_name','Date_of_birth','Email', 'Password']
campaign_fields=['CID','Name','Bank_account_number','Address','Purposs','COID','GoalID']
Worker_fields=['SSN','Date_of_entry','Field','CID']
Financial_aid_fields=['FID','Amount','Unit','Date']
Non_financial_aid_fields=['NCID','Value','Unit','Name','Number']
Destitute_fields=['SSN','First_name','Last_name','Date_of_birth','Care_taker_ID','Campaign_ID']
@api.route('/Add')
@api.expect(charity_insertion_model)
@api.response(204,'successfully added')
@api.response(400,'there is a charity with this COID')
class Add(Resource):
    def post(self):
        '''add a new charity '''
        data = api.payload
        cur.execute('''
        select * from charity_organization
        where COID = %s        
        ''',(data["COID"],))
        charity = cur.fetchall()
        if len(charity) == 1:
            return None, 400
        cur.execute('''
        insert into charity_organization values (%s,%s, %s,%s,%s);
        ''',(data['COID'],data['Name'],data['PostalCode'],data['Address'],data['PhoneNumber']))
        conn.commit()
        return None,204




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




    