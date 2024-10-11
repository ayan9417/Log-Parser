import pandas as pd
from collections import defaultdict, Counter

flow_logs_file = 'flow_logs.txt'

with open(flow_logs_file, 'r') as file:
    log_data = file.read()

def parse_log_to_dict(log_data):
    log_entries = log_data.strip().split("\n")
    log_data_dict = []
    
    for entry in log_entries:
        fields = entry.split()
        log_dict = {
            'version': int(fields[0]),
            'account_id': int(fields[1]),
            'eni': fields[2],
            'src_ip': fields[3],
            'dst_ip': fields[4],
            'dstport': int(fields[5]),
            'srcport': int(fields[6]),
            'protocol': int(fields[7]),
            'packets': int(fields[8]),
            'bytes': int(fields[9]),
            'start': int(fields[10]),
            'end': int(fields[11]),
            'action': fields[12],
            'status': fields[13]
        }
        log_data_dict.append(log_dict)
    
    return log_data_dict

log_data_dict = parse_log_to_dict(log_data)

lookup_df = pd.read_csv('lookup_table.csv')

port_protocol_tag_mapping = defaultdict(list)
for _, row in lookup_df.iterrows():
    key = (row['dstport'], row['protocol'].lower())  
    port_protocol_tag_mapping[key].append(row['tag']) 

def get_protocol_name(protocol_num):
    if protocol_num == 6:
        return 'tcp'
    elif protocol_num == 17:
        return 'udp'
    elif protocol_num == 1:
        return 'icmp'
    else:
        return 'untagged'

for log in log_data_dict:
    protocol_name = get_protocol_name(log['protocol']).lower()
    key = (log['dstport'], protocol_name)
    log['tags'] = port_protocol_tag_mapping.get(key, ['untagged'])

df = pd.DataFrame(log_data_dict)


tags = [tag for log in log_data_dict for tag in log['tags']]

tag_count = Counter(tags)

with open('output.txt', 'w') as f:
    f.write("Tag Counts:\n")
    f.write("Tag,Count\n")
    for tag, count in tag_count.items():
        f.write(f"{tag},{count}\n")

port_protocol_combinations = [(log['dstport'], get_protocol_name(log['protocol']).lower()) for log in log_data_dict]

port_protocol_count = Counter(port_protocol_combinations)

with open('output.txt', 'a') as f:
    f.write("\nPort/Protocol Combination Counts:\n")
    f.write("Port,Protocol,Count\n")
    for combination, count in port_protocol_count.items():
        dstport, protocol = combination
        f.write(f"{dstport},{protocol},{count}\n")

print("Flow logs have been processed with the specified constraints, and the output.txt file has been updated.")
