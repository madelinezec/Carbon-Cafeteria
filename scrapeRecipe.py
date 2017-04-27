
 #!/usr/bin/python
import requests
import mechanize
import re
import cookielib

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# The site we will navigate into, handling it's session
br.open('http://www.cleanmetrics.net/foodcarbonscope')

br.select_form(name="aspnetForm")
br.form['ctl00$ContentPlaceHolder1$userName'] = "fcstemp"
br.form['ctl00$ContentPlaceHolder1$passWord'] = "fcs2880#"

# Login
br.submit()

# Configure this to be your first request URL
r = requests.get("https://www.fns.usda.gov/usda-standardized-recipe")
soup = BeautifulSoup(r.content, "html.parser")

div = soup.find('div', class_='grid-9 region region-content')

for category in div.findAll('a', href=True):
	if "/tn/" in category['href']:
		print('Hello')
		base_url = "https://www.fns.usda.gov"
		request_href = requests.get(base_url + category['href'])
		#print(request_href)	    soupTwo = BeautifulSoup(request_href.content, "html.parser")
		links = soupTwo.find('article', class_='node node-page node-published node-not-prompted node-not-sticky')
		for link in soupTwo.findAll('a', href=True):
			if link.find(text=re.compile("50-100 servings")):
				x = requests.get(link['href'])
				recipe = BeautifulSoup(x.content, "html.parser")
				for ingredient in recipe.findAll('div', class_='tableRow'):
					name = ingredient.find('div', class_='tcell ingredient-name').text
					amount = ingredient.find('div', class_='tcell ingredient-lweight').text
					print(name)
					break;




