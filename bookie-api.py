import json
from flask import Flask
from flask import request
from flask import jsonify
from peerplays import PeerPlays
from getpass import getpass
from peerplaysbase import operations
from peerplays.account import Account
from peerplays.amount import Amount
from pprint import pprint
from peerplays.sport import Sport, Sports
from peerplays.eventgroup import EventGroup, EventGroups
from peerplays.event import Event, Events
from peerplays.bettingmarketgroup import BettingMarketGroup, BettingMarketGroups
from peerplays.bettingmarket import BettingMarket, BettingMarkets
from peerplays.rule import Rule, Rules
from peerplays.cli.ui import pretty_print

app = Flask(__name__)

pwd = getpass()
ppy = PeerPlays(nobroadcast=False)
ppy.wallet.unlock(pwd)

@app.route("/placeBets", methods=['POST'])
def placeBets():
	body = request.get_json()
	response = []
	for bet in body['bets']:
		asset_symbol = bet['asset_symbol']
		bet_amount = bet['bet_amount']
		betting_market_id = bet['betting_market_id']
		odds = bet['odds']
		back_or_lay = bet['back_or_lay']
		a  = Amount(bet_amount, asset_symbol)
		#right now, we will place bets successfully one by one until one breaks.
		#the user will be confused whether any of the bets got placed or not
		bet_response = ppy.bet_place(betting_market_id, a, odds, back_or_lay)
		response.append(bet_response)
	return jsonify(response)

@app.route("/cancelBets/bet/<bet_id>", methods=['DELETE'])
def cancelBets(bet_id):
	# TODO cancel by event id, bmg id
	cancel_response = ppy.bet_cancel(bet_id)
	return jsonify(cancel_response)

@app.route("/unmatchedBets/bettor/<bettor_id>", methods=['GET'])
def unmatchedBets(bettor_id):
	response = []
	unmatched_bets = ppy.rpc.get_all_unmatched_bets_for_bettor("1.2.18")
	response.append(unmatched_bets)
	return jsonify(response)

@app.route("/sports", methods=['GET'])
def getSports():
	sports = Sports(peerplays_instance=ppy)
	# TODO Add pagination 
	return jsonify(sports.sports)

@app.route("/sports/<sport_id>/eventGroups")
def getEventGroups(sport_id):
	event_groups = Sport(sport_id, peerplays_instance=ppy)
	# TODO add pagination
	return jsonify(event_groups.eventgroups)

@app.route("/eventGroups/<event_group_id>/events")
def getEvents(event_group_id):
	events = EventGroup(event_group_id, peerplays_instance=ppy)
	# TODO add pagination
	return jsonify(events.events)

@app.route("/events/<event_id>/bettingMarketGroups")
def getBettingMarketGroups(event_id):
	bmgs = Event(event_id, peerplays_instance=ppy)
	# TODO add pagination
	return jsonify(bmgs.bettingmarketgroups)

@app.route("/bettingMarketGroups/<bmg_id>/bettingMarkets")
def getBettingMarkets(bmg_id):
	betting_markets = BettingMarketGroup(bmg_id, peerplays_instance=ppy)
	# TODO add pagination
	return jsonify(betting_markets.bettingmarkets)

@app.route("/rules/<rules_id>")
def getRules(rules_id):
	rules = Rule(rules_id, peerplays_instance=ppy)
	# TODO add pagination
	return jsonify(rules)

if __name__ == '__main__':
	app.run(debug=False)
