import os, datetime, time, json, shutil
import instantbirdLogToPidginLog

class ChatLogConverter:

	def __init__(self):
		self.lastRunTimestamp = 0
		self.instantbirdLogDir = ""
		self.pidginLogDir = ""
		self.filesConvertedCount = 0
		self.startTime = 0
		self.configName = "config.my.json"

	def run(self):
		self.printHello()
		self.readConfig()
		self.convertLogs()
		self.printSummary()
		self.updateTimestempInConfig()

	def printHello(self):
		print("This is Instantbird to Pidgin chat log converter.")

	def readConfig(self):
		if not os.path.exists(self.configName):
			shutil.copyfile('config.default.json', self.configName)
			print("Running for the first time: creating " + self.configName)

		print("Reading " + self.configName)
		with open(self.configName, encoding="utf8") as configFile:
			configData = json.load(configFile)
		self.setupDirectories(configData)
		self.lastRunTimestamp = configData["lastRunTimestamp"]
		print("Will convert only files created after last run (" + str(datetime.datetime.fromtimestamp(self.lastRunTimestamp)) + ")")
		print("")

	def setupDirectories(self, configData):
		self.instantbirdLogDir = configData["instantBirdLogDir"]
		self.pidginLogDir = configData["pidginLogDir"]

		print("Looking for Instantbird logs in:\n" + self.instantbirdLogDir)
		print("Placing Pidgin logs in:\n" + self.pidginLogDir)

		if not os.path.exists(self.instantbirdLogDir):
			raise Exception("Instantbird log directory does not exist! Check " + self.configName + "!")
		if not os.path.exists(self.pidginLogDir):
			raise Exception("Specified Pidgin log directory does not exist! Check " + self.configName + "!")

	def convertLogs(self):
		self.startTime = datetime.datetime.now()
		for dirname, dirnames, filenames in os.walk(self.instantbirdLogDir):
			for subdirname in dirnames:
				self.convertLogsInDirectory(os.path.join(dirname, subdirname))

	def convertLogsInDirectory(self, directory):
		logFilePaths = self.findRelevantLogsIn(directory)
		fileCount = len(logFilePaths)
		if fileCount == 0:
			return
		print("converting " + self.leadingSpaces(fileCount) + " files in " + directory.replace(self.instantbirdLogDir, ""))
		for jsonPath in logFilePaths:
			htmlPath = self.destinationPath(jsonPath)
			instantbirdLogToPidginLog.convertLog(jsonPath, htmlPath)
			self.filesConvertedCount += 1;

	def findRelevantLogsIn(self, directory):
		filePaths = []

		for fileName in os.listdir(directory):
			if fileName.lower().endswith('.json'):
				filePath = os.path.join(directory, fileName)
				if os.path.getmtime(filePath) > self.lastRunTimestamp:
					filePaths.append(filePath)

		return filePaths

	def leadingSpaces(self, integer):
		prefix = ""
		if integer < 1000:
			prefix += " "
		if integer < 100:
			prefix += " "
		if integer < 10:
			prefix += " "
		return prefix + str(integer)

	def destinationPath(self, sourcePath):
		htmlFilename = os.path.splitext(os.path.basename(sourcePath))[0] + ".html"
		sourceDir = os.path.dirname(sourcePath)
		destDir = sourceDir.replace(self.instantbirdLogDir, self.pidginLogDir)
		return os.path.join(destDir, htmlFilename)

	def printSummary(self):
		endTime = datetime.datetime.now()
		timeTaken = endTime - self.startTime
		print("\nConverted " + str(self.filesConvertedCount) + " log files in %.2f seconds." % timeTaken.total_seconds())

	def updateTimestempInConfig(self):
		with open(self.configName, encoding="utf8") as configFile:
			configData = json.load(configFile)
		configData["lastRunTimestamp"] = int(time.time())
		with open(self.configName, "w", encoding="utf8") as configFile:
			json.dump(configData, configFile, indent=4, sort_keys=True)
		print("Wrote lastRunTimestamp:"+ str(int(time.time())) + " to " + self.configName + " to to avoid redundant work next time.")

if __name__ == "__main__":
	ChatLogConverter().run()