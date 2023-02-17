import xbmcaddon
import xbmcgui
import xbmcvfs
import chardet
import re

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

def settingsUpdate():
	topBottomConv = [8,2]
	bordStlConv = [1,3]
	global userSettings
	userSettings = {
		"autoShft" : addon.getSetting("autoShft"), #Auto shift (True / False)
		"autoShftAmt" : int(addon.getSetting("autoShftAmt")), #Auto shift threshold 100=1 sec (Number)
		"manShft" : addon.getSetting("manShft"), #Manual shift both subs (True, False)
		"manShftAmt" : int(addon.getSetting("manShftAmt")), #Manual shift both amount 100=1 sec (Number)
		"manShftSub" : addon.getSetting("manShftSub"), #Manual shift sub master (True, False)
		"manShftSubAmt" : int(addon.getSetting("manShftSubAmt")), #Manual shift sub amount 100=1 sec (Number)
		"fntSize" : addon.getSetting("fntSize"), #Font size in px (Number)
		"forceLineBreak" : addon.getSetting("forceLineBreak"), #Forces same line breaks as SRT file if true (True / False)
		"mastPrimeClr" : addon.getSetting("mastPrimeClr"), #Font color (Hex Color String RRGGBB)
		"subMastPrimeClr" : addon.getSetting("subMastPrimeClr"), #Font color (Hex Color String RRGGBB)
		"mastOutrClr" : addon.getSetting("mastOutrClr"), #Outline/Background color (Hex Color String RRGGBB)
		"subMastOutrClr" : addon.getSetting("subMastOutrClr"), #Outline/Background color (Hex Color String RRGGBB)
		"outrOpcty" : int(addon.getSetting("outrOpcty")), #Outline/Background opacity % (Number 0 - 100)
		"mastShdwClr" : addon.getSetting("mastShdwClr"), #Shadow color (Hex Color String RRGGBB)
		"subMastShdwClr" : addon.getSetting("subMastShdwClr"), #Shadow color (Hex Color String BBGGRR)
		"shdwOpcty" : int(addon.getSetting("shdwOpcty")), #Shadow opacity % (Number 0 - 100)
		"bordStyl" : bordStlConv[int(addon.getSetting("bordStyl"))], #1 Outline and shadow / 3 Solid box (1 / 3)
		"outWid" : addon.getSetting("outWid"), #Text outline width (0 - 4)
		"shdwSize" : addon.getSetting("shdwSize"), #Shadow size (0 - 4)
		"mastLoc" : topBottomConv[int(addon.getSetting("mastLoc"))], #2 Bottom / 8 Top (2 / 8)
		"subMastLoc" : topBottomConv[int(addon.getSetting("subMastLoc"))], #2 Bottom / 8 Top (2 / 8)
		"saveFolder" : addon.getSetting("saveFolder"), #Folder to save subs to
		"permSave" : addon.getSetting("permSave"),
		"autoApply" : addon.getSetting("autoApply"),
		"previewFiles" : addon.getSetting("previewFiles"),
		"warnOvrWrite" : addon.getSetting("warnOvrWrite"),
		"subFldr" : addon.getSetting("subFldr"), #Folder to look for subs in
		"tmpSrch" : addon.getSetting("tmpSrch")
	}

def timeConv(timeStr):
	timeAry = timeStr.split(":")
	totalTime = 0
	totalTime += (int(timeAry[0])*360000)
	totalTime += (int(timeAry[1])*6000)
	totalTime += int(timeAry[2].replace(".",""))
	return totalTime

def timeShift(timeStr, shift):
	timeAryShftd = []
	totalTime = timeConv(timeStr)
	totalTime += shift
	timeAryShftd.append(str(int(totalTime/360000)))
	timeAryShftd.append(str(int((totalTime%360000)/6000)))
	timeAryShftd.append(str(int(((totalTime%360000)%6000)/100)))
	timeAryShftd.append(str(int(((totalTime%360000)%6000)%100)))
	for i in range(1,3):
		if len(timeAryShftd[i]) == 1:
			timeAryShftd[i] = ("0" + timeAryShftd[i])
	timeStrShftd = (timeAryShftd[0] + ":" + timeAryShftd[1] + ":" + timeAryShftd[2] + "." + timeAryShftd[3])
	return timeStrShftd

