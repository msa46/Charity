from flask_restplus import Namespace, Resource, fields, abort
import json
from flask import Response
from Utils.serializer import serializer
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

api =Namespace('Employee',description='Employee related operations')
employee_insertion_model=api.model('Addition of Employee(member already created',{
            "Date_of_entry":fields.String(description="Date of entry",example='2016-07-07 17:01:18',required=True) ,
            "Field":fields.String(description="Field of work",example='CE',required=True) ,
            "Salary":fields.Integer(description="Salary",example=100,required=True),
            "COID":fields.Integer(description="Charity ID",required=True)
}
)

@api.route('/<id>')
@api.response(404,'no member with that ssn')
@api.response(409,'there is an employee with that SSN')
@api.response(204,'Successfully created')
class Employee(Resource):
    @api.expect(employee_insertion_model)
    def post(self,id):
        '''Add a new employee'''
        data = api.payload
        cur.execute('''
        select * from Member
        where SSN = %s
        ''',(id,))
        member = cur.fetchall()
        if(len(member) == 0):
            return None,404

        cur.execute('''
            select * from employee
            where SSN = %s
            ''',(id,))
        employee = cur.fetchall()
        if(len(employee) == 1):
            return None,409
        print(data["Salary"])
        cur.execute('''
        insert into employee values(%s,%s,%s,%s,%s)
        ''',(id,data["Date_of_entry"],data["Field"],data["Salary"],data["COID"],))
        conn.commit()

        return None,204