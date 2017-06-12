
# coding: utf-8

# In[1]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

osmfile_sample = "sample3.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "street": "Street",
            "Rd": "Road",
            "raod": "road",
            "Ln": "Lane",
            "Rd.": "Road",
            "Ave": "Avenue",
           "ave" : " Avenue",
          " Hwg" : "Highway",
           "Hwy" : "Highway",
           "Sq" : "Square"
            }


# In[2]:

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile_sample):
    osm_file = open(osmfile_sample, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib["v"])
    osm_file.close()
    return street_types


# In[3]:

pprint.pprint(dict(audit(osmfile_sample)))


# In[4]:

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

update_street = audit(osmfile_sample) 

# print the updated names
for street_type, ways in update_street.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "=>", better_name  


# In[ ]:



