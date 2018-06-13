import requests
from peerplays import PeerPlays
from getpass import getpass
from pprint import pprint
import bookie
import json

def placeBetHelper(gameName, teamName, odds, side, ppy):
	events = json.loads(json.dumps(bookie.getEvents('1.17.3'))) # world cup group stages on elizabeth
	for event in events:
		#go until betting_event = event['name'] == gameName
		#bmg = betting_event['match_odds']
		#loop through bmg until betting_market['name'] = teamname
	# ppy.bet_place(betting_market_id, amount, odds, back_or_lay)

if __name__ == '__main__':
	ppy = PeerPlays(nobroadcast=True) # no need to unlock, the bookieapi import does that for us

	url = "https://api.matchbook.com/edge/rest/events?category-ids=15,400798618290009,410468520880009,617663353250012&exchange-type=back-lay&odds-type=DECIMAL&price-depth=1"

	response = requests.get(url)
	json_response = response.json()
	for event in json_response['events']:
		# print(event['name'])
		for market in event['markets']:
		# if (market['name'] == "Match Odds" and market['in-running-flag']):
			if (market['name'] == "Match Odds"): # aka if bettingmarketgroup = moneyline
				for runner in market['runners']: # runner is a bettingmarket
					placeBetHelper(event['name'], runner['name'], runner['prices'][0]['odds'], runner['prices'][0]['side'], ppy) #one back
					placeBetHelper(event['name'], runner['name'], runner['prices'][1]['odds'], runner['prices'][1]['side'], ppy) #one lay
