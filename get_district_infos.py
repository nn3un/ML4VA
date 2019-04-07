import re
from urllib import request

from bs4 import BeautifulSoup
from cffi.backend_ctypes import unicode

f = open('district_links.txt', 'r')
lines = f.readlines()
district_links = [line.strip() for line in lines]
districts = []
BASE_URL = 'https://nces.ed.gov/ccd/districtsearch/'

for link in district_links:
    district = {}
    page = request.urlopen(link)
    soup = BeautifulSoup(page, "html.parser")
    district_name_label = soup.find(string=re.compile('District Name'))
    district['district_name'] = district_name_label.find_parent('b').find_next_sibling('font').text
    district_id_label = soup.find(string=re.compile('State District ID'))
    district_id_pre_process = district_id_label.find_parent('b').find_next_sibling('font').text
    district['district_id'] = district_id_pre_process[district_id_pre_process.find('-') + 1:]
    total_schools_label = soup.find(string=re.compile('Total Schools'))
    district['total_school'] = total_schools_label.find_parent('b').find_next_sibling('font').text
    locale_label = soup.find(string=re.compile('Locale'))
    district['locale'] = unicode(locale_label.find_parent('font').contents[1])
    total_students_label = soup.find(string=re.compile('Total Students'))
    district['total_students'] = total_students_label.find_parent('td').fetchNextSiblings('td')[1].text
    fte_label = soup.find(string=re.compile('FTE'))
    district['fte'] = fte_label.find_parent('td').fetchNextSiblings('td')[1].text
    student_teacher_ratio_label = soup.find(string=re.compile('Student/Teacher Ratio'))
    district['student_teacher_ratio'] = student_teacher_ratio_label.find_parent('td').fetchNextSiblings('td')[1].text
    ell_label = soup.find(string=re.compile('ELL'))
    district['ell'] = ell_label.find_parent('td').fetchNextSiblings('td')[1].text
    iep_label = soup.find(string=re.compile('IEP'))
    district['iep'] = iep_label.find_parent('td').fetchNextSiblings('td')[1].text
    fiscal_link = BASE_URL + soup.find('a', string=re.compile('Fiscal'))['href']
    fiscal_page = request.urlopen(fiscal_link)  # jumping to the fiscal page
    fiscal_soup = BeautifulSoup(fiscal_page, "html.parser")
    total_revenue_label = fiscal_soup.find(string=re.compile('Total Revenue'))
    if total_revenue_label is not None:
        district['total_revenue'] = total_revenue_label.find_parent('td').findNextSibling('td').text[1:].replace(',',                                                                                                         '')  # getting rid of the dollar sign and commas
    total_expenditures_label = fiscal_soup.find(string=re.compile('Total Expenditures'))
    if total_expenditures_label is not None:
        district['total_expenditures'] = total_expenditures_label.find_parent('td').findNextSibling('td').text[1:].replace(
        ',', '')  # getting rid of the dollar sign and comma
    districts.append(district)

import csv

with open('district_info.csv', mode='w+') as file:
    fieldnames = ['district_id', 'district_name', 'district_id', 'total_school', 'fte', 'ell', 'iep', 'total_revenue',
                  'total_expenditures', 'student_teacher_ratio', 'locale', 'total_students']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(districts)


pass
