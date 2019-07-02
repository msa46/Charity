from flask_restplus import Namespace, Resource, fields, abort
import json
from flask import Response
from Utils.serializer import serializer
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

api = Namespace('Member',description='Member related operations')
memeber_insertion_model=api.model('Addition of member',{
            "SSN":fields.Integer(description="Social security number",required=True),
            "User_name": fields.String(description="User name",required=True),
            "First_name": fields.String(description="First name",required=True),
            "Last_name":fields.String(description="Last name", required=True) ,
            "Date_of_birth":fields.String(description="Date of birth", required=True) ,
            "Email":fields.String(description="Email",required=True) ,
            "Password":fields.String(description="Password",required=True)
})


financial_donate_insertion_model=api.model('Addiootion for FDonate table without id',{
    "CID":fields.Integer(description="Campaign ID"),
    "Amount":fields.Integer(description="Amount",required=True),
    "Unit":fields.String(description="unit of the aid given"),
    "Date":fields.String(description='date of creation/transaction')
})
non_financial_insertion_model=api.model('Adding Nonfinancial object',{
    "CID":fields.Integer(description="Campaign ID"),
    "Value":fields.Integer(description="Amount",required=True),
    "Unit":fields.String(description="unit of the aid given"),
    "Name":fields.String(description="unit of the aid given"),
    "Number":fields.Integer(description='date of creation/transaction')
})
member_fields=['SSN','User_name','First_name','Last_name','Date_of_birth','Email', 'Password']

@api.route('/')
@api.response(409,'There is a member object with this SSN')
@api.response(204,'Successfully created')
@api.expect(memeber_insertion_model)
class Member(Resource):
    def post(self):
        '''Add a new member'''
        data = api.payload

        cur.execute('''
        select * from Member
        where SSN = %s
        ''',(data["SSN"],))
        member = cur.fetchall()
        if(len(member) == 1):
            return None,409
        cur.execute('''
        insert into member values(%s,%s,%s,%s,%s,%s,%s)
        ''',(data["SSN"],data["User_name"],data["First_name"],data["Last_name"],data["Date_of_birth"],data["Email"],data["Password"],))
        conn.commit()

        return None,204
@api.route('/<id>')
@api.param('id','SSN of a member')
@api.response(201,'Successfully donated')
class Donate(Resource):
    @api.expect(financial_donate_insertion_model)
    def post(self,id):
        '''Make a financial donate'''
        data = api.payload
        cur.execute('''
        select FID from financial_aid order by FID desc limit 1 ;
        ''')
        
        FID = cur.fetchall()[0][0] + 1
        
        cur.execute('''
            insert into financial_aid values(%s,%s,%s,%s)
        ''',(FID,data["Amount"],data["Unit"],data["Date"]))
        conn.commit()
        
        cur.execute('''
        insert into FDonate values(%s,%s,%s)
        ''',(id,FID,data["CID"]))
        conn.commit()

        return 201,None
    @api.expect(non_financial_insertion_model)
    def put(self,id):
        '''Make non financial donation '''
        data = api.payload
        cur.execute('''
            select NCID from non_cash_aid order by NCID desc limit 1 ;
            ''')
        NCID = cur.fetchall()[0][0] + 1
        cur.execute('''
        insert into Non_cash_aid values(%s,%s,%s,%s,%s)
            ''',(NCID,data["Value"],data["Unit"],data["Name"],data["Number"],)
        )
        conn.commit()

        cur.execute('''
        insert into NCDONATE values(%s,%s,%s)
        ''',(id,NCID,data["CID"]))
        conn.commit()

        return None,201