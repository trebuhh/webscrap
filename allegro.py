from bs4 import BeautifulSoup
import urllib.request as urllib2
import dbm

def read_page(page):
    #using request module load page to memory
    opened_page = urllib2.urlopen(page)
    read = opened_page.read()
    opened_page.close()
    soup = BeautifulSoup(read, "html.parser")
    return soup

def last_key(db):
    #return max value which represents last key
    temp =[]
    for key in db:
        temp.append(int(key))
    return max(temp)

def db_comparision(db_1, db_tp):
    #compare to db's, if there is new link, print it and at to local database
    list_1 = [db_1[key] for key in db_1]
    list_2 = [db_tp[key] for key in db_tp]

    new = [site for site in list_2 if site not in list_1]
    if not new:
        print("Nie ma nowych linków")
    else:
        print(new)
        ls = last_key(db_1)
        for x, item in enumerate(new, 1):
            db_1[str(ls+x)] = item




#get source of page
site = "https://allegro.pl/kategoria/czesci-samochodowe-czesci-karoserii-4094?string=e46%20silbergrau&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-aut-1-2-1003"
html = read_page(site)


#select div
allegro_div = html.select("div")

#how many subsites at site
h_num = []
for classes in allegro_div:
    my_class = classes.get('class')
    if str(my_class) == "['pagination-bottom']":
       pagination = classes.select('a')
       for links in pagination:
         h_num.append(links.get('data-page'))

#delete NoneType at pagination-bottom, get maximum value
for num in h_num:
    if isinstance(num, str):
        num = int(num)
    else:
        h_num.remove(num)
max_num = max(h_num)

db = dbm.open('local_links', 'c')
temp = dbm.open('temp_links', 'n')

x = 0
#get links with DEV attribiutes from all subsites
for page in range(int(max_num)):
    #load subsite
    print(site+"&p="+str(page+1))
    html = read_page(site+"&p="+str(page+1))
    allegro_div = html.select("div")
    for ids in allegro_div:
        my_id = ids.get('id')
        if str(my_id) == 'opbox-listing':
           opbox_a = ids.select('a')
           for link in opbox_a:
               if 'events' not in link.get('href'):
                    if 'blotnik' in link.get('href'):
                        x += 1
                        temp[str(x)] = link.get('href')

print('Pobralem '+str(x)+' linkow odnoszacych sie do blotnikow do e46 w kolorze silbergrau')

db_comparision(db, temp)

db.close()
temp.close()

