from bs4 import BeautifulSoup
import unittest
import requests
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.

try:
  cat_image = open("gallery.html",'r').text
except:
  cat_image = requests.get("http://newmantaylor.com/gallery.html").text
  f = open("gallery.html",'w')
  f.write(cat_image)
  f.close()

soup = BeautifulSoup(cat_image, 'html.parser')

all_imgs = soup.find_all('img')
# for image in all_imgs:
    # print(image.get('alt',"No alternative text provided!"))

######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.

try:
  nps_data = open("nps_gov_data.html",'r').read()
except:
  nps_data = requests.get("https://www.nps.gov/index.htm").text
  f = open("nps_gov_data.html",'w')
  f.write(nps_data)
  f.close()

nps_soup = BeautifulSoup(nps_data, 'html.parser')

get_state_data = nps_soup.find("ul",{"class":"dropdown-menu SearchBar-keywordSearch"})
# print (get_state_data)


# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure
# that the rest of the program can access.


state_list=['Michigan','Arkansas','California']
state_links = [nps_soup.find('a', text=x)['href'] for x in state_list]
state_elems=[]
for elem in state_links:
    state_elems.append("https://www.nps.gov" + elem)

for elem in state_elems:
    if "/mi/" in elem:
        mich_url = elem
    if "ar" in elem:
        ark_url = elem
    if "ca" in elem:
        cal_url = elem

# print (mich_url)
# TRY:
# To open and read all 3 of the files
# But if you can't, EXCEPT:
# Create a BeautifulSoup instance of main page data
# Access the unordered list with the states' dropdown
try:
    arkansas_data = open("arkansas_data.html",'r').read()
    california_data = open("california_data.html",'r').read()
    michigan_data = open("michigan_data.html",'r').read()
except:
    michigan_data = requests.get(mich_url).text
    f = open("michigan_data.html", 'w')
    f.write(michigan_data)
    f.close()
    california_data = requests.get(cal_url).text
    f = open("california_data.html", 'w')
    f.write(california_data)
    f.close()
    arkansas_data = requests.get(ark_url).text
    f = open("arkansas_data.html",'w')
    f.write(arkansas_data)
    f.close()



# ul = soup.find('ul',{"class":"dropdown-menu SearchBar-keywordSearch"})
# # Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method
# list_elems = ul.find_all("li")
# # print (list_elems)

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects
# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements
# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.
## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?
# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)
# And then, write each set of data to a file so this won't have to run again.




######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

mich_soup = BeautifulSoup(michigan_data,'html.parser')
ark_soup = BeautifulSoup(arkansas_data, 'html.parser')
cal_soup = BeautifulSoup(california_data, 'html.parser')


# print(mich_soup.prettify)

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...


## Define your class NationalSite here:

class NationalSite:
    def __init__(self, object):
        try:
            self.location = object.find("h4").text
        except:
            self.location = ""
        self.name = object.find("h3").text
        if object.find("h2").text == '':
            self.type = "None"
        else:
            self.type = object.find("h2").text
        try:
            self.description = object.find("p").text
        except:
            self.description = ""
        self.link = object.find("a").get("href")
        self.park_link = "https://www.nps.gov" + self.link + "index.htm"

    def __str__(self):
        return "{} | {}".format(self.name, self.location)

    def get_mailing_address(self):
        site_html = requests.get(self.park_link).text
        site_soup = BeautifulSoup(site_html, 'html.parser')
        address = site_soup.find("div",{"class":"mailing-address"})
        mail_stop = address.find('div', {'itemprop':'address'}).text.strip()
        real_address = mail_stop.replace("\n","/")
        return (real_address)

    def __contains__(self, x):
        if x in self.name:
            return True
        else:
            return False




## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:
#
f = open("sample_html_of_park.html",'r')
soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
sample_inst = NationalSite(soup_park_inst)
f.close()



######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.


michigan_natl_sites=[]
mich_parks = mich_soup.find("ul",{"id":"list_parks"})
MI_park_item = mich_parks.find_all("li",{"class":"clearfix"})

for park in MI_park_item:
    soup = BeautifulSoup(str(park),'html.parser')
    mich_national=NationalSite(soup)
    michigan_natl_sites.append(mich_national)

arkansas_natl_sites=[]
ark_parks = ark_soup.find("ul",{"id":"list_parks"})
AR_park_item = ark_parks.find_all("li",{"class":"clearfix"})
for park in AR_park_item:
    soup = BeautifulSoup(str(park),'html.parser')
    ark_national=NationalSite(soup)
    arkansas_natl_sites.append(ark_national)

california_natl_sites=[]
cal_parks = cal_soup.find("ul",{"id":"list_parks"})
CA_park_item = cal_parks.find_all("li",{"class":"clearfix"})
for park in CA_park_item:
    soup = BeautifulSoup(str(park),'html.parser')
    cal_national=NationalSite(soup)
    california_natl_sites.append(cal_national)


# ##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!
def csv_func(filename, listname):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name","Location","Type","Address","Description"])
        for x in listname:
            description_clean = x.description.strip()
            writer.writerow([x.name, x.location, x.type, x.get_mailing_address(), description_clean])

csv_func("arkansas.csv", arkansas_natl_sites)
csv_func("michigan.csv",michigan_natl_sites)
csv_func("california.csv",california_natl_sites)
