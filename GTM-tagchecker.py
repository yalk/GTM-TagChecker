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



def checkAdobe(page_source):
	
	GAStatusList=[None]*3
	RE_GA= re.findall("//assets\.adobedtm\.com/.*?\.js",page_source)
	
	for k in RE_GA:
		RE_GA_trimmer= re.findall("//assets\.adobedtm\.com/.*?\.js",str(k))
		if(RE_GA_trimmer!=None):
			if("ADOBE_YES" not in GAStatusList):
				GAStatusList[0]="ADOBE_YES"
			
			if RE_GA_trimmer not in GAStatusList:
				if GAStatusList[2]==None:
					GAStatusList[2]=str(RE_GA_trimmer[0])
				
				else:
					GAStatusList[2]=GAStatusList[2]+"|"+str(RE_GA_trimmer[0])
		
	if GAStatusList[0]==None:
		GAStatusList[0]="ADOBE_ABSENT"
		GAStatusList[2]="ADOBE_NO"
	#print GAStatusList
	return GAStatusList

def checkTealium(page_source):
	
	TealiumStatusList=[None]*3
	#//tags.tiqcdn.com/
	RE_TEALIUM= re.findall("\/\/tags\.tiqcdn.com\/.*?\.js", page_source)
	#//tags.tiqcdn.com/utag/telenor/telenor.no/prod/utag.sync.js
	for k in RE_TEALIUM:
		RE_Tealium_trimmer= re.findall("\/\/tags\.tiqcdn.com\/.*?\.js",str(k))
		if(RE_Tealium_trimmer!=None):
			if("TEALIUM_YES" not in TealiumStatusList):
				TealiumStatusList[0]="TEALIUM_YES"
			
			if RE_Tealium_trimmer not in TealiumStatusList:
				if TealiumStatusList[2]==None:
					TealiumStatusList[2]=str(RE_Tealium_trimmer[0])
				
				else:
					TealiumStatusList[2]=TealiumStatusList[2]+"|"+str(RE_Tealium_trimmer[0])
		
	if TealiumStatusList[0]==None:
		TealiumStatusList[0]="TEALIUM_ABSENT"
		TealiumStatusList[2]="TEALIUM_NO"
	#print GAStatusList
	return TealiumStatusList

def checkAdobePagePath(page_source):
	
	AdobePagePathStatusList=[None]*3
	#//tags.tiqcdn.com/
	RE_ADOBEPAGEPATH= re.findall('\<input type\=\"hidden\" id\=\"pagepath\" value\=\".*?\"', page_source)
	#//tags.tiqcdn.com/utag/telenor/telenor.no/prod/utag.sync.js
	for k in RE_ADOBEPAGEPATH:
		RE_AdobePagePath_trimmer= re.findall('\<input type\=\"hidden\" id\=\"pagepath\" value\=\".*?\"',str(k))
		if(RE_AdobePagePath_trimmer!=None):
			if("AdobePagePath_YES" not in AdobePagePathStatusList):
				AdobePagePathStatusList[0]="AdobePagePath_YES"
			
			if RE_AdobePagePath_trimmer not in AdobePagePathStatusList:
				if AdobePagePathStatusList[2]==None:
					AdobePagePathStatusList[2]=str(RE_AdobePagePath_trimmer[0])
				
				else:
					AdobePagePathStatusList[2]=AdobePagePathStatusList[2]+"|"+str(RE_AdobePagePath_trimmer[0])
		
	if AdobePagePathStatusList[0]==None:
		AdobePagePathStatusList[0]="AdobePagePath_ABSENT"
		AdobePagePathStatusList[2]="AdobePagePath_NO"
	#print GAStatusList
	return AdobePagePathStatusList

