
# coding: utf-8

# In[2]:

import csv, sqlite3

con = sqlite3.connect("mumbai.db")
con.text_factory = str
cur = con.cursor()



cur.execute('''DROP TABLE IF EXISTS nodes;''')
con.commit()
# create nodes table
cur.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")
with open('nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp'])              for i in dr]

cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp)                 VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()



cur.execute('''DROP TABLE IF EXISTS nodes_tags;''')
con.commit()
#create nodes_tags table
cur.execute("CREATE TABLE nodes_tags (id, key, value, type);")
with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
con.commit()



cur.execute('''DROP TABLE IF EXISTS ways;''')
con.commit()
#Create ways table
cur.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
with open('ways.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
con.commit()



cur.execute('''DROP TABLE IF EXISTS ways_nodes;''')
con.commit()
#Create ways_nodes table
cur.execute("CREATE TABLE ways_nodes (id, node_id, position);")
with open('ways_nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)
con.commit()



cur.execute('''DROP TABLE IF EXISTS ways_tags;''')
con.commit()
#Create ways_tags table
cur.execute("CREATE TABLE ways_tags (id, key, value, type);")
with open('ways_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
con.commit()


# In[7]:

#number of nodes
cur.execute("SELECT COUNT(*) FROM nodes")
results = cur.fetchall()
print results


# In[8]:

#number of ways
cur.execute("SELECT COUNT(*) FROM ways")
results = cur.fetchall()
print results


# In[14]:

#Number of Unique users
cur.execute('''SELECT COUNT(DISTINCT(e.uid)) 
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;''')
results =cur.fetchall()
print results


# In[18]:

#Top contributing users
cur.execute('''SELECT e.user, COUNT(*) as num
FROM(SELECT user FROM nodes UNION ALL SELECT user FROM ways) e 
GROUP BY e.user 
ORDER BY num DESC
LIMIT 10;''')
results = cur.fetchall()
print results


# In[25]:

#Common ammenities
cur.execute('''
SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;''')
results =cur.fetchall()
print results


# In[36]:

#Popular cuisines
cur.execute('''SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC ;''')
results = cur.fetchall()
print results


# In[37]:

#Biggest religion:
cur.execute('''SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 1;''')
results = cur.fetchall()
print results


# In[ ]:



