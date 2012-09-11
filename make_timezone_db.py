import urllib
import BeautifulSoup
from pysqlite2 import dbapi2 as sqlite

def fetch(url):
	return urllib.urlopen(url).read()

def fetchall():
	con = sqlite.connect('timezones.sqlite')
	try:
		for i in range(1, 2271):
			if i == 1440: # this is the UTC city, which makes no sense
				continue
			url = 'http://www.timeanddate.com/worldclock/city.html?n=' + str(i)
			print 'fetching: ' + url
			html = fetch(url)
			soup = BeautifulSoup.BeautifulSoup(html)
			timezonetable = soup.find(id='tz1')
			utcoffsetstr =  timezonetable.td.next.next.next
			utcoffset = "+0"
			plusoffset = utcoffsetstr.find('+')
			if plusoffset == -1:
				plusoffset = utcoffsetstr.find('-')
			if plusoffset > -1:
				utcoffsetstr = utcoffsetstr[plusoffset:]
				utcoffset = utcoffsetstr[:utcoffsetstr.index(' ')]
			daylightsavings = True
			daylightsavingsstr = timezonetable.td.next.next.next.next.next.next
			if daylightsavingsstr.startswith('No'):
				daylightsavings = False
			descriptiontags = soup.findAll('meta')[-1]['content']
			city = descriptiontags.split(',')[-1]
			country = descriptiontags.split(',')[-2]
			print 'CITY: ' + city
			print 'COUNTRY: ' + country
			print 'UTC OFFSET: ' + str(utcoffset)
			print 'DAYLIGHT SAVINGS: ' + str(daylightsavings)
			values = {'cityname':city, 'country':country, 'utcoffset':utcoffset, 'daylightsavings':daylightsavings}
			cur = con.cursor()
			cur.execute('insert into city(cityname, country, utcoffset, daylightsavings) values (:cityname, :country, :utcoffset, :daylightsavings)', values)
	except:
		con.commit()
		raise
	con.commit()
		
