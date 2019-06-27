import json

def serializer(fields, records):
    # fields=['id', 'name']
    # records=[[1, 'ali'], [2, 'reza']]
    result = []
    
    for r in records: 
        rec  = {}
        for i in range(len(fields)): 
            rec[fields[i]] =  r[i] 
        result.append(rec)
    
    return result
