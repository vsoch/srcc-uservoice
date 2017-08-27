'''
utils.py: general utilities for analysis to look at UserVoice data
logs for research computing

@vsoch 9-2016
'''

import os
import simplejson
import json
from gvars import *

# General util / file functions
def write_file(filename,content,mode="wb"):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    filey = open(filename,mode)
    filey.writelines(content)
    filey.close()
    return filename


def write_json(json_obj,filename,mode="w",print_pretty=True):
    '''write_json will (optionally,pretty print) a json object to file
    :param json_obj: the dict to print to json
    :param filename: the output file to write to
    :param pretty_print: if True, will use nicer formatting   
    '''
    with open(filename,mode) as filey:
        if print_pretty == True:
            filey.writelines(json.dumps(json_obj, indent=4, separators=(',', ': ')))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def read_json(filename,mode='r'):
    '''read_json reads in a json file and returns
    the data structure as dict.
    '''
    with open(filename,mode) as filey:
        data = json.load(filey)
    return data


def read_file(filename,mode="r"):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    with open(filename,mode) as filey:
        content = filey.read()
    return content


def get(url,data=None,headers=None):
    '''get will use requests for a GET, hopefully don't need to use this if
    user-voice is fixed
    '''
    default_headers = { 'Content-Type': 'application/json', 
                        'Accept': 'application/json',  
                        'API-Client': 'uservoice-python-' + api_version }
    if headers != None:
        if isinstance(headers,dict):
            default_headers.update(headers)

    if data != None:
        response = requests.get(url,headers=headers,data=data)
    else:
        response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.json()
    return None   
