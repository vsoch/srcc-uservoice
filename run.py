'''
run.py: main run script for generating data for analysis
to look at UserVoice data logs for research computing

@vsoch 9-2016
'''

from api import SRCC
from utils import write_json

import pandas
import datetime
import os

# Create the client
srcc = SRCC()

# Get open and closed tickets
print("Using srcc client to obtain tickets...")
tickets = srcc.get_tickets()

# Save data
today = datetime.datetime.today().strftime('%Y-%m-%d')
if not os.path.exists('data'):
    os.mkdir('data')
write_json(tickets,'data/tickets-%s_raw.json' %today)

# Extract Features
# We are only going to use the first message, as we assume this
# is the main/first attempt to summarize the problem
columns = ['id','message','user','ticket_number','subject']
df = pandas.DataFrame(columns=columns)
for ticket in tickets:
    uid = ticket['id']
    if len(ticket['messages']) > 0:
        df.loc[uid,'id'] = uid
        message = ''.join([x['body'] for x in ticket['messages'] if x['body'] is not None])
        df.loc[uid,'message'] = ticket['messages'][0]['body']
        df.loc[uid,'ticket_number'] = ticket['ticket_number']    
        df.loc[uid,'subject'] = ticket['subject']
        user = ticket['contact'].get('email',None)
        if user is None:
            user = ticket['created_by']['email']
        df.loc[uid,'user'] = user
        for cf in ticket['custom_fields']:
            df.loc[uid,cf['key']] = cf['value']

df.to_csv('data/tickets_df_%s.tsv' %today, sep='\t')
