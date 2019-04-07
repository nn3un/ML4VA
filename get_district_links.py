from urllib import request
from bs4 import BeautifulSoup
import re

def get_district_links(url):
    begin_url = "https://nces.ed.gov/ccd/districtsearch/"
    page = request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    a_tags = soup.find_all(href=re.compile("^district_detail"))
    return [begin_url + tag['href'] for tag in a_tags]

root_url = 'https://nces.ed.gov/ccd/districtsearch/district_list.asp?Search=1&details=1&InstName=&DistrictID=&Address=&City=&State=51&Zip=&Miles=&County=&PhoneAreaCode=&Phone=&DistrictType=1&DistrictType=2&DistrictType=3&DistrictType=4&DistrictType=5&DistrictType=6&DistrictType=7&DistrictType=8&NumOfStudents=&NumOfStudentsRange=more&NumOfSchools=&NumOfSchoolsRange=more'
NUM_OF_PAGES = 14
f = open('district_links.txt', 'w+')

for i in range(NUM_OF_PAGES):
    page_url = root_url + '&DistrictPageNum=' + str(i+1)
    parsed_district_links = get_district_links(page_url)
    for district_link in parsed_district_links:
        f.write(district_link + '\n')

f.close()