def colorConv(colorStr, opcty=100):
	opcty = 100 - opcty
	opcty = str(hex(round(opcty * 2.55)))[2:]
	if len(opcty) == 1:
		opcty = "0" + opcty
	col = "&H" + opcty + colorStr[-2:] + colorStr[2:4] + colorStr[:2]
	return col

def srtPreview(sub,title):
	if (sub[-4:] == ".srt"):
		sub = sub.encode(encoding="UTF-8")
		f = open(sub, "rb").read()
		detected = (chardet.detect(f)["encoding"])
		f = f.decode(detected)
		xbmcgui.Dialog().textviewer(title, f)
		del(f)

def fileToArray(subFile, level):
	if (subFile[-4:] == ".srt"):
		subFile = subFile.encode(encoding="UTF-8")
		f = open(subFile, "rb").read()
		detected = (chardet.detect(f)["encoding"])
		f = open(subFile, "r", encoding=detected)
		lines = f.readlines()
		del(f)
	else:
		return []
	
	indx = -1
	strPart = False
	splitArray = []
	if userSettings["forceLineBreak"] == 'true':
		lineBreak = "\\N"
	else:
		lineBreak = "\\n"
	
	for line in lines:
		if "-->" in line:
			indx += 1
			timeSplit = line.replace(",",".").split(" --> ")
			splitArray.append([timeSplit[0][1:-1], timeSplit[1].replace("\n","")[1:-1], ""])
			strPart = True
		elif line == "\n":
			strPart = False
		elif strPart:
			splitArray[indx][2] += line
	for i in range(len(splitArray)):
		splitArray[i][2] = splitArray[i][2].rstrip().replace("\n", lineBreak)
		if len(re.findall("<.>",splitArray[i][2])) > 0:
			splitArray[i][2] = splitArray[i][2].replace("<i>","{\\i1}")
			splitArray[i][2] = splitArray[i][2].replace("<b>","{\\b1}")
			splitArray[i][2] = splitArray[i][2].replace("<u>","{\\u1}")
		splitArray[i][2] = re.sub("<.*?>","",splitArray[i][2])
	shift = 0
	if userSettings["manShft"]:
		shift += userSettings["manShftAmt"]
	if userSettings["manShftSub"] and level == "submaster":
		shift += userSettings["manShftSubAmt"]
	if shift > 0:
		for i in range(len(splitArray)):
			splitArray[i][0] = timeShift(splitArray[i][0], shift)
			splitArray[i][1] = timeShift(splitArray[i][1], shift)
	return splitArray

def alignSubs(mastArray, subMastArray):
	timeThresh = userSettings["autoShftAmt"]
	onSubLine = 0
	for i in range(len(mastArray)):
		mastTime = [timeConv(mastArray[i][0]),timeConv(mastArray[i][1])]
		while onSubLine < len(subMastArray):
			subMastTime = [timeConv(subMastArray[onSubLine][0]),timeConv(subMastArray[onSubLine][1])]
			difs = [mastTime[0] - subMastTime[0], mastTime[1] - subMastTime[1]]
			if abs(difs[0]) <= timeThresh and abs(difs[1]) <= timeThresh:
				subMastArray[onSubLine][0] = mastArray[i][0]
				subMastArray[onSubLine][1] = mastArray[i][1]
				onSubLine += 1
				break
			elif difs[0] < 0 or difs[1] < 0:
				break
			else:
				onSubLine += 1
	return [mastArray, subMastArray]

