import json, os

def convertLog(jsonFilePath, htmlFilePath):
	logObjects = parseFile(jsonFilePath)
	logHtml = createHtml(logObjects)
	writeToFile(logHtml, htmlFilePath)

def parseFile(filename):
	jsonObjects = []
	with open(filename, encoding="utf8") as instantbirdLogFile:
		for line in instantbirdLogFile:
			jsonObjects.append(json.loads(line))
	instantbirdLogFile.close()
	return jsonObjects

def createHtml(logObjects):
	title = createTitle(logObjects[0])

	head = "<head><meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\"><title>" + title + "</title></head>"
	heading = "<h3>" + title + "</h3>\n"

	posts = createPostsHtml(logObjects)

	body = "<body>" + heading + posts + "</body>"
	html = "<html>" + head + body + "</html>"

	return html

def createTitle(headObjects):
	buddyId = headObjects['name']
	formattedDate = formatDate(headObjects['date'])
	accountId = headObjects['account']
	protocol = headObjects['protocol']

	return "Conversation with " + buddyId + " at " + formattedDate + " on "+ accountId + " (" + protocol + ")"

def formatDate(dateString):
	return dateString.replace('T', ' ')[:19]

def createPostsHtml(logObjects):
	postsHtml = ""
	for postObject in logObjects:
		postsHtml += createPostHtml(postObject)
	return postsHtml

def createPostHtml(postObject):
	if not "text" in postObject:
		return ''
	if not "alias" in postObject:
		return ''
	text = sanitizePostText(postObject['text'])
	time = formatTime(postObject['date'])
	alias = postObject['alias']
	color = postColor(postObject['flags'])

	postHtml = "<font color=\"" + color + "\"><font size=\"2\">" + time + "</font> <b>" + alias + ":</b></font> " + text + "<br/>\n"
	return postHtml

def sanitizePostText(postText):
	return postText.replace("<BODY>", "").replace("</BODY>", "")

def formatTime(dateString):
	return "(" + dateString[11:19] + ")"

def postColor(postObjectFlags):
	if('incoming' in postObjectFlags):
		return "#A82F2F"
	return "#16569E"

def writeToFile(text, path):
	dirPath = os.path.dirname(path)
	if not os.path.exists(dirPath):
		os.makedirs(dirPath)
	with open(path, 'w', encoding="utf8") as f:
		f.write(text)


if __name__ == "__main__":
    print("usage: python chatLogConverter.py")