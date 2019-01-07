# Importing libraries
import csv 
import json
import datetime

jsonData = [] # array to store json 
csvfile = open('file.csv', 'r') # open csv file in read mode
# define column list to read from csv file 
fieldnames = ("tracker_history_id","tracker_id","installation_id","tracker_status","timestamp","metadata")
reader = csv.DictReader(csvfile, fieldnames) # reading csv file 
next(reader) # to skip heading row of csv

# iterating reader to perform logic and validation
for row in reader:
    # forming raw json object
    data = {
        "tracker_history_id": row["tracker_history_id"],
        "tracker_id": row["tracker_id"],
        "installation_id": row["installation_id"],
        "tracker_status": row["tracker_status"],
        "timestamp": row["timestamp"],
        "metadata": json.loads(row["metadata"])
    }   
    
    # filtering and formatting data to get defined output
    finalData = {
        "tracker_id": data["tracker_id"],
        "installation_id": data["installation_id"],
        "start_time": datetime.datetime.fromtimestamp(float(data["timestamp"])/1000).strftime("%c"),
        "end_time": datetime.datetime.fromtimestamp((data["metadata"]["restart_time"])/1000).strftime("%c"),
        "restart_reason": data["metadata"]["boot_reason"],
        "restart_count": data["metadata"]["restart_count"]
    }

    if row["tracker_history_id"] not in jsonData: # checking if array is empty
            if data["metadata"]["restart_time"] != 0: # condition to exclude data which has restart_time = 0
                jsonData.append(finalData) # appending filtered object to array
       
    out = json.dumps(jsonData, indent=4) # dumping json data with indent
    f = open( 'file.json', 'w') # creating a new json file
    f.write(out) # writing into file
    
    f = open('file.json') # opening created json file 
    data = json.load(f) # loading file into varible
    f.close() 

    f = csv.writer(open('output.csv','w')) # creating new csv file
    # writing column headings
    f.writerow(['installation_id', 'tracker_id', 'start_time', 'end_time', 'restart_reason', 'restart_count'])

    # Iterating json data to write into csv file
    for item in data:
        # wrtiting row by row with defined column order
        f.writerow([item['installation_id'],item['tracker_id'], item['start_time'], item['end_time'], item['restart_reason'], item['restart_count']])