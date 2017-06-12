
# coding: utf-8

# In[6]:

import xml.etree.cElementTree as ET 
from collections import defaultdict
import re
import pprint


# In[7]:

osmfile_sample = "sample3.osm"
bank_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = ["Bank of India","HDFC Bank","Central Bank","Bank Of Maharashtra","Canara Bank","Axis Bank","ICICI Bank"]

mapping ={'hindusthan':'Hindustan',
          'vijya bank':'Vijaya Bank',
          'Union Bank':'Union Bank of India',
          'StateBank':'State Bank of India',
          'Union Bank':'Union Bank of India'
         }
            
            
            


# In[8]:

def audit_banks_type(bank_types, bank_name):
    m = bank_type_re.search(bank_name)
    if m:
        bank_type = m.group()
        if bank_type not in expected:
            bank_types[bank_type].add(bank_name)


def audit2(filename):

    bank_types = defaultdict(set)
    osm_file = open(filename, "r")
    for event, elem in ET.iterparse(osmfile_sample, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if (tag.get("k")=="amenity") and (tag.get("v")=="bank"):
                    for tag in elem.iter("tag"):
                        if (tag.get("k")=="name"):
                            audit_banks_type(bank_types, tag.attrib['v'])
                            tag.attrib["v"]=update_name_bank(tag.attrib["v"], mapping) 


    return bank_types


def update_name_bank(name, mapping):
    for bank_type in mapping:
        if bank_type in name:
            name = re.sub(r'\b' + bank_type+ r'\b\.?', mapping[bank_type],name)
    return name


# In[9]:

pprint.pprint(dict(audit2(osmfile_sample)))


# In[10]:

def string_case(s): # change string into titleCase except for UpperCase
    if s.isupper():
        return s
    else:
        return s.title()

# return the updated names
def update_name(name, mapping):
    name = name.split(' ')
    for i in range(len(name)):
        if name[i] in mapping:
            name[i] = mapping[name[i]]
            name[i] = string_case(name[i])
        else:
            name[i] = string_case(name[i])
    
    name = ' '.join(name)
   

    return name

update_street = audit2(osmfile_sample) 

# print the updated names
for street_type, ways in update_street.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "=>", better_name  


# In[ ]:



