'''
run.py: main run script for generating data for analysis
to look at UserVoice data logs for research computing

@vsoch 9-2016
'''

from api import SRCC
from utils import (
    write_json,
    get_custom_field
)

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
columns = ['id','message','user','ticket_number','subject', 'cluster']
df = pandas.DataFrame(columns=columns)
for ticket in tickets:
    uid = ticket['id']
    message = ticket['messages'][0]['body']
    ticket_number = ticket['ticket_number']
    cf = ticket['custom_fields']
    cluster = get_custom_field(cf,'System')[0]
    subject = ticket['subject']
    user = ticket['contact'].get('email',None)
    if user is None:
        user = ticket['created_by']['email']
    df.loc[uid] = [uid, message, user, ticket_number, subject, cluster]

count=dict()
for ticket in tickets:
    uid = ticket['id']
    if uid in count:
        count[uid] +=1
    else:
        count[uid] = 1

# Let's just save tickets text content for classification
text = []

for ticket in tickets:
    user = ticket['created_by']['email']

    # Let's save a little "timeseries" of messages
    user_messages = [x['plaintext_body'] for x in ticket['messages'] if x['sender']['email'] == user]
    admin_messages = [x['plaintext_body'] for x in ticket['messages'] if x['sender']['email'] != user]
    user_messages.reverse() # make chronologically ordered
    admin_messages.reverse()
    messages = {'user':user_messages,
                'admin':admin_messages}

    new_ticket = {"user":lookup[user],
                  "id":ticket["id"],
                  "date": ticket['created_at'],
                  "subject":ticket['subject'],
                  "messages":messages}

    anon_tickets.append(new_ticket)

# Note - we will still need to parse out non english terms, etc. to get rid of user names
write_json(anon_tickets,'data/tickets_anon.json')


anon_tickets = []
# Now save tickets based on unique user id
for ticket in tickets:
    user = ticket['created_by']['email']

    # Let's save a little "timeseries" of messages
    user_messages = [x['plaintext_body'] for x in ticket['messages'] if x['sender']['email'] == user]
    admin_messages = [x['plaintext_body'] for x in ticket['messages'] if x['sender']['email'] != user]
    user_messages.reverse() # make chronologically ordered
    admin_messages.reverse()
    messages = {'user':user_messages,
                'admin':admin_messages}

    new_ticket = {"user":lookup[user],
                  "id":ticket["id"],
                  "date": ticket['created_at'],
                  "subject":ticket['subject'],
                  "messages":messages}

    anon_tickets.append(new_ticket)

# Note - we will still need to parse out non english terms, etc. to get rid of user names
write_json(anon_tickets,'data/tickets_anon.json')
