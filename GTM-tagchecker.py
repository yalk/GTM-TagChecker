import urllib2, base64
import re
import csv
import time



def fetchpage(URL=None, username=None, password=None):

	if(URL!=None):

		user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
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

#START OF SOURCE CODE CHECK FUNCTIONS

def checkCustomCode(page_source, regex, codename):
	
	GAStatusList=[None]*3
	RE_GA= re.findall(regex, page_source)
	
	for k in RE_GA:
		RE_GA_trimmer= re.findall(regex,str(k))
		
		if(RE_GA_trimmer!=None):
			if(""+codename+"_YES" not in GAStatusList):
				GAStatusList[0]=""+codename+"_YES"
			
			if RE_GA_trimmer not in GAStatusList:
				if codename == 'SitCat':
					RE_GA_trimmer[0] = filter(None, list(RE_GA_trimmer[0]))[0]
				#print "fun-checkCode-re_ga_trimmer="+str((RE_GA_trimmer[0])),#str(type(RE_GA_trimmer[0](0))),

				if GAStatusList[2]==None:
					#print "fun-checkCode-re_ga_trimmer="+str(RE_GA_trimmer[0]),
					GAStatusList[2]=str(RE_GA_trimmer[0])
				
				else:
					GAStatusList[2]=GAStatusList[2]+"|"+str(RE_GA_trimmer[0])
		
	if GAStatusList[0]==None:
		GAStatusList[0]=""+codename+"_ABSENT"
		GAStatusList[2]=""+codename+"_NO"
	#print GAStatusList
	return GAStatusList

#END OF SOURCE CODE CHECK FUNCTIONS

def init_output(outputCSVFile=None):
	
	if(outputCSVFile!=None):
		headerForCSV="No,URL,GTM_Found,NoOfGTM,GTM_Code,GA_Found,NoOfGA,GA_Code,Adobe_Found,NoOfAdobe,Adobe_Code,EnsightenBootstrap_Found,NoOfEnsightenBootstrap,EnsightenBootstrap_Code,Facebook_Found,NoOfFacebook,Facebook_Code,DCM_Found,NoOfDCM,DCM_Code,AdWords_Found,NoOfAdwords,AdWords_Code\n"
		#URL_Code_status= URLList +GTMStatusList +GAStatusList +AdobeStatusList +AdobePagePathStatusList +TealiumStatusList +EnsightenBootstrapStatusList +sCodeStatusList +TestnTargetStatusList +FacebookStatusList +DCMPixelStatusList +AdWordsPixelStatusList
		outputCSVFile.write(headerForCSV)



