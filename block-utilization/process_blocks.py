import csv
import json
with open('processed_blocks.csv', 'w', newline='') as csvfile:
    my_write = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    my_write.writerow([
        "block_number", 
        "size_in_bytes", 
        "tx_count", 
        "gas_used", 
        "gas_limit",
    ])
    with open('./block_data.csv') as f:
        f.readline()
        for line in f:
            data = line.split("\"")[1]
            data = data.replace("\'", "\"")
            data = json.loads(data)
            my_write.writerow([
                data["_field_1"],
                data["_field_2"],
                data["_field_3"],
                data["_field_4"],
                data["_field_5"],
            ])
