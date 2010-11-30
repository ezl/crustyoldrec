import urllib
import urllib2
from lxml import etree
from newedgeutils import *
# build opener with HTTPCookieProcessor
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
urllib2.install_opener(opener)

userid = "ERICLIU"
password = "Ctc12345"

credentials = urllib.urlencode(dict(userid=userid, password=password))

url = "https://pulse.newedgegroup.com/wps/myportal"

user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7"
request_headers = {"User-Agent": user_agent, "Referer": "http://python.org"}
request = urllib2.Request(url, headers=request_headers)


print "Logging in to DataPort..."
f = opener.open(request, credentials)
page = f.read()
f.close()

#WTF no idea why i need to hit this page
url2 = "https://pulsedataport.newedgegroup.com/wps/myportal/reports"
print "Accessing report landing page..."
request2 = urllib2.Request(url2, headers=request_headers)
request2 = urllib2.Request(url2)
f = opener.open(request2)
page2 = f.read()
f.close()

def retrieve_transactions():
    print "Retrieving real time transactions..."
    url = "https://pulsedataport.newedgegroup.com/wps/PA_dataport-report-na/crystalExport.jsp?exportFormat=CSV&repid=31934186&archid=31934561"
    request = urllib2.Request(url, headers=request_headers)
    f = opener.open(request)
    page = f.read()
    f.close()
    return page

def retrieve_positions():
    "Retrieving open position..."
    url = "https://pulsedataport.newedgegroup.com/wps/PA_dataport-report-na/crystalExport.jsp?exportFormat=CSV&repid=31934370&archid=33260099"
    request = urllib2.Request(url, headers=request_headers)
    f = opener.open(request)
    page = f.read()
    f.close()
    return page

p = retrieve_positions()
t = retrieve_transactions()

positions = parse_positions(p)
transactions = parse_transactions(t)
