import urllib2
import re

#Browser related tags
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
headers = { 'User-Agent' : user_agent }

#Replace the address string with appropriate values
address='C:\\Users\\For Users\\Desktop\\lodha\\siteLinks'
siteLinks = open(address, 'r')

#Used if there is no Google Tag Manager code present at all.
flag=0

#Replace 295 with number of lines on the file
for i in range(0,442):
	currentPage=siteLinks.readline()
	print(""+str(i+1)+", "+str(currentPage.splitlines()[0])+", "),

	#Request the webpage source
	req = urllib2.Request(currentPage, None, headers)
	response = urllib2.urlopen(req)
	page = response.read()
	#Resetting Flag
	flag=0

	#Regular Expression to detect GTM Object IDs. Feel free to change it.
	RE= re.findall(r'dataLayer = \[\]', page)
	
	for j in RE:
		#dataLayer = [];
		if j.lower()!='dataLayer = []'.lower():
			print(""+j+", FAILED")
			flag=1
		else:
			print(""+j+", PASSED")
			flag=1
	if flag==0:
		print("NOCODE, ABSENT")


#NOTE: If you want to export the output in Excel/Speadsheet, format the print calls and make them appear on the same line. Values should be seperated with a comman (,) Save the output as a CSV file, import that into Excel/Spreadsheet with delimiter as comma (,)