import requests
from peerplays import PeerPlays
from getpass import getpass
import bookie
import json
import csv
import time
import random
from peerplays.amount import Amount

# this function exists to deal with the precision of the backing_multiplier
def odds_round(x):
	if (x >= 50):
		return round(50 * round(float(x)/50),2)
	elif (x >= 10):
		return round(0.5 * round(float(x)/0.5),2)
	else:
		return float('%.2f'%(x))

def cancelUnmatchedBets(ppy):
	unmatched = json.loads(json.dumps(bookie.getUnmatchedBets("1.2.769"))) # account id of market-maker
	for bet in unmatched:
		try:
			print(ppy.bet_cancel(bet['id']))
		except:
			print('Could not cancel bet.')

def placeBetHelper(runners, mappings, ppy):
	print("Entered placeBetHelper")
	for runner in runners:
		runners_event_id = str(runner['event-id'])
		event_id = mappings[runners_event_id]

		bmgs = json.loads(json.dumps(bookie.getBettingMarketGroups(event_id)))
		for bmg in bmgs: # find the moneyline bmg
			if (bmg['description'][0][1] == "Match Odds"):
				markets = json.loads(json.dumps(bookie.getBettingMarkets(bmg['id'])))
				for market in markets: # find the betting market for this team
					if (market['description'][0][1] == runner['name'] or market['description'][0][1][-4:].upper() == runner['name'][:4]):

						try:
							print("Betting on betting market ", market['id'])
							if (runner['prices'][0]):
								print(ppy.bet_place(market['id'], Amount(random.uniform(0.02, 0.08), "BTF"), odds_round(runner['prices'][0]['odds']), runner['prices'][0]['side']))
							if (runner['prices'][1]):
								print(ppy.bet_place(market['id'], Amount(random.uniform(0.02, 0.08), "BTF"), odds_round(runner['prices'][1]['odds']), runner['prices'][1]['side']))
						except:
							print('Handling exception... bad odds?')

if __name__ == '__main__':
	ppy = PeerPlays(nobroadcast=False)
	ppy.wallet.unlock(bookie.pwd)
	url = "https://api.matchbook.com/edge/rest/events?category-ids=15,400798618290009,410468520880009,617663353250012&exchange-type=back-lay&odds-type=DECIMAL&price-depth=1"
	with open('mapping.txt', 'r') as mappingsfile:
		reader = csv.reader(mappingsfile)
		mappings = {}
		for row in reader:
			k, v = row
			mappings[k] = v

	something_in_play = False
	while True:
		print("Cancelling...")
		cancelUnmatchedBets(ppy)
		print("Cancelled")
		print("Getting odds...")
		response = requests.get(url)
		print("Got odds")
		json_response = response.json()
		for event in json_response['events']:
			for market in event['markets']:
				if (market['name'] == "Match Odds" and market['in-running-flag']): # aka if bettingmarketgroup = moneyline
				# if (market['name'] == "Match Odds" and market['start'] == "2018-06-15T12:00:00.000Z"): # aka if bettingmarketgroup = moneyline
					placeBetHelper(market['runners'], mappings, ppy)
					something_in_play = True
		if (something_in_play):
			print("Something in play, sleeping for 20s")
			something_in_play = False
			time.sleep(20)
		else:
			print("Nothing in play, sleeping for 15m")
			something_in_play = False
			time.sleep(900)
