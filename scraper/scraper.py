import urllib2
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import ast
import pydot

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
                    if a_tag['href'] not in prereq_dict[url]:
                        prereq_dict[url].append(a_tag['href'])
    return prereq_dict

# generate overall graph, accept user input to change color color of subtree and generate new graph, with unique file name. try to avoid doing scraping more than once. store dict somewhere, reload it if it already exists?

def dict_from_file(filename):
    """Given a file containing the string representation of a dictionary,
    reconstruct the dictionary."""
    with open(filename, 'r') as f:
       s = f.read()
       a_dict = ast.literal_eval(s)
       return a_dict

def relabel(prereq_dict):
    """doc strings"""
    for url in prereq_dict:
        for prereq in prereq_dict[url]:
            prereq.replace('CDs/','').replace('.html','').replace('/','')
    url.replace('CDs/','').replace('.html','').replace('/','')
    return prereq_dict

if __name__ == '__main__':
    elec = 'http://web.uvic.ca/calendar2012/CDs/ELEC/CTs.html'
    csc = 'http://web.uvic.ca/calendar2012/CDs/CSC/CTs.html'
    
    try:
        with open('elec_dict.txt', 'r') as elec_f:
            elec_prereqs = dict_from_file('elec_dict.txt')
    except:
        elec_prereqs = prereqs(elec)
        with open('elec_dict.txt', 'w') as elec_f:
            elec_f.write(str(elec_prereqs))
    try:
        with open('csc_dict.txt', 'r') as csc_f:
            csc_prereqs = dict_from_file('csc_dict.txt')
    except:
        csc_prereqs = prereqs(csc)
        with open('csc_dict.txt', 'w') as csc_f:
            csc_f.write(str(csc_prereqs))

elec_dict = relabel(elec_prereqs)
csc_dict = relabel(csc_prereqs)
elec_graph = pydot.Dot(graph_name='elec', graph_type='digraph')
csc_graph = pydot.Dot(graph_name='csc', graph_type='digraph')

for course in elec_dict:
    for prereq in elec_dict[course]:
        elec_graph.add_edge(pydot.Edge(pydot.Node(course), pydot.Node(prereq)))
for course in csc_dict:
    for prereq in csc_dict[course]:
        csc_graph.add_edge(pydot.Edge(pydot.Node(course), pydot.Node(prereq)))
