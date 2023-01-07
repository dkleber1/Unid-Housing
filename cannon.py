from time import sleep
import requests
import os
from bs4 import BeautifulSoup

# Sending notification to Mac OS
def notify(title, text):
    os.system("""
              osascript -e 'display dialog "{}" with title "{}"'
              """.format(text, title))

# url = input("enter link: ")
urls = []
user_url = input("enter url (press return to finish): ")
while(user_url != ""):
    urls.append(user_url)
    user_url = input("enter url (press return to finish): ")

max_distance = input("Enter max distance (km), press return for none: ")

try:
    max_distance = float(max_distance)
except ValueError:
    max_distance = -1

# Existing postings
existing_postings = set()
    
for current_url in urls:
    page = requests.get(current_url)



    # Get html from page using .text
    # Use beautiful soup to convert raw html into parseable data
    parsed_page = BeautifulSoup(page.text,'html.parser')

    tr_elements = parsed_page.find_all('tr')[1:]

    # Loops through each posting hi! hi
    for i in tr_elements:
        # tr object is a posting, td object is a single attribute in a posting
        # Get all td elements
        td_elements = i.find_all('td')

        # Set variable as posting attribute
        address = td_elements[4].text

        existing_postings.add(address)

# Test case
existing_postings.remove('21 Halesmanor  Court , Guelph')
# existing_postings.remove('177  Harvard Road , #G, Guelph')


#26 Sydney Crescent , Guelph
while(True):
    sleep(15)
    
    for current_url in urls:
        page = requests.get(current_url)

        parsed_page = BeautifulSoup(page.text,'html.parser')

        tr_elements = parsed_page.find_all('tr')[1:]

        # Loops through each posting
        for i in tr_elements:
            # Get all td elements
            td_elements = i.find_all('td')

            # Set variables as posting attributes
            address = td_elements[4].text
            distance = td_elements[5].text
            # Check if address is new and either the distance or max distance is provided,
            # if both provided check if user distance is less than or equal to the max distance
            if(address not in existing_postings and ((distance == 'n/a' or max_distance == -1) or (float(distance[:-2]) <= max_distance))):
                start_date = td_elements[0].text
                end_date = td_elements[1].text
                listing_type = td_elements[2].text
                home_type = td_elements[3].text
                sublet = td_elements[6].text
                rooms = td_elements[7].text
                price = td_elements[9].text

                raw_string = """Address: {0}
                Start Date: {1}
                End Date: {2}
                Listing Type: {3}
                Home Type: {4}
                Distance: {5}
                Sublet: {6}
                Rooms: {7}
                Price: {8}
                """
                formatted_string = raw_string.format(address,start_date, end_date, listing_type, home_type, distance, sublet, rooms, price)
                notify("New Posting",formatted_string)
                existing_postings.add(address)