from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

page = urlopen("https://aysanparvaz.com/%DA%A9%D8%AF-%D9%81%D8%B1%D9%88%D8%AF%DA%AF%D8%A7%D9%87")
html = page.read().decode("utf-8")
soup = BeautifulSoup(html,"html.parser")
check = soup.findAll("strong")
pattern = "<strong.*?>.*?</strong.*?>"
for i in range(len(check)):
    match_results = re.search(pattern, str(check[i]), re.IGNORECASE)
    city_name = match_results.group()
    city_name = re.sub("<.*?>", "", city_name)
    check[i] = city_name


check2 = soup.findAll("td", width = "143")
pattern = "<td.*?>.*?</td.*?>"
for i in range(len(check2)):
    match_results = re.search(pattern, str(check2[i]), re.IGNORECASE)
    city_name = match_results.group()
    city_name = re.sub("<.*?>", "", city_name)
    check2[i] = city_name

with open("text.text","w") as f:
    f.write("{")
    for i in range (len(check)):
        f.write('"' + check2[i] + '"' + ":" + '"' + check[i] + '"' + ",")
    f.write("}")