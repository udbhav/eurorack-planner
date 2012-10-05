import requests
from bs4 import BeautifulSoup
import json

node_range = range(1,810)
modules = []

for node in node_range:
    url = "http://eurorackdb.com/node/%i" % node
    print "checking %s" % url
    r = requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text)

        try:
            title = soup.title.string
        except AttributeError:
            title = ''

        if title.find("| Module:") != -1:
            print "module found..."
            module_table = soup.find_all('table')[1].find('table')
            module = {
                'manufacturer': module_table.find_all("tr")[0].find_all("td")[1].string,
                'name': module_table.find_all("tr")[1].find_all("td")[1].string,
                'hp': module_table.find_all("tr")[4].find_all("td")[1].string,
                'depth': module_table.find_all("tr")[5].find_all("td")[1].string,
                'msrp': module_table.find_all("tr")[6].find_all("td")[1].string,
                'current_12v': module_table.find_all("tr")[7].find_all("td")[1].string,
                'negative_current_12v': module_table.find_all("tr")[8].find_all("td")[1].string,
                'current_5v': module_table.find_all("tr")[9].find_all("td")[1].string,
                'url': module_table.find_all("tr")[10].find_all("td")[1].string,
                }

            image = soup.find("img")
            if image:
                module['image'] = image['src']

            print module
            modules.append(module)


fwrite  = open('modules.json', 'w')
fwrite.write(json.dumps(modules))
fwrite.close()
