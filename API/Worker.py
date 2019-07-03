from flask_restplus import Namespace, Resource, fields, abort
import json
from flask import Response
from Utils.serializer import serializer
import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

api = Namespace('Worker',description='Worker related operations')
worker_insertion_model=api.model('Addition of worker(member already created)',{
            "Date_of_entry":fields.String(description="Date of entry",example='2016-07-07 17:01:18',required=True) ,
            "Field":fields.String(description="Field of work",example='CE',required=True) ,
            "CID":fields.Integer(description="Campaign ID",required=True)
})



@api.route('/<id>')
@api.param('id','SSN')
@api.response(404,'no member with that SSN')
@api.response(409,'there is a worker with that SSN')
@api.response(204,'Successfully created')
class Worker(Resource):
    @api.expect(worker_insertion_model)
    def post(self,id):
        '''Adding a worker while he has been enlisted as a member'''
        data = api.payload
        cur.execute('''
        select * from Member
        where SSN = %s
        ''',(id,))
        member = cur.fetchall()
        if(len(member) == 0):
            return None,404

        cur.execute('''
            select * from worker
            where SSN = %s
            ''',(id,))
        worker = cur.fetchall()
        if(len(worker) == 1):
            return None,409
        cur.execute('''
        insert into worker values(%s,%s,%s,%s)
        ''',(id,data["Date_of_entry"],data["Field"],data["CID"],))
        conn.commit()

        return None,204