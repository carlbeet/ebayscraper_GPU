from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=gpu&_sacat=0&LH_TitleDesc=0&_odkw=GPU&_osacat=0'
#sublime- ctrl shift P > set syntax > python
#for html- https://beautifier.io/

#grab the page
uSite = uReq(my_url) #download page
page_html = uSite.read() #store page
uSite.close()

page_soup = soup(page_html, "html.parser")
containers = page_soup.findAll("li", {"class": "s-item s-item--watch-at-corner"})
#gives 50 containers
#first container = containers[0]

filename = "gpus_EBAY.csv"
f = open(filename, "w", encoding = "utf-8")
headers = "name, used_status, brand, model, size, shipping, price, item_rating, rating_count\n"
f.write(headers)
#create file



for container in containers:
	#DATA: name, used, brand, size (GB), price, shipping, rating, ratingcount
	
	item_name = container.find("h3",{"class":"s-item__title"}).text
	item_subtitle = container.find("div", {"class":"s-item__subtitle"}).text
	#need to parse into 3:
	#item subtitle: 'Pre-Owned · NVIDIA · 24 GB'

	if item_subtitle.count('·') == 2:
		used, brand, size = item_subtitle.split('·')
		used.strip()
		brand.strip()
		model = ""
		size.strip()
	elif item_subtitle.count('·') == 3:
		used, brand, model, size = item_subtitle.split('·')
		used.strip()
		brand.strip()
		model.strip()
		size.strip()
	else:
		used = item_subtitle.strip()
		brand = ""
		model = ""
		size = ""
	#handles all subtitle variations



	item_shipping = container.find("span", {"class": "s-item__shipping s-item__logisticsCost"}).text
	item_price = container.find("span", {"class":"s-item__price"}).text
	   
	item_rating = container.find("span", {"class":"clipped"}).text
	if "stars" in item_rating:
		item_rating.strip()
		item_rating = item_rating[0:3]
	else:
		item_rating = "none"	



	try: 
		item_rating_count = container.find("span", {"class":"s-item__reviews-count"}).text.strip()
		item_rating_count, dropped_words = item_rating_count.split(maxsplit=1)
		#makes 2 string list

	except:
		item_rating_count = ""

	print("name: "+ item_name)
	print("used: "+ used)
	print("brand: "+ brand)
	print("model: " + model)
	print("size: "+ size)
	print("item_shipping: "+ item_shipping)
	print("item_price: "+ item_price)
	print("item_rating: "+ item_rating)
	print("item_rating_count: " + item_rating_count)
	#all data collected, now write to a file 
	

	f.write(item_name.replace(",", "-") + "," +  used + "," + brand + "," + model.replace(",", "-")+ "," + size + "," + item_shipping + "," + item_price.replace(",", "") + "," + item_rating + "," + item_rating_count + "\n")
	#name, used_status, brand, model, size, shipping, price, item_rating, rating_count\n"
f.close()


#cd SublimeProjectsNotes
#py ebayScraper.py 












