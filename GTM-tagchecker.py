import urllib2, base64
import re

#Browser related tags
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
headers = { 'User-Agent' : user_agent }

#Replace the address string with appropriate values
address='siteLinks'
siteLinks = open(address, 'r')

#Used if there is no Google Tag Manager code present at all.

flag=0
address2='outputCSV.csv'
outputfile = open(address2, 'w')

headerForCSV="No,Link,Retrieved,Status,Retrieved,Status,Retrieved,Status\n"
outputfile.write(headerForCSV)

#Replace 295 with number of lines on the file
for i in range(0,6):
#for i in range(0,10):
	try:
		currentPage=siteLinks.readline()
		outputLine=""+str(i+1)+","+str(currentPage.splitlines()[0])

		print(outputLine),
		outputfile.write(outputLine)

		#Request the webpage source
		req = urllib2.Request(currentPage, None, headers)
		
		#Uncomment if site needs password
		base64string = base64.encodestring('%s:%s' % ('admin', 'caresupport')).replace('\n', '')
		req.add_header("Authorization", "Basic %s" % base64string)   
		
		response = urllib2.urlopen(req)
		page = response.read()
		#Resetting Flag
		
		page = re.sub(re.compile("/\*.*?\*/", re.DOTALL) , "", page) 	#Remove all occurance streamed comments (/*Javascript Multiline COMMENT */) from string
		page = re.sub(re.compile("<!--.*?-->", re.DOTALL) , "", page) 	#Remove all occurance streamed comments (<!--HTML Multiline COMMENT-->) from string
		#page = re.sub(re.compile("//.*?\n") , "", page) 				#Remove all occurance singleline comments (//COMMENT\n ) from string
		
		flag=0
		flag1=0
		#Regular Expression to detect GTM Object IDs. Feel free to change it.
		#RE= re.findall(r'dataLayer = \[\]', page)
		#RE= re.findall(r'dataLayer ?= ?\[\]', page)
		#RE= re.findall(r'gaq\.push', page)
		#RE= re.findall(r'(?m)^(?!//)Weybeo_widget', page)
		RE= re.findall(r'GTM-.*?(?=\W)', page) #String starts with 'GTM-.*<followed by anything before a non alphanumeric character>?(?=\W)
		#RE= re.findall(r'GTM-.*"', page)
		#RE= re.findall(r'gaq\.push', page)
		RE2= re.findall("ga\('send'*", page)
		#RE= re.findall(r'GTM.*"', page)

		for j in RE:
			#dataLayer = [];
			#if j.lower()=='dataLayer = []'.lower():
			######if j.lower()=="ga('send'".lower():
			#if j.lower()=="gaq.push":
			#if j.lower()=='datalayer = []'.lower():
			#if j.lower()==r'Weybeo_widget'.lower():

			#GTM

			if j.lower()==r'GTM-PL9Z33'.lower():
				outputfile.write(","+j+",GTM_PASSED")
				print(","+j+", GTM_PASSED"),
				flag=1
			else:
				outputfile.write(","+j+",GTM_FAILED")
				print(","+j+", GTM_FAILED"),
				flag=1
		if flag==0:
			outputfile.write(",GTM_NOCODE,GTM_ABSENT")
			print("GTM_NOCODE, GTM_ABSENT"),

		#GA

		for k in RE2:
			if k.lower()=="ga('send'".lower():
				outputfile.write(","+k+",GA_PASSED")
				print(","+k+", GA_PASSED"),
				flag1=1
			else:
				outputfile.write(","+k+",GA_FAILED")
				print(","+k+", GA_FAILED"),
				flag1=1
		if flag1==0:
			outputfile.write(",GA_NOCODE,GA_ABSENT")
			print("GA_NOCODE, GA_ABSENT"),

		print ""
		outputfile.write("\n")
	except:
		outputfile.write(",ERROR")
		print(", ERROR"),

		print ""
		outputfile.write("\n")
siteLinks.close()
outputfile.close()