def writer_and_printer(outputCSVFile, URL_GTM_and_GA_status):
	
	writerobject=csv.writer(outputCSVFile, quoting=csv.QUOTE_ALL)
	writerobject.writerow(URL_GTM_and_GA_status)

	print URL_GTM_and_GA_status,



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
	startTime= time.time()
	for i in range(0,numberOfLinks):
		URLList= [None]*2
		try:

			interTime= time.time()

			URL= siteLinks.readline().splitlines()[0]
			URLLine= ""+str(i+1)+","+str(URL)

			URLList[0]= i+1
			URLList[1]= URL

			page_source= fetchpage(URL)
			URL_Code_status= URLList
			
			#Custom Codes
			#regex= re.compile('GTM-.*?(?=\W)')
			regex = r"\'GTM-.*?\'"
			codename= "GTM"
			CustomCodeStatusList= checkCustomCode(page_source, regex, codename)
			CustomCodes= str(CustomCodeStatusList[2])
			countOfCustomCodes= int(CustomCodes.count('GTM-'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			CustomCodeStatusList[1]= countOfCustomCodes

			#Uncomment the append statuslist variable from the below line
			URL_Code_status= URL_Code_status +CustomCodeStatusList
			
			#Custom Codes
			#regex= re.compile('GTM-.*?(?=\W)')
			regex = r"(ga ?\('create' ?, ?'UA-.*?' ?, ?'auto' ?\))|(gaq\.push\(\['_setAccount' ?, ?'UA-.*?'\]\))"
			codename= "GA"
			CustomCodeStatusList= checkCustomCode(page_source, regex, codename)

			CustomCodeStatusList[2]= str(",".join(re.findall("UA-.*?-.",str(CustomCodeStatusList[2]))))
			CustomCodes= str(CustomCodeStatusList[2])
			countOfCustomCodes= int(CustomCodes.count('UA-'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			CustomCodeStatusList[1]= countOfCustomCodes

			#Uncomment the append statuslist variable from the below line
			URL_Code_status= URL_Code_status +CustomCodeStatusList
			
			#Custom Codes
			#regex= re.compile('GTM-.*?(?=\W)')
			#AU - Site_Catalyst.js
			#HK - Site_Catalyst.js
			#CN - SC_code1.js
			#CN - SC_code1.js
			#SG - SC_code.js
			#ID - SC_code.js
			#TW - citi_s_code.js
			#TH - citi_s_code.js
			#IN - s_code.js
			
			regex = r"((Site_Catalyst|(SC|citi_s|s)_code(1?))\.js)"

			#regex = r"(Site_Catalyst\.js)|(SC_code1\.js)|(citi_s_code\.js)|(SC_code\.js)|(s_code\.js)|(page_code.js)"
			codename= "SitCat"
			CustomCodeStatusList= checkCustomCode(page_source, regex, codename)
			
			CustomCodes= str(CustomCodeStatusList[2])
			countOfCustomCodes= int(CustomCodes.count('.js'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			CustomCodeStatusList[1]= countOfCustomCodes
			#print CustomCodeStatusList
			#Uncomment the append statuslist variable from the below line
			URL_Code_status= URL_Code_status +CustomCodeStatusList

			#Custom Codes
			#regex= re.compile('GTM-.*?(?=\W)')
			regex = r"prod/Bootstrap.js"
			codename= "Ensighten"
			CustomCodeStatusList= checkCustomCode(page_source, regex, codename)
			CustomCodes= str(CustomCodeStatusList[2])
			#print CustomCodeStatusList
			countOfCustomCodes= int(CustomCodes.count('Bootstrap.js'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			CustomCodeStatusList[1]= countOfCustomCodes
			#Uncomment the append statuslist variable from the below line
			URL_Code_status= URL_Code_status +CustomCodeStatusList

			#Custom Codes
			#regex= re.compile('GTM-.*?(?=\W)')
			regex = r"'fbq'"
			codename= "FBPixel"
			CustomCodeStatusList= checkCustomCode(page_source, regex, codename)
			CustomCodes= str(CustomCodeStatusList[2])
			countOfCustomCodes= int(CustomCodes.count('fbq'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			CustomCodeStatusList[1]= countOfCustomCodes
			#Uncomment the append statuslist variable from the below line
			URL_Code_status= URL_Code_status +CustomCodeStatusList

			regex = r"doubleclick"
			codename= "DC"
			CustomCodeStatusList= checkCustomCode(page_source, regex, codename)
			CustomCodes= str(CustomCodeStatusList[2])
			countOfCustomCodes= int(CustomCodes.count('doubleclick'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			CustomCodeStatusList[1]= countOfCustomCodes
			#Uncomment the append statuslist variable from the below line
			URL_Code_status= URL_Code_status +CustomCodeStatusList

			regex = r"google_conversion_id"
			codename= "AdWords"
			CustomCodeStatusList= checkCustomCode(page_source, regex, codename)
			CustomCodes= str(CustomCodeStatusList[2])
			countOfCustomCodes= int(CustomCodes.count('google_conversion_id'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			CustomCodeStatusList[1]= countOfCustomCodes
			#Uncomment the append statuslist variable from the below line
			URL_Code_status= URL_Code_status +CustomCodeStatusList

			#URL_Code_status= URLList +GTMStatusList +GAStatusList +AdobeStatusList +AdobePagePathStatusList +TealiumStatusList +EnsightenBootstrapStatusList +sCodeStatusList +TestnTargetStatusList +FacebookStatusList +DCMPixelStatusList +AdWordsPixelStatusList +AdWordsPixelStatusList #+CustomCodeStatusList
			
			writer_and_printer(outputCSVFile, URL_Code_status)
			endTime= time.time()
			print "I: "+str(endTime-interTime)+"\tT: "+str(endTime-startTime)
			#print("\n\nlength="+page_source);
		except Exception as e:
			error= str(e)+"\n"
			URLList.append(error)
			#URL_Code_status = [e,e,e]
			#print URL_Code_status
			writer_and_printer(outputCSVFile, URLList)
			#print(e)
			continue
	
	siteLinks.close()
	outputCSVFile.close()

if __name__ == "__main__": main()
