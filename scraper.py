import urllib2
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

elec_page = urllib2.urlopen('http://web.uvic.ca/calendar2012/CDs/ELEC/CTs.html').read()
csc_page = urllib2.urlopen('http://web.uvic.ca/calendar2012/CDs/CSC/CTs.html').read()
ul_tags = SoupStrainer('ul', class_='CDTL')
ul_soup = BeautifulSoup(elec_page+csc_page, 'html.parser', parse_only=ul_tags)

prereq_dict = {}

a_tags = ul_soup.find_all('a')
for a in a_tags:
    prereqs[a['href']] = []

prefix_url = u'http://web.uvic.ca/calendar2012/'
p_tags = SoupStrainer('p')

for url in prereqs.keys(): # DOES THIS LOOK AT PREREQS OF PREREQS??
    next_page = urllib2.urlopen(prefix_url+url).read()
    next_soup = BeautifulSoup(next_page, 'html.parser', parse_only=p_tags)
    
    for tag in next_soup:
        if tag.b and u'requisites' in tag.b.string:
            for a_tag in tag.find_all('a'):
                if a_tag['href'] not in prereqs: prereqs[a_tag['href']] = []
                if (a_tag['href'], url) not in prereqs[url]:
                    prereqs[url].append((a_tag['href'], url))

#f = file.open('prereqs.gv', 'w')

#opening_lines = '''
#/*
#* @command = dot
#*
#*/
#digraph g {
#rankdir = TB
#'''

#f.write(opening_lines)