def arraysToASS(mastArray,subMastArray):
	mastColors = [colorConv(userSettings["mastPrimeClr"]), colorConv(userSettings["mastOutrClr"],userSettings["outrOpcty"]), colorConv(userSettings["mastShdwClr"],userSettings["shdwOpcty"])]
	subMastColors = [colorConv(userSettings["subMastPrimeClr"]), colorConv(userSettings["subMastOutrClr"],userSettings["outrOpcty"]), colorConv(userSettings["subMastShdwClr"],userSettings["shdwOpcty"])]
	if xbmcvfs.exists("special://home/temp/"):
		fileRoot = "special://home/temp/"
	else:
		fileRoot = "special://home/cache/"
	fileName = ("subtitle")
	if userSettings["permSave"] == "true":
		fileName = xbmcgui.Dialog().input("Choose your new file name")
		fileRoot = userSettings["saveFolder"]
	fileSpot = fileRoot + fileName + ".ass"
	if userSettings["warnOvrWrite"]  == "true" and xbmcvfs.exists(fileSpot):
		txt = "You are about to replace the file\n" + fileSpot + "\nDo you want to continue?"
		leave = xbmcgui.Dialog().yesno('Warning', txt)
		if not leave:
			quit()
	with xbmcvfs.File(fileSpot, 'w') as f:
		f.write("[Script Info]\n; Generated at mattrangel.net\nTitle: Subtitles\nScriptType: v4.00+\nCollisions: Normal\nPlayDepth: 0\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
		f.write("Style: Default, Arial, " + str(userSettings["fntSize"]) + ", " + mastColors[0] + ", &H0300FFFF, " + mastColors[1] + ", " + mastColors[2] + ", 0, 0, " + str(userSettings["bordStyl"]) + ", " + str(userSettings["outWid"]) + ", " + str(userSettings["shdwSize"]) + ", " + str(userSettings["mastLoc"]) + ", 10, 10, 10, 1\n")
		f.write("Style: Secondary, Arial, " + str(userSettings["fntSize"]) + ", " + subMastColors[0] + ", &H0300FFFF, " + subMastColors[1] + ", " + subMastColors[2] + ", 0, 0, " + str(userSettings["bordStyl"]) + ", " + str(userSettings["outWid"]) + ", " + str(userSettings["shdwSize"]) + ", " + str(userSettings["subMastLoc"]) + ", 10, 10, 10, 1\n\n")
		f.write("[Events]\nFormat: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n")
		mastLen = len(mastArray)
		subMastLen = len(subMastArray)
		for i in range(mastLen):
			f.write("Dialogue: 0," + mastArray[i][0] + "," + mastArray[i][1]  + ",Default,,0,0,0,," + mastArray[i][2]  + "\n")
		for i in range(subMastLen):
			f.write(("Dialogue: 0," + subMastArray[i][0] + "," + subMastArray[i][1] + ",Secondary,,0,0,0,," + subMastArray[i][2] + "\n"))
		f.close()
	return fileSpot

def autoApply(file):
	if xbmc.Player().isPlayingVideo():
		xbmc.Player().setSubtitles(file)
		xbmc.executebuiltin("ActivateWindow(fullscreenvideo)")
	
def run():
	settingsUpdate()
	if userSettings["tmpSrch"] == "true":
		if xbmcvfs.exists("special://home/temp/"):
			userSettings["subFldr"] = "special://home/temp/"
		else:
			userSettings["subFldr"] = "special://home/cache/"
	mf = xbmcgui.Dialog().browseSingle(1, "Select Master File", "", ".srt", False, False, userSettings["subFldr"])
	smf = xbmcgui.Dialog().browseSingle(1, "Select Sub-Master File", "", ".srt", False, False, userSettings["subFldr"])
	mf = xbmcvfs.translatePath(mf)
	smf = xbmcvfs.translatePath(smf)
	if userSettings["previewFiles"] == "true":
		srtPreview(mf, "Preview Master File")
		srtPreview(smf, "Preview Sub-Master File")
		xbmc.executebuiltin("Addon.OpenSettings(script.submerge)", True)
		settingsUpdate()
	if userSettings["autoShft"] == "true":
		z = alignSubs(fileToArray(mf,"master"),fileToArray(smf,"submaster"))
	else:
		z = [fileToArray(mf,"master"),fileToArray(smf,"submaster")]
	fileSpot = arraysToASS(z[0],z[1])
	del(z)
	if userSettings["autoApply"] == "true":
		autoApply(fileSpot)

run()