def checkEnsightenBootstrap(page_source):
	
	EnsightenBootstrapStatusList=[None]*3
	#//tags.tiqcdn.com/
	RE_ENSIGHTENBOOTSTRAP= re.findall('Bootstrap.*?', page_source)
	#//tags.tiqcdn.com/utag/telenor/telenor.no/prod/utag.sync.js
	for k in RE_ENSIGHTENBOOTSTRAP:
		RE_EnsightenBootstrap_trimmer= re.findall('Bootstrap.*?',str(k))
		if(RE_EnsightenBootstrap_trimmer!=None):
			if("EnsightenBootstrap_YES" not in EnsightenBootstrapStatusList):
				EnsightenBootstrapStatusList[0]="EnsightenBootstrap_YES"
			
			if RE_EnsightenBootstrap_trimmer not in EnsightenBootstrapStatusList:
				if EnsightenBootstrapStatusList[2]==None:
					EnsightenBootstrapStatusList[2]=str(RE_EnsightenBootstrap_trimmer[0])
				
				else:
					EnsightenBootstrapStatusList[2]=EnsightenBootstrapStatusList[2]+"|"+str(RE_EnsightenBootstrap_trimmer[0])
		
	if EnsightenBootstrapStatusList[0]==None:
		EnsightenBootstrapStatusList[0]="EnsightenBootstrap_ABSENT"
		EnsightenBootstrapStatusList[2]="EnsightenBootstrap_NO"
	#print GAStatusList
	return EnsightenBootstrapStatusList

def checkSCode(page_source):
	
	SCodeStatusList=[None]*3
	#//tags.tiqcdn.com/
	RE_SCODE= re.findall('code.js', page_source)
	#//tags.tiqcdn.com/utag/telenor/telenor.no/prod/utag.sync.js
	for k in RE_SCODE:
		RE_SCode_trimmer= re.findall('code.js',str(k))
		if(RE_SCode_trimmer!=None):
			if("SCode_YES" not in SCodeStatusList):
				SCodeStatusList[0]="SCode_YES"
			
			if RE_SCode_trimmer not in SCodeStatusList:
				if SCodeStatusList[2]==None:
					SCodeStatusList[2]=str(RE_SCode_trimmer[0])
				
				else:
					SCodeStatusList[2]=SCodeStatusList[2]+"|"+str(RE_SCode_trimmer[0])
		
	if SCodeStatusList[0]==None:
		SCodeStatusList[0]="SCode_ABSENT"
		SCodeStatusList[2]="SCode_NO"
	#print GAStatusList
	return SCodeStatusList

def checkTestnTarget(page_source):
	
	TestnTargetStatusList=[None]*3
	#//tags.tiqcdn.com/
	RE_TESTNTARGET= re.findall('mbox.js', page_source)
	#//tags.tiqcdn.com/utag/telenor/telenor.no/prod/utag.sync.js
	for k in RE_TESTNTARGET:
		RE_TestnTarget_trimmer= re.findall('mbox.js',str(k))
		if(RE_TestnTarget_trimmer!=None):
			if("TestnTarget_YES" not in TestnTargetStatusList):
				TestnTargetStatusList[0]="TestnTarget_YES"
			
			if RE_TestnTarget_trimmer not in TestnTargetStatusList:
				if TestnTargetStatusList[2]==None:
					TestnTargetStatusList[2]=str(RE_TestnTarget_trimmer[0])
				
				else:
					TestnTargetStatusList[2]=TestnTargetStatusList[2]+"|"+str(RE_TestnTarget_trimmer[0])
		
	if TestnTargetStatusList[0]==None:
		TestnTargetStatusList[0]="TestnTarget_ABSENT"
		TestnTargetStatusList[2]="TestnTarget_NO"
	#print GAStatusList
	return TestnTargetStatusList

def checkFacebookPixel(page_source):
	
	FacebookPixelStatusList=[None]*3
	#//tags.tiqcdn.com/
	RE_FACEBOOKPIXEL= re.findall('fbq', page_source)
	#//tags.tiqcdn.com/utag/telenor/telenor.no/prod/utag.sync.js
	for k in RE_FACEBOOKPIXEL:
		RE_FacebookPixel_trimmer= re.findall('fbq',str(k))
		if(RE_FacebookPixel_trimmer!=None):
			if("FacebookPixel_YES" not in FacebookPixelStatusList):
				FacebookPixelStatusList[0]="FacebookPixel_YES"
			
			if RE_FacebookPixel_trimmer not in FacebookPixelStatusList:
				if FacebookPixelStatusList[2]==None:
					FacebookPixelStatusList[2]=str(RE_FacebookPixel_trimmer[0])
				
				else:
					FacebookPixelStatusList[2]=FacebookPixelStatusList[2]+"|"+str(RE_FacebookPixel_trimmer[0])
		
	if FacebookPixelStatusList[0]==None:
		FacebookPixelStatusList[0]="FacebookPixel_ABSENT"
		FacebookPixelStatusList[2]="FacebookPixel_NO"
	#print GAStatusList
	return FacebookPixelStatusList

