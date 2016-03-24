#!/usr/bin/env python

import houndify
import sys

if __name__ == '__main__':
  if len(sys.argv) < 4:
    print "Usage: %s <CLIENT_ID> <CLIENT_KEY> '<QUERY>'" % sys.argv[0]
    sys.exit(0)

  CLIENT_ID = sys.argv[1]
  CLIENT_KEY = sys.argv[2]
  query = sys.argv[3]

  requestInfo = {
    'ClientID': CLIENT_ID,
    ## Pretend we're at SoundHound HQ.  Set other fields as appropriate
    'Latitude': 37.388309, 
    'Longitude': -121.973968
  }

  client = houndify.TextHoundClient(CLIENT_ID, CLIENT_KEY, "test_user", requestInfo)
  response = client.query(query)
  print response 