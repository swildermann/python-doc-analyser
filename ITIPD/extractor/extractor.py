from bs4 import BeautifulSoup, Tag
import re
import psycopg2
from os import listdir
from os.path import isfile, join
import copy


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
    # for child in childs:
    #     b_found = False
    #     for parent in parents:
    #         foundParent = child.findParent()
    #         if foundParent == parent:
    #             parents.append(parents.index(parent))
    #             b_found = True
    #             break
    #     if not b_found:
    #         parents.append(child.findParent())
    # return parents
    for child in childs:
        parents.append(child.findParent())
    return parents


def file_to_soup(path):
    """open a file and make a soup out of that"""
    g = open(path, "r")
    data = g.read()
    soup = BeautifulSoup(bs_preprocess(data))
    return soup


def grab_elements(soup, elem, attr1, attr2):
    """grabs the different elemens with the given attributes out of a soup"""
    return soup.find_all([elem], attrs={attr1: [attr2]})


if __name__ == "__main__":
    ####be aware: this is spaghetti code###
    mypath = "python-3.4.0-docs-html/library/"
    files = get_list_of_filepath(mypath)
    #f = open('test.html', 'w')  # needs to exist
    for file in files:
        soup = file_to_soup(file)

        methods = grab_elements(soup, "dl", "class", "method")
        functions = grab_elements(soup, "dl", "class", "function")
        describtions = grab_elements(soup, "dl", "class", "describe")
        classmethods = grab_elements(soup, "dl", "class", "classmethod")
        staticmethods = grab_elements(soup, "dl", "class", "staticmethod")
        sections = grab_elements(soup, "div", "class", "section")
        classes = grab_elements(soup, "dl", "class", "class")
        ### attributes, data and exceptions will not be filtered ##
        #attributes = grab_elements(soup, "dl", "class", "attribute")
        #datas = grab_elements(soup, "dl", "class", "data")

        all_parents = find_parents(
            methods + functions + describtions + classmethods + staticmethods + sections + classes)
        all_parents_copy = copy.copy(all_parents)

        ###define placeholder
        placeholder = '[something removed here]'

        for parent in methods + functions + describtions + classmethods + staticmethods + sections + classes:
            ### set placeholders to duplicated elements ###
            for elem in parent.find_all('dl', {
            'class': ['method', 'function', 'describe', 'classmethod', 'staticmethod', 'section', 'class']}):
                tag = Tag(name='p')
                tag.string = placeholder
                elem.replace_with(tag)
            ### same thing with sections##
            for elem in parent.find_all('div', {'class': 'section'}):
                tag = Tag(name='p')
                tag.string = placeholder
                elem.replace_with(tag)

            ### summarize placeholders ###
            summarize_placeholders(parent, placeholder)

        results = methods + functions + describtions + classmethods + staticmethods + sections + classes

        # #########STORE SOMETHING INTO THE DATABASE#############
        conn = psycopg2.connect("host=127.0.0.1 dbname=mydb user=sven password=Schwen91")
        cur = conn.cursor()
        cur.execute(
            'SELECT id FROM extractor_documentationunit WHERE id=(SELECT max(id) FROM extractor_documentationunit)')
        try:
            i = cur.fetchone()[0]+1
        except:
            i = 0    # if table is empty
        j = i
        ## store parents of each documenation_unit
        for elem in all_parents_copy:
            if isinstance(elem, Tag):
                parent = elem.prettify()
                cur.execute('INSERT INTO extractor_parentelement VALUES (%s, %s);',
                            (j, parent))
            j += 1

        ##store documenation units##
        for elem in results:
            fname = file
            if isinstance(elem, Tag):
                strng = elem.prettify()
                cur.execute('INSERT INTO extractor_documentationunit  VALUES (%s,  %s,  %s,  %s);',
                            (i, strng, fname, len(strng)))
            i += 1

            ### progress bar ###
            if i % 100 == 0:
                print("Just finished import for documentation unit "+str(i))

        conn.commit()
        cur.close()
        conn.close()
        #f.close()