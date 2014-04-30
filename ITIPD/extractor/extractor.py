from bs4 import BeautifulSoup, Tag
import re
import psycopg2
from os import listdir
from os.path import isfile, join

def get_list_of_filepath(mypath):
    pathlist = []
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles:
        file = mypath + file
        pathlist.append(file)
    return pathlist


def bs_preprocess(html):
    """remove distracting whitespaces and newline characters
    (c) mail-group of beautifulsoup4"""
    pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
    html = re.sub(pat, '', html)  # remove leading and trailing whitespaces
    html = re.sub('\n', ' ', html)  # convert newlines to spaces
    # this preserves newline delimiters
    html = re.sub('[\s]+<', '<', html)  # remove whitespaces before opening tags
    html = re.sub('>[\s]+', '>', html)  # remove whitespaces after closing tags
    return html


def summarize_placeholders(parent, string):
    """ removes multiple placeholders if they are next to each other"""
    for elem in parent.find_all("p"):
        while isinstance(elem.next_sibling,
                         Tag) and elem.next_sibling.name == 'p' and elem.text == string and elem.next_sibling.text == string:
            elem.next_sibling.extract()


def find_parents(childs):
    """ finds the parent of each BeautifulSoup-Element given in a list (childs).
    in case of multiple childs having the same parent, the index of the parent 
    will be returned for each element after the first"""
    parents = []
    for child in childs:
        b_found = False
        for parent in parents:
            foundParent = child.findParent()
            if foundParent == parent:
                parents.append(parents.index(parent))
                b_found = True
                break
        if not b_found:
            parents.append(child.findParent())
    return parents


def offset(elements):
    """get the offsets of the given element"""
    startoffset = []
    endoffset = []
    length = 0
    for elem in elements:
        AllPrevious = elem.findAllPrevious()
        for previous in AllPrevious:
            if any(previous in p.findAllPrevious() for p in AllPrevious):
                continue
            length += len(str(previous))
        startoffset.append(length)
        endoffset.append(length + len(str(elem)))
        length = 0
    return (startoffset, endoffset)


def file_to_soup(path):
    """open a file and make a soup out of that"""
    g = open(path, "r")
    data = g.read()
    soup = BeautifulSoup(bs_preprocess(data))
    return soup


def grab_elements(soup, elem, attr1, attr2):
    """grabs the different elemens with the given attributes out of a soup"""
    return soup.find_all([elem], attrs={attr1: [attr2]})


def grab_all(soup):
    methods = grab_elements(soup, "dl", "class", "method")
    functions = grab_elements(soup, "dl", "class", "function")
    describtions = grab_elements(soup, "dl", "class", "describe")
    classmethods = grab_elements(soup, "dl", "class", "classmethod")
    staticmethods = grab_elements(soup, "dl", "class", "staticmethod")
    sections = grab_elements(soup, "div", "class", "sections")
    classes = grab_elements(soup, "dl", "class", "class")
    attributes = grab_elements(soup, "dl", "class", "attribute")
    datas = grab_elements(soup, "dl", "class", "data")

    #    return methods + functions + describtions + classmethods + staticmethods + sections + classes + attributes + datas

    #def placeholding(allunits):
    ###define placeholders
    method_string = '[method(s) removed here]'
    function_string = '[function(s) removed here]'
    describe_string = '[descriptions removed here]'
    classmethod_string = '[classmethod removed here]'
    staticmethod_string = '[staticmethod removed here]'
    class_string = '[class(es) removed here]'
    section_string = '[section removed here]'
    attribute_string = '[attribute removed here]'
    datas_string = '[data removed here]'

    for parent in methods + functions + describtions + classmethods + staticmethods + sections + classes + attributes + datas:
        ### set placeholders to duplicated elements ###
        for elem in parent.find_all('dl', {'class': 'method'}):
            tag = Tag(name='p')
            tag.string = method_string
            elem.replace_with(tag)
        for elem in parent.find_all('dl', {'class': 'function'}):
            tag = Tag(name='p')
            tag.string = function_string
            elem.replace_with(tag)
        for elem in parent.find_all('dl', {'class': 'describe'}):
            tag = Tag(name='p')
            tag.string = describe_string
            elem.replace_with(tag)
        for elem in parent.find_all('dl', {'class': 'classmethod'}):
            tag = Tag(name='p')
            tag.string = classmethod_string
            elem.replace_with(tag)
        for elem in parent.find_all('dl', {'class': 'staticmethod'}):
            tag = Tag(name='p')
            tag.string = staticmethod_string
            elem.replace_with(tag)
        for elem in parent.find_all('dl', {'class': 'class'}):
            tag = Tag(name='p')
            tag.string = class_string
            elem.replace_with(tag)
        for elem in parent.find_all('div', {'class': 'section'}):
            tag = Tag(name='p')
            tag.string = section_string
            elem.replace_with(tag)
        for elem in parent.find_all('dl', attrs={'class': 'attribute'}):
            tag = Tag(name='p')
            tag.string = attribute_string
            elem.replace_with(tag)
        for elem in parent.find_all('dl', attrs={'class': 'data'}):
            tag = Tag(name='p')
            tag.string = datas_string
            elem.replace_with(tag)

        ### summarize placeholders ###
        summarize_placeholders(parent, method_string)
        summarize_placeholders(parent, function_string)
        summarize_placeholders(parent, describe_string)
        summarize_placeholders(parent, classmethod_string)
        summarize_placeholders(parent, staticmethod_string)
        summarize_placeholders(parent, class_string)
        summarize_placeholders(parent, section_string)
        summarize_placeholders(parent, attribute_string)
        summarize_placeholders(parent, datas_string)
        return methods + functions + describtions + classmethods + staticmethods + sections + classes + attributes + datas


if __name__ == "__main__":
    mypath = "/home/sven/Bachelorarbeit/python-doc-extractor-for-cado/ITIPD/extractor/python-3.4.0-docs-html/"
    files = get_list_of_filepath(mypath)

    soup = file_to_soup("/home/sven/Bachelorarbeit/python-doc-extractor-for-cado/ITIPD/extractor/index.html")
    units = grab_all(soup)
    #    parents = find_parents(units)
    #    new_units = placeholding(units)

    ###output file
    f = open('test.html', 'w')  # needs to exist
    ###create the output
    print(units, file=f)
    print("**********", file=f)
    #    print(parents, file=f)
    f.close()


#########STORE SOMETHING INTO THE DATABASE#############
# conn = psycopg2.connect("dbname=mydb user=sven")
# cur = conn.cursor()
# parents = find_parents(results)
# i = 1
# for elem in results:
#     i = i + 1
#     fname = "None"
#     if isinstance(elem, Tag):
#         strng = elem.prettify()
#         cur.execute('INSERT INTO extractor_documentationunit  VALUES (%s,  %s,  %s,  %s,  %s, %s);',
#                     (i, strng, 0, fname, 0, 0))
# conn.commit()
# cur.close()
# conn.close()
