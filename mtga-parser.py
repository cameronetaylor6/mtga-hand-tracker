from html.parser import HTMLParser
import json
import os
import codecs
from mtga.set_data import all_mtga_cards

class MyHTMLParser(HTMLParser):
	def handle_data(self, data):
		global matchId
		global searchForHands
		global cards
		gameStart = "DuelScene.GameStart"
		possibleStartingHand = '"prevGameStateId":'
		endOfStartingHand = '"turnNumber": 1,'
		zones = "zones"
		gameEnd = "DuelScene.GameStop"

		if data.find(gameStart) >= 0:
			# print("Found DieRoll")

			# remove first two lines of data (html divs)
			postString = data.split("\n",2)[2];
			data2 = json.loads(postString)
			try:
				matchId = data2["params"]["payloadObject"]["matchId"]
				eventId = data2["params"]["payloadObject"]["eventId"]
			except:	
				# print("Error: No matchId data")
				return
			pass
			print("id: " + matchId)
			print("match type: " + eventId)
		elif matchId != "" and data.find(endOfStartingHand) >= 0:
			# print("Found First Turn")
			searchForHands = False
		elif matchId != "" and searchForHands and data.find(possibleStartingHand) >= 0 and data.find(zones) >= 0:
			# print("Found Cards in Hand")

			# remove first line of data (html div)
			postString = data.split("\n",1)[1];
			data2 = json.loads(postString)
			try:
				cards = data2["greToClientEvent"]["greToClientMessages"][0]["gameStateMessage"]["gameObjects"]
			except:
				# gameStateId = data2["greToClientEvent"]["greToClientMessages"][0]["gameStateMessage"]["gameStateId"]
				# print("Error: No card data with id:" + matchId + ", gameStateId: " +str(gameStateId))
				return
		elif matchId != "" and data.find(gameEnd) >= 0:
			# print("Found MatchCompleted")

			# remove first two lines of data (html divs)
			postString = data.split("\n",2)[2];
			data2 = json.loads(postString)

			# check that GameEnd matchId is same as GameStart
			resultmatchId = data2["params"]["payloadObject"]["matchId"]
			if matchId != resultmatchId:
				print("Error: Could not find winner with id: " + matchId)
				return
			print("Final Hand")

			postCards = []
			# just take the groupId from cards since that's all we need
			for card in cards:
				postCards.append(card['grpId'])
			for card in postCards:
				print(all_mtga_cards.find_one(card))
			
			owner = data2["params"]["payloadObject"]["seatId"]
			winner = data2["params"]["payloadObject"]["winningTeamId"]
			print("Owner: " + str(owner))
			print("Winner: " + str(winner))

			mulliganedHands = data2["params"]["payloadObject"]["mulliganedHands"]
			if len(mulliganedHands) > 0:
				print("Mulliganed Hands: ")
				i = 1
				for hand in mulliganedHands:
					print("Hand " + str(i) + ":")
					i = i + 1
					for card in hand:
						print(all_mtga_cards.find_one(card['grpId']))
			print()

			# reset globals
			matchId = ""
			searchForHands = True
			cards = []

parser = MyHTMLParser()
baseDir = "./Logs"
matchId = ""
searchForHands = True
cards = []

for root, dirs, files in os.walk(baseDir):
	print( dirs )
	for filename in files:
		if(filename.find("Log") > -1):
			print(filename)
			print()
			f = open(baseDir + "/" + filename, 'r')
			parser.feed(f.read())
			f.close()
			print()
			print()
