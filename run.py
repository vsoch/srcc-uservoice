'''
run.py: main run script for generating data for analysis
to look at UserVoice data logs for research computing

@vsoch 9-2016
'''

from api import SRCC
from utils import write_json
import os

# Create the client
srcc = SRCC()

# Get open and closed tickets
print("Using srcc client to obtain tickets...")
tickets = srcc.get_tickets()

# Save data
if not os.path.exists('data'):
    os.mkdir('data')
    write_json(tickets,'data/tickets.json')
