import requests
from peerplays import PeerPlays
from getpass import getpass
import bookie
import json
import time
import random
from peerplays.amount import Amount

def placeBetHelper(startTime, runner, ppy):
	with open('events.txt', 'r') as eventsfile: #this file holds all the events for eventgroup 1.17.3 = world cup group stage
		events = json.loads(eventsfile.read())
	for event in events:
		if (event['start_time'] == startTime[:-5]): #find the right game, by start time
			bmgs = json.loads(json.dumps(bookie.getBettingMarketGroups(event['id'])))
			for bmg in bmgs: # find the moneyline bmg
				if (bmg['description'][0][1] == "Match Odds"):
					markets = json.loads(json.dumps(bookie.getBettingMarkets(bmg['id'])))
					for market in markets: # find the betting market for this team
						if (market['description'][0][1] == runner['name'] or market['description'][0][1][-4:].upper() == runner['name'][:4]):
							print(ppy.bet_place(market['id'], Amount(random.uniform(0.02, 0.08), "BTF"), runner['prices'][0]['odds'], runner['prices'][0]['side']))
							print(ppy.bet_place(market['id'], Amount(random.uniform(0.02, 0.08), "BTF"), runner['prices'][1]['odds'], runner['prices'][1]['side']))

def cancelUnmatchedBets(ppy):
	unmatched = json.loads(json.dumps(bookie.getUnmatchedBets("1.2.18"))) # account id of bettor
	for bet in unmatched:
		print(ppy.bet_cancel(bet['id']))

if __name__ == '__main__':
	ppy = PeerPlays(nobroadcast=True)
	ppy.wallet.unlock(bookie.pwd)
	url = "https://api.matchbook.com/edge/rest/events?category-ids=15,400798618290009,410468520880009,617663353250012&exchange-type=back-lay&odds-type=DECIMAL&price-depth=1"

	while True:
		cancelUnmatchedBets(ppy)
		response = requests.get(url)
		json_response = response.json()
		for event in json_response['events']:
			for market in event['markets']:
				if (market['name'] == "Match Odds" and market['in-running-flag']): # aka if bettingmarketgroup = moneyline
				# if (market['name'] == "Match Odds" and market['start'] == "2018-06-14T15:00:00.000Z"): # aka if bettingmarketgroup = moneyline
					for runner in market['runners']: # runner is a bettingmarket
						placeBetHelper(event['start'], runner, ppy)
		time.sleep(30)
