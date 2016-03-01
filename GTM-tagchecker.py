import urllib2, base64
import re
import csv

def fetchpage(URL=None, username=None, password=None):

	if(URL!=None):

		user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
		headers = { 'User-Agent' : user_agent }

		req = urllib2.Request(URL, None, headers)

		if((username!=None) and (password!=None)):						#for domains with passwords
			base64string = base64.encodestring('%s:%s' % ('admin', 'caresupport')).replace('\n', '')
			req.add_header("Authorization", "Basic %s" % base64string)   
		response = urllib2.urlopen(req)									#fetch page
		page_source = response.read()
		
		#clean up page
		page_source = re.sub(re.compile("/\*.*?\*/", re.DOTALL) , "", page_source) 	#Remove all occurance streamed comments (/*Javascript Multiline COMMENT */) from string
		page_source = re.sub(re.compile("<!--.*?-->", re.DOTALL) , "", page_source) 	#Remove all occurance streamed comments (<!--HTML Multiline COMMENT-->) from string
		
		return page_source



def checkGTM(page_source):
	
	GTMStatusList=[None]*3
	RE_GTM= re.findall(r'GTM-.*?(?=\W)', page_source) #String starts with 'GTM-.*<followed by anything before a non alphanumeric character>?(?=\W)
	
	for j in RE_GTM:
		if (j!=None):
			if("GTM_YES" not in GTMStatusList):
				GTMStatusList[0]="GTM_YES"
			
			if j not in GTMStatusList:
				if GTMStatusList[2]==None:
					GTMStatusList[2]=str(j)
				
				else:
					GTMStatusList[2]=GTMStatusList[2]+"|"+str(j)
		
	if GTMStatusList[0]==None:
		GTMStatusList[0]="GTM_ABSENT"
		GTMStatusList[2]="GTM_NO"
	#print GTMStatusList,
	return GTMStatusList
	


def checkGA(page_source):
	
	GAStatusList=[None]*3
	RE_GA= re.findall("(ga ?\('create' ?, ?'UA-.*?' ?, ?'auto' ?\))|(gaq\.push\(\['_setAccount' ?, ?'UA-.*?'\]\))",page_source)
	
	for k in RE_GA:
		RE_GA_trimmer= re.findall("UA-.*?-.",str(k))
		
		if(RE_GA_trimmer!=None):
			if("GA_YES" not in GAStatusList):
				GAStatusList[0]="GA_YES"
			
			if RE_GA_trimmer not in GAStatusList:
				if GAStatusList[2]==None:
					GAStatusList[2]=str(RE_GA_trimmer[0])
				
				else:
					GAStatusList[2]=GAStatusList[2]+"|"+str(RE_GA_trimmer[0])
		
	if GAStatusList[0]==None:
		GAStatusList[0]="GA_ABSENT"
		GAStatusList[2]="GA_NO"
	#print GAStatusList
	return GAStatusList


def init_output(outputCSVFile=None):
	
	if(outputCSVFile!=None):
		headerForCSV="No,URL,GTM_Found,NoOfGTM,GTM_Code,GA_Found,NoOfGA,GA_Code\n"
		outputCSVFile.write(headerForCSV)	



def writer_and_printer(outputCSVFile, URL_GTM_and_GA_status):
	
	writerobject=csv.writer(outputCSVFile, quoting=csv.QUOTE_ALL)
	writerobject.writerow(URL_GTM_and_GA_status)

	print URL_GTM_and_GA_status



def main():

	addressOfInputFile='siteLinks'

	numberOfLinks= 0;
	
	with open(addressOfInputFile, 'r') as temp_f:
	    numberOfLinks= sum(1 for _ in temp_f)
	temp_f.close()

	addressOfOutputFile= 'outputCSV.csv'
	outputCSVFile= open(addressOfOutputFile, 'wb')
	
	init_output(outputCSVFile)

	siteLinks= open(addressOfInputFile, 'r')

	for i in range(0,numberOfLinks):

		try:
			URLList= [None]*2
			URL= siteLinks.readline().splitlines()[0]
			URLLine= ""+str(i+1)+","+str(URL)

			URLList[0]= i+1
			URLList[1]= URL

			page_source= fetchpage(URL)
			
			GTMStatusList= checkGTM(page_source)
			GTMs= str(GTMStatusList[2])
			countOfGTMCodes= int(GTMs.count('|')) +1
			GTMStatusList[1]= countOfGTMCodes
			

			GAStatusList= checkGA(page_source)
			GAs= str(GAStatusList[2])
			countofGACodes= int(GAs.count('|')) +1
			GAStatusList[1]= countofGACodes

			URL_GTM_and_GA_status= URLList +GTMStatusList +GAStatusList
			
			writer_and_printer(outputCSVFile, URL_GTM_and_GA_status)

		except:
			continue
	
	siteLinks.close()
	outputCSVFile.close()

if __name__ == "__main__": main()