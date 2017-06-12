
# coding: utf-8

# In[1]:

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import collections


# In[2]:

import os
datadir = "D:\OSM"
datafile ="sample3.osm"
mum_data = os.path.join(datadir,datafile)


# In[3]:

def count_tags(filename):
    tags = {}
    for event,elem in ET.iterparse(filename):
        if elem.tag in tags:
            tags[elem.tag] += 1
        else :
            tags[elem.tag] = 1
    return tags
mum_tags = count_tags(mum_data)
pprint.pprint(mum_tags)


# In[4]:

import re
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problem_chars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter('tag'):
            k = tag.get('k')
            if lower.search(k):
                keys['lower'] += 1
            elif lower_colon.search(k):
                keys['lower_colon'] += 1
            elif problem_chars.search(k):
                keys['problem_chars'] += 1
            else:
                keys['other'] += 1
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problem_chars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

mum_keys = process_map(mum_data)
pprint.pprint(mum_keys)


# In[ ]:



