from bs4 import BeautifulSoup

soup = BeautifulSoup(open("/home/sven/Bachelorarbeit/python-doc-extractor-for-cado/extractor-application/index.html"))

f = open('test.html','w')
f.truncate

print("<h1>************FUNCTIONS***********</h1>",file=f)
print(soup.find_all('dl', attrs={'class':'function'}),file=f)
print("<h1>***********DESCRIBE*************</h1>",file=f)
print(soup.find_all('dl', attrs={'class':'describe'}),file=f)
print("<h1>************ATTRIBUTE***********</h1>",file=f)
print(soup.find_all('dl', attrs={'class':'attribute'}),file=f)
print("<h1>************METHOD**************</h1>",file=f)
print(soup.find_all('dl', attrs={'class':'method'}),file=f)
print("<h1>************DATA****************</h1>",file=f)
print(soup.find_all('dl', attrs={'class':'data'}),file=f)
print("<h1>************CLASSMETHOD*********</h1>",file=f)
print(soup.find_all('dl', attrs={'class':'classmethod'}),file=f)
print("<h1>************CLASS***************</h1>",file=f)


classes= soup.find_all('dl', attrs={'class':'class'})
print(classes,file=f)


print("<h1>************STATICMETHOD********</h1>",file=f)
print(soup.find_all('dl', attrs={'class':'staticmethod'}),file=f)



f.close()
