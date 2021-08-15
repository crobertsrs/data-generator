import requests
import random
import time

API = r"https://maizepages.umich.edu/api/discovery/search/organizations"

max_items = 1640 # The site says this is the number of groups

with open('student_organizations_raw.txt', 'w') as f:
    f.write("[")      

    for i_skip in range(0,1640,10):

        # Random delay just in case they are limiting API calls
        delay_interval = random.randint(1,4)

        # Parameters
        payload = {
            'orderBy[0]': 'UpperName asc', 
            'top': 10,
            'skip': i_skip
        }

        # Make a requests call using GET (including parameters)
        r = requests.get(API, params=payload)

        # Get the returns json data
        json_data = r.json()
        f.write(r.text) 
        if i_skip < 1630:     
            f.write(",")    

        # Give it just a second in case they are limiting API calls
        time.sleep(delay_interval)
    
    f.write("]")      

