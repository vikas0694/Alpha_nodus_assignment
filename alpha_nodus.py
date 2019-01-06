import csv
import json

csvfile = open('file.csv', 'r')
jsonfile = open('file.json', 'w')

jsonData = []

fieldnames = ("tracker_history_id","tracker_id","installation_id","tracker_status","timestamp","metadata")
reader = csv.DictReader( csvfile, fieldnames)
next(reader)

for row in reader:
    data = {
        "tracker_history_id": row["tracker_history_id"],
        "tracker_id": row["tracker_id"],
        "installation_id": row["installation_id"],
        "tracker_status": row["tracker_status"],
        "timestamp": row["timestamp"],
        "metadata": json.loads(row["metadata"])
    }   
    
    finalData = {
        "tracker_id": data["tracker_id"],
        "installation_id": data["installation_id"],
        "start_time": data["timestamp"],
        "end_time": data["metadata"]["restart_time"],
        "restart_reason": data["metadata"]["boot_reason"],
        "restart_count": data["metadata"]["restart_count"]
    }
    if row["tracker_history_id"] not in jsonData:
            if data["metadata"]["restart_time"] != 0:
                jsonData.append(finalData)
       
    out = json.dumps(jsonData, indent=4)
    f = open( 'file.json', 'w')
    f.write(out)
    
    f = open('file.json')
    data = json.load(f)
    f.close()

    f=csv.writer(open('output.csv','w'))
    f.writerow(['installation_id', 'tracker_id', 'start_time', 'end_time', 'restart_reason', 'restart_count'])
    for item in data:
        f.writerow([item['installation_id'],item['tracker_id'], item['start_time'], item['end_time'], item['restart_reason'], item['restart_count']])