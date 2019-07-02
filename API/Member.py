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
