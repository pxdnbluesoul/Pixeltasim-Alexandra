from whiffle import wikidotapi
from util import hook
import re
import time,threading
import thread
import __builtin__

def return_final(page):
		title = titlelist[page]
		rating = ratinglist[page]
		is_title = 0
		try:
			if scptitles[page]:
				is_title = 1
		except KeyError:
			pass 
		if is_title ==1:
			scptitle = scptitles[page]
			string = ""+scptitle+""+"("+title+", Rating:"+str(rating)+")"
			return string
		else:
			string = ""+title+""+"(Rating:"+str(rating)+")"
			return string 
			
@hook.command("s")
@hook.command("sea")
def sea(inp): #this is for WL use, easily adaptable to SCP
	".sea <Article Name> -- Will return first three pages containing exact matches to Article Name, with number of other matches"
	line = re.sub("[ ,',_]",'-',inp) #removes spaces and apostrophes and replaces them with dashes, per wikidot's standards
	results = []
	for page in scppages: 
		if line.lower() in page.lower(): #check for first match to input
			if "tale" in taglist[page] or "scp" in taglist[page] or "essay" in taglist[page]or "hub" in taglist[page]or "goi-format" in taglist[page]: #check for tag
				results.append(page)
				continue 
			else:
				print "UPDATE NEEDED! PAGE LISTED NO LONGER EXISTS:"
				print page
		if inp.lower() in titlelist[page].lower():
			if "tale" in taglist[page] or "scp" in taglist[page] or "essay" in taglist[page]or "hub" in taglist[page]or "goi-format" in taglist[page]: #check for tag
				results.append(page)
		try:
			if scptitles[page]:
				if inp.lower() in re.sub('["]',"",scptitles[page].lower()):
					if "tale" in taglist[page] or "scp" in taglist[page]: #check for tag
						results.append(page)
		except KeyError:
			pass
	if results == []:
		return "No matches found."
	final = ""
	third = 0
	for result in results:
		third+=1
		if third == 1:
			final+= return_final(result)
		if third<=3 and third != 1:
			final += ", "+return_final(result)
	if third>3:
		final += ", With " + str(third-3) + " more matches."
	if third==1:
		page = results[0]
		final = return_final(page)+" - http://www.scp-wiki.net/"+page
	__builtin__.seaiter = 1
	__builtin__.searesults = results
	return final
				
@hook.command("sm")
@hook.command("showmore")
def showmore(inp):
	final = ""
	minval = seaiter*3+1
	maxval = seaiter*3+3
	__builtin__.seaiter +=1
	val= 0
	for result in searesults:
		val+=1
		if val == minval:
			final+= return_final(result)
		if val<=maxval and val != minval and val>minval:
			final+= ", "+return_final(result)
	if val>maxval:
		final += ", With " + str(val-maxval) + " more matches."
	if final == "":
		return "There are no more matches to show."
	return final 