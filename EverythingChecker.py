import urllib2
import re

#Browser related tags
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
headers = { 'User-Agent' : user_agent }

#Replace the address string with appropriate values
address='C:\\Users\\For Users\\Desktop\\lodha\\newTool\\siteLinks'
siteLinks = open(address, 'r')

#Used if there is no Google Tag Manager code present at all.

flag=0
address2='C:\\Users\\For Users\\Desktop\\lodha\\newTool\\outputCSV.csv'
outputfile = open(address2, 'w')

headerForCSV="No,Link,Retrieved,Status\n"
outputfile.write(headerForCSV)

#Replace 295 with number of lines on the file
for i in range(0,224):
	currentPage=siteLinks.readline()
	outputLine=""+str(i+1)+","+str(currentPage.splitlines()[0])+", "

	print(outputLine),
	outputfile.write(outputLine)

	#Request the webpage source
	req = urllib2.Request(currentPage, None, headers)
	response = urllib2.urlopen(req)
	page = response.read()
	#Resetting Flag
	
	page = re.sub(re.compile("/\*.*?\*/", re.DOTALL) , "", page) 	#Remove all occurance streamed comments (/*Javascript Multiline COMMENT */) from string
	page = re.sub(re.compile("<!--.*?-->", re.DOTALL) , "", page) 	#Remove all occurance streamed comments (<!--HTML Multiline COMMENT-->) from string
	#page = re.sub(re.compile("//.*?\n") , "", page) 				#Remove all occurance singleline comments (//COMMENT\n ) from string
	
	flag=0

	#Regular Expression to detect GTM Object IDs. Feel free to change it.
	#RE= re.findall(r'dataLayer = \[\]', page)
	#RE= re.findall(r'dataLayer ?= ?\[\]', page)
	#RE= re.findall(r'gaq\.push', page)
	RE= re.findall(r'(?m)^(?!//)Weybeo_widget', page)
	#RE= re.findall(r'GTM-.*"', page)
	#RE= re.findall(r'gaq\.push', page)

	#RE= re.findall(r'GTM.*"', page)

	for j in RE:
		#dataLayer = [];
		#if j.lower()=='dataLayer = []'.lower():
		#if j.lower()=='gaq.push'.lower():
		#if j.lower()=='datalayer = []'.lower():
		if j.lower()==r'Weybeo_widget'.lower():
		#if j.lower()!=r'GTM-Q8FF"'.lower():
			outputfile.write(""+j+",PASSED\n")
			print(" "+j+", PASSED"),
			flag=1
		else:
			outputfile.write(""+j+",FAILED\n")
			print(" "+j+", FAILED"),
			flag=1
		print ""
	if flag==0:
		outputfile.write("NOCODE,ABSENT\n")
		print("NOCODE, ABSENT")

siteLinks.close()
outputfile.close()