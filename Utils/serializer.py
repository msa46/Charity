import json
import datetime

def serializer(fields, records):
    result = []
    
    for r in records: 
        rec  = {}
        for i in range(len(fields)):
            if isinstance(r[i],datetime.date):
                 rec[fields[i]] = r[i].strftime("%d-%b-%Y (%H:%M:%S.%f)")
            else:
                rec[fields[i]] =  r[i] 
        result.append(rec)
    
    return result
