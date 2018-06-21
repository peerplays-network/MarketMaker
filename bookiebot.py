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
	if (x <= 1000 and x > 100):
		return round(10 * round(float(x)/10),0)
	elif (x <= 100 and x > 50):
		return round(5 * round(float(x)/5),0)
	elif (x <= 50 and x > 30):
		return round(2 * round(float(x)/2),0)
	elif (x <= 30 and x > 20):
		return round(1 * round(float(x)/1),0)
	elif (x <= 20 and x > 10):
		return round(0.5 * round(float(x)/0.5), 1)
	elif (x <= 10 and x > 6):
		return round(0.2 * round(float(x)/0.2), 1)
	elif (x <= 6 and x > 4):
		return round(0.1 * round(float(x)/0.1), 1)
	elif (x <= 4 and x > 3):
		return round(0.05 * round(float(x)/0.05), 2)
	elif (x <= 3 and x > 2):
		return round(0.02 * round(float(x)/0.02), 2)
	elif (x <= 2):
		return round(0.01 * round(float(x)/0.01), 2)
	else:
		return float('%.2f'%(x))

def cancelUnmatchedBets(ppy):
	num_bets_cancelled = 0
	unmatched = json.loads(json.dumps(bookie.getUnmatchedBets("1.2.769"))) # account id of market-maker
	for bet in unmatched:
		try:
			start_time = time.time()
			print(ppy.bet_cancel(bet['id'], fee_asset="1.3.1"))
			end_time = time.time()
			# print("Took ",end_time - start_time,"to cancel bet")
			num_bets_cancelled += 1
		except:
			print('Could not cancel bet.')
			continue
	return num_bets_cancelled

def placeBetHelper(runners, mappings, ppy):
	print("Entered placeBetHelper")
	num_bets_placed = 0
	for runner in runners:
		runners_event_id = str(runner['event-id'])
		event_id = mappings[runners_event_id]

		bmgs = json.loads(json.dumps(bookie.getBettingMarketGroups(event_id)))
		for bmg in bmgs: # find the moneyline and totals bmg
			markets = json.loads(json.dumps(bookie.getBettingMarkets(bmg['id'])))
			for market in markets: # find the betting market for this team
				 # if statement to trim list down to Match Odds and Totals
				if (market['description'][0][1] == runner['name'] or market['description'][0][1][-4:].upper() == runner['name'][:4] or market['description'][0][1][:-6].upper() == runner['name']):
					try:
						print("Betting on betting market ", market['id'])
						if (runner['prices'][0]):
							amount = Amount(random.uniform(0.02, 0.08), "BTF")
							odds = odds_round(runner['prices'][0]['odds'])
							start_time = time.time()
							print(ppy.bet_place(market['id'], amount, odds, runner['prices'][0]['side'], fee_asset = "1.3.1"))
							num_bets_placed += 1
							end_time = time.time()
							# print("Took ",end_time - start_time,"to place bet")
						if (runner['prices'][1]):
							amount = Amount(random.uniform(0.02, 0.08), "BTF")
							odds = odds_round(runner['prices'][1]['odds'])
							start_time = time.time()
							print(ppy.bet_place(market['id'], amount, odds, runner['prices'][1]['side'], fee_asset="1.3.1"))
							num_bets_placed += 1
							end_time = time.time()
							# print("Took ",end_time - start_time,"to place bet")
					except:
						print('Handling exception... bad odds?')
	return num_bets_placed

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
	num_bets_placed = 0
	num_bets_cancelled = 0
	while True:
		print("Cancelling...")
		num_bets_cancelled += cancelUnmatchedBets(ppy)
		print("Cancelled")
		print("Getting odds...")
		response = requests.get(url)
		print("Got odds")
		json_response = response.json()
		for event in json_response['events']:
			for market in event['markets']:
				# if (market['name'] == "Match Odds" and market['start'] == "2018-06-21T15:00:00.000Z"): # aka if bettingmarketgroup = moneyline
				if (market['in-running-flag'] and (market['name'] == "Match Odds" or market['name'] == "Total")): # aka if bettingmarketgroup = moneyline
					num_bets_placed += placeBetHelper(market['runners'], mappings, ppy)
					something_in_play = True
		if (something_in_play):
			print("Something in play, sleeping for 10s")
			something_in_play = False
			time.sleep(10)
		else:
			if (num_bets_placed > 0):
				print("I placed ",num_bets_placed," bets")
				num_bets_placed = 0
			if (num_bets_cancelled > 0):
				print("I cancelled ",num_bets_cancelled," bets")
				num_bets_cancelled = 0
			print("Nothing in play, sleeping for 5m")
			something_in_play = False
			time.sleep(300)