def checkDCMPixel(page_source):
	
	DCMPixelStatusList=[None]*3
	#//tags.tiqcdn.com/
	RE_DCMPIXEL= re.findall('doubleclick', page_source)
	#//tags.tiqcdn.com/utag/telenor/telenor.no/prod/utag.sync.js
	for k in RE_DCMPIXEL:
		RE_DCMPixel_trimmer= re.findall('doubleclick',str(k))
		if(RE_DCMPixel_trimmer!=None):
			if("DCMPixel_YES" not in DCMPixelStatusList):
				DCMPixelStatusList[0]="DCMPixel_YES"
			
			if RE_DCMPixel_trimmer not in DCMPixelStatusList:
				if DCMPixelStatusList[2]==None:
					DCMPixelStatusList[2]=str(RE_DCMPixel_trimmer[0])
				
				else:
					DCMPixelStatusList[2]=DCMPixelStatusList[2]+"|"+str(RE_DCMPixel_trimmer[0])
		
	if DCMPixelStatusList[0]==None:
		DCMPixelStatusList[0]="DCMPixel_ABSENT"
		DCMPixelStatusList[2]="DCMPixel_NO"
	#print GAStatusList
	return DCMPixelStatusList

def checkAdWordsPixel(page_source):
	
	AdWordsPixelStatusList=[None]*3
	#//tags.tiqcdn.com/
	RE_ADWORDSPIXEL= re.findall('google_conversion_id', page_source)
	#//tags.tiqcdn.com/utag/telenor/telenor.no/prod/utag.sync.js
	for k in RE_ADWORDSPIXEL:
		RE_AdWordsPixel_trimmer= re.findall('google_conversion_id',str(k))
		if(RE_AdWordsPixel_trimmer!=None):
			if("AdWordsPixel_YES" not in AdWordsPixelStatusList):
				AdWordsPixelStatusList[0]="AdWordsPixel_YES"
			
			if RE_AdWordsPixel_trimmer not in AdWordsPixelStatusList:
				if AdWordsPixelStatusList[2]==None:
					AdWordsPixelStatusList[2]=str(RE_AdWordsPixel_trimmer[0])
				
				else:
					AdWordsPixelStatusList[2]=AdWordsPixelStatusList[2]+"|"+str(RE_AdWordsPixel_trimmer[0])
		
	if AdWordsPixelStatusList[0]==None:
		AdWordsPixelStatusList[0]="AdWordsPixel_ABSENT"
		AdWordsPixelStatusList[2]="AdWordsPixel_NO"
	#print GAStatusList
	return AdWordsPixelStatusList

#END OF SOURCE CODE CHECK FUNCTIONS

