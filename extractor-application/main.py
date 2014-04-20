from bs4 import BeautifulSoup
soup = BeautifulSoup(open("/home/sven/Bachelorarbeit/python-doc-extractor-for-cado/extractor-application/index.html"))
f = open('test.html','w')
f.truncate

#classes= soup.find_all('dl', attrs={'class': ['class', 'method','function','describe', 'attribute', 'data', 'clasmethod', 'staticmethod']})
matches = []
for elem in soup.find_all('dl', attrs={'class': ['class', 'method','function','describe', 'attribute', 'data', 'classmethod', 'staticmethod', 'section']}):
    if any(elem in m.descendants for m in matches):
        # child of already found element
        continue
#    matches.append(BeautifulSoup("<p>****************</p>"))
    matches.append(elem)



#for div in soup.find_all('div', attrs={'class':'section'}):
#    if any(dl or div in m.descedants for m in matches):
#    #child of already found element
#        continue
#    matches.append(dl)

print(soup.head,file=f)
print(matches,file=f)
print(soup.footer,file=f)
f.close()
