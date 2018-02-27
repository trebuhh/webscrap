from bs4 import BeautifulSoup
import urllib.request as urllib2


allegroFile = urllib2.urlopen("https://allegro.pl/kategoria/czesci-samochodowe-czesci-karoserii-4094?string=e46%20silbergrau&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-aut-1-2-1003$")
allegroHtml = allegroFile.read()
allegroFile.close()

#list all wanted links
soup = BeautifulSoup(allegroHtml, "html.parser")
allegroDIV = soup.select("div")

#oblicz ile jest stron
h_num = []
for classes in allegroDIV:
    my_class = classes.get('class')
    if "['pagination-bottom']" == str(my_class):
       pagination = classes.select('a')
       for links in pagination:
         h_num.append(links.get('data-page'))

for num in h_num:
        if isinstance(num, str):
            num = int(num)
        else:
            h_num.remove(num)

max_num = max(h_num)
x=1
site="https://allegro.pl/kategoria/czesci-samochodowe-czesci-karoserii-4094?string=e46%20silbergrau&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-aut-1-2-1003&p="
for page in range(int(max_num)):
    print(site+str(page+1))
    allegroFile = urllib2.urlopen(site+str(page+1))
    allegroHtml = allegroFile.read()
    allegroFile.close()

    #list all wanted links
    soup = BeautifulSoup(allegroHtml, "html.parser")
    allegroDIV = soup.select("div")

    for ids in allegroDIV:
        my_id = ids.get('id')
        if str(my_id) == 'opbox-listing':
           opboxA = ids.select('a')
           for link in opboxA:
               if 'events' not in link.get('href'):
                    if 'blotnik' in link.get('href'):
                        print(str(x)+link.get('href'))
                        x+=1