def init_output(outputCSVFile=None):
	
	if(outputCSVFile!=None):
		headerForCSV="No,URL,GTM_Found,NoOfGTM,GTM_Code,GA_Found,NoOfGA,GA_Code,Adobe_Found,NoOfAdobe,Adobe_Code,AdobePagePath_Found,NoOfAdobePagePath,AdobePagePath_Code,Tealium_Found,NoOfTealium,Tealium_Code,EnsightenBootstrap_Found,NoOfEnsightenBootstrap,EnsightenBootstrap_Code,sCode_Found,NoOfsCode,sCode_Code,TestnTarget_Found,NoOfTestnTarget,TestnTarget_Code,Facebook_Found,NoOfFacebook,Facebook_Code,DCM_Found,NoOfDCM,DCM_Code,AdWords_Found,NoOfAdwords,AdWords_Code\n"
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

		try:

			interTime= time.time()

			URLList= [None]*2
			URL= siteLinks.readline().splitlines()[0]
			URLLine= ""+str(i+1)+","+str(URL)

			URLList[0]= i+1
			URLList[1]= URL

			page_source= fetchpage(URL)

			#GTM
			GTMStatusList= checkGTM(page_source)
			GTMs= str(GTMStatusList[2])
			countOfGTMCodes= int(GTMs.count('GTM-'))
			#if(countOfGTMCodes>0):
			#	countOfGTMCodes= countOfGTMCodes +1
			GTMStatusList[1]= countOfGTMCodes
			
			#GA
			GAStatusList= checkGA(page_source)
			GAs= str(GAStatusList[2])
			countOfGACodes= int(GAs.count('UA-'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			GAStatusList[1]= countOfGACodes
			
			#ADOBE
			AdobeStatusList= checkAdobe(page_source)
			Adobes= str(AdobeStatusList[2])
			countOfAdobeCodes= int(Adobes.count('adobe'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			AdobeStatusList[1]= countOfAdobeCodes

			#ADOBE
			AdobePagePathStatusList= checkAdobePagePath(page_source)
			AdobePagePaths= str(AdobePagePathStatusList[2])
			countOfAdobePagePathCodes= int(AdobePagePaths.count('id="pagepath"'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			AdobePagePathStatusList[1]= countOfAdobePagePathCodes

			#Tealium
			TealiumStatusList= checkTealium(page_source)
			Tealiums= str(TealiumStatusList[2])
			countOfTealiumCodes= int(Tealiums.count('tiqcdn'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			TealiumStatusList[1]= countOfTealiumCodes

			#Ensighten
			EnsightenBootstrapStatusList= checkEnsightenBootstrap(page_source)
			EnsightenBootstraps= str(EnsightenBootstrapStatusList[2])
			countOfEnsightenCodes= int(EnsightenBootstraps.count('Bootstrap'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			EnsightenBootstrapStatusList[1]= countOfEnsightenCodes

			#sCode
			sCodeStatusList= checkSCode(page_source)
			sCodes= str(sCodeStatusList[2])
			countOfsCodes= int(sCodes.count('code.js'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			sCodeStatusList[1]= countOfsCodes

			#TestnTarget
			TestnTargetStatusList= checkTestnTarget(page_source)
			TestnTargets= str(TestnTargetStatusList[2])
			countOfTestnTargetCodes= int(TestnTargets.count('mbox.js'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			TestnTargetStatusList[1]= countOfTestnTargetCodes

			#FacebookPixel
			FacebookStatusList= checkFacebookPixel(page_source)
			FacebookPixels= str(FacebookStatusList[2])
			countOfFacebookPixels= int(FacebookPixels.count('fbq'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			FacebookStatusList[1]= countOfFacebookPixels

			#DCMPixel
			DCMPixelStatusList= checkDCMPixel(page_source)
			DCMPixels= str(DCMPixelStatusList[2])
			countOfDCMPixels= int(DCMPixels.count('doubleclick'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			DCMPixelStatusList[1]= countOfDCMPixels

			#AdWords Pixel
			AdWordsPixelStatusList= checkAdWordsPixel(page_source)
			AdWordsPixels= str(AdWordsPixelStatusList[2])
			countOfAdWordsPixels= int(AdWordsPixels.count('google_conversion_id'))
			#if(countOfGACodes>0):
			#	countOfGACodes= countOfGACodes
			AdWordsPixelStatusList[1]= countOfAdWordsPixels


			URL_Code_status= URLList +GTMStatusList +GAStatusList +AdobeStatusList +AdobePagePathStatusList +TealiumStatusList +EnsightenBootstrapStatusList +sCodeStatusList +TestnTargetStatusList +FacebookStatusList +DCMPixelStatusList +AdWordsPixelStatusList
			
			writer_and_printer(outputCSVFile, URL_Code_status)
			endTime= time.time()
			print "I: "+str(endTime-interTime)+"\tT: "+str(endTime-startTime)
			#print("\n\nlength="+page_source);
		except:
			continue
	
	siteLinks.close()
	outputCSVFile.close()

if __name__ == "__main__": main()
