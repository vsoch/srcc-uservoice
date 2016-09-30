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
                api_key,api_secret = [x.strip('\n').strip(' ') for x in auth]

        return uservoice.Client(sub_domain, api_key, api_secret)    


    def get(self,url,params):
        '''get is a general function for a get call to the api at some url, 
        using some params
        :param url: the url to post to
        :param params: the parameters to use
        '''

        done = False   # handle pagination
        results = []
        page = 1
        count = 0
        api_url = "/api/%s/%s.json" %(api_version,url)

        # Loop through calls until we have no more
        while done == False:

            print('Retrieving page %s' %(page))
            res = self.client.get(api_url, params)
            results = results + res[url]

            # Update the count
            count = count + len(res[url])
 
            # Some calls just have 'records' as key...
            if 'records' in res['response_data']:
                if res['response_data']['records'] != page:
                    page = page + 1
                else:
                    done = True
 
            # Others have total records...
            elif 'total_records' in res['response_data']:
                if count < res['response_data']['total_records']:
                    page = page + 1
                else:
                    done = True

            # If we get here, the API is so inconsistent in return fields,
            # it's just safest to stop.
            else:
                print("Not clear if more records remain, stopping.")
                print("\n".join(res["response_data"].keys()))
                done = True

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

        # Parameters must be dictionary
        params = { 'sort': sort,
                   'page': page,
                   'filter':filter,
                   'per_page': per_page }

        articles = self.get('articles', params)
        return articles


    def get_tickets(self,per_page=500,filter="all",sort="newest",states=['open','closed']):
        '''get_tickets will return a list of tickets 
        :param per_page: the number of articles to return per page (default 500)
        :param filter: either all [default], published, or unpublished
        :param sort: sort by newest, oldest, instant_answers
        :param states: list of states to parse through (open,closed,spam)
        '''
        tickets = []
        for state in states:
            params = {'sort': sort,
                      'page': 1,
                      'filter':filter,
                      'per_page': per_page,
                      'state':state }

            res = self.get('tickets', params)
            tickets = tickets + res
        return tickets
