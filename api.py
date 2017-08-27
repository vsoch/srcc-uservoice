'''
api.py: class to hold an api client and perform calls to
srcc uservoice client

@vsoch 9-2016
'''

import os
import requests
import uservoice

from utils import read_file
from gvars import *


class SRCC:

    def __init__(self,api_key=None,api_secret=None,sub_domain=None):
        self.client = self.authenticate(api_key=api_key,
                                        api_secret=api_secret,
                                        sub_domain=sub_domain)

    def __str__(self):
        return "<%s:client>" %(self.subdomain)

    def __unicode__(self):
        return "<%s:client>" %(self.subdomain)


    def authenticate(self,api_key=None,api_secret=None,sub_domain=None):

        # Did the user provide a subdomain?
        if sub_domain == None:
            sub_domain = subdomain
        self.subdomain = sub_domain

        # Read in api key from secrets?
        if api_key == None:
            if os.path.exists('.secrets'):
                auth = read_file(".secrets")
                api_key,api_secret = [x.strip(' ') for x in auth.split('\n') if x]

        return uservoice.Client(sub_domain, api_key, api_secret)    


    def get(self, endpoint, page=1, per_page=500, filter="all", sort="newest", state="closed"):
        '''get is a general function for a get call to the api at some url, 
        using some params

        Parameters
        ==========
        :param endpoint: the url endpoint (eg, tickets)
        :param page: starting page
        :param per_page: results per page
        :param filter: filter for results
        :param sort: sort results by
        '''

        done = False   # handle pagination
        results = []

        count = 0
        api_url = "/api/%s/%s.json" %(api_version,endpoint)

        # Loop through calls until we have no more
        while done == False:

            url = self.client.api_url + api_url
            url += '?client=' + self.client.api_key
            url += '&page=' + str(page)
            url += '&per_page=' + str(per_page)
            url += '&sort=' + sort
            url += '&state=' + state
            url += '&filter=' + filter

            print('Retrieving page %s' %(page))
            print(url)

            res = requests.get(url, 
                               headers=self.client.default_headers, 
                               auth=self.client.oauth)

            if res.status_code == 200:
                res = res.json()
                results = results + res[endpoint]
                count = count + len(res[endpoint])
                total = res['response_data'].get('records',res['response_data'].get('total_records'))

                # Should we keep going?
                if count < total:
                    page = page + 1
                else:
                    done = True
            else:
                print('Error with page %s:%s' %(page,url))


        return results


    def post_ticket(self,email,subject,message):
        '''post_ticket will post a ticket to the help desk
        :param email: the from email address
        :param subject: the subject of the email
        '''

        # Populate the ticket
        ticket = {'subject': subject,
                  'message': message }

        return self.client.post("/api/v1/tickets.json", {
                                'email': 'vsochat@stanfod.edu',
                                'ticket': ticket })['ticket']


    def get_articles(self,per_page=500,filter="all",sort="newest"):
        '''get_articles will return a list of articles 
        :param per_page: the number of articles to return per page (default 500)
        :param filter: either all [default], published, or unpublished
        :param sort: sort by newest, oldest, instant_answers
        '''
        return self.get('articles', page=page, per_page=per_page, filter=filter, sort=sort)


    def get_tickets(self,per_page=500,filter="all",sort="newest",get_open=True,get_closed=True):
        '''get_tickets will return a list of tickets 
        :param per_page: the number of articles to return per page (default 500)
        :param filter: either all [default], published, or unpublished
        :param sort: sort by newest, oldest, instant_answers
        :param get_open: retrieve open (open,closed,spam)
        :param get_closed: retrieve closed
        '''
        states = []
        if get_closed:
            states.append('closed')
        if get_open:
            states.append('open')

        if len(states) == 0:
            bot.error("You must specify one or more states, open or closed.")
            sys.exit(1)
 
        tickets = []
        for state in states:
            res = self.get('tickets', sort=sort,
                                      page=1,
                                      filter=filter,
                                      per_page=per_page,
                                      state=state)

            tickets = tickets + res
        return tickets
