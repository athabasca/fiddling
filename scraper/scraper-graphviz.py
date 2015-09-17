"""
Creates dot files to feed into graphviz by scraping the UVic course calendar.
Not terribly sophisticated.
To use:
python scraper.py
dot -Tsvg csc_prereqs.dot
Same for elec_prereqs.dot. Requires graphviz.
-Tformat option can take png, ps, etc.. Can give outfile name with -o.
Author: A. Witschi
Date: Feb 2013
"""

import urllib2
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def prereqs(url):
    """Scrapes courses and their prerequisites from the provided URL for a
    department overview page from the UVic academic calender website.
    Returns a dictionary with key-value pairs of format URL:[(URL,prereqURL), ...]"""

    page = urllib2.urlopen(url).read()
    ul_tags = SoupStrainer('ul', class_='CDTL')
    ul_soup = BeautifulSoup(page, 'html.parser', parse_only=ul_tags)

    prereq_dict = {}
    prereq_list = []

    a_tags = ul_soup.find_all('a')
    for a in a_tags:
        prereq_dict[a['href']] = []
        prereq_list.append(a['href'])

    prefix_url = u'http://web.uvic.ca/calendar2012/'
    p_tags = SoupStrainer('p')

    for url in prereq_list:
        next_page = urllib2.urlopen(prefix_url+url).read()
        next_soup = BeautifulSoup(next_page, 'html.parser', parse_only=p_tags)
        
        for tag in next_soup:
            if tag.b and u'requisites' in tag.b.string:
                for a_tag in tag.find_all('a'):
                    if a_tag['href'] not in prereq_dict:
                        prereq_dict[a_tag['href']] = []
                        prereq_list.append(a_tag['href'])
                    if (a_tag['href'], url) not in prereq_dict[url]:
                        prereq_dict[url].append((a_tag['href'], url))
    return prereq_dict

def make_dot_file(dictionary, filename):
    """doc strings"""
    
    f = open(filename, 'w')

    opening_lines = '''
digraph g {
rankdir = TB

'''
    f.write(opening_lines)
    for item in dictionary.keys():
        for (x,y) in dictionary[item]: f.write (label(x) + '->' + label(y) + '\n')
    f.write('}\n')

    f.close()

def label(url):
    """doc strings"""
    return url.replace('CDs/','').replace('.html','').replace('/','')

if __name__ == '__main__':
    elec = 'http://web.uvic.ca/calendar2012/CDs/ELEC/CTs.html'
    csc = 'http://web.uvic.ca/calendar2012/CDs/CSC/CTs.html'
    
    elec_prereqs = prereqs(elec)
    csc_prereqs = prereqs(csc)
    make_dot_file(elec_prereqs, 'elec_prereqs.dot')
    make_dot_file(csc_prereqs, 'csc_prereqs.dot')
  
