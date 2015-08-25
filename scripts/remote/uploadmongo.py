__author__ = 'lorenzo'

from pymongo import MongoClient
from config import _CRAWLING_POST, _TEMP_SECRET


connection = MongoClient('localhost', 27017)

db = connection.PTEST_BACKUP

results = db.crawling.find({}, {'_id': False})

"""
{
        "_id" : ObjectId("54dd29d2b396811764a01330"),
        "url" : "http://www.nasa.gov/pdf/55395main_12%20Earth%20Science.pdf",
        "home" : "NASA",
        "abstract" : "The mission of NASA's Earth Science ... and help answer qu
estions concerning many related aspects of ... forecasters in assessing particul
ate pollutio ...",
        "title" : "Earth Science - NASA",
        "keyword" : "aerosols+(pollution+aspects)",
        "stored" : true,
        "complete" : false,
        "key" : "aerosols (pollution aspects)",
        "hashed" : "aHR0cDovL3d3dy5uYXNhLmdvdi9wZGYvNTUzOTVtYWluXzEyJTIwRWFydGglMjBTY2llbmNlLnBkZg=="
}
"""


# upload via POST endpoint
from scripts.remote.remote import post_curling
import json

for record in results:
    post_curling(_CRAWLING_POST['local'], {'resource': json.dumps(record), 'pwd': _TEMP_SECRET}, display=True)

# close the connection to MongoDB
connection.close()
