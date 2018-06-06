from flask import Flask
from flask import request
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
	req_data = request.get_json()
	asset_symbol = req_data['asset_symbol']
	bet_amount = req_data['bet_amount']
	betting_market_id = req_data['betting_market_id']
	odds = req_data['odds']
	back_or_lay = req_data['back_or_lay']
	a  = Amount(bet_amount, asset_symbol)
	ppy.bet_place(betting_market_id, a, odds, back_or_lay)
	return "Bet Placed\n"

@app.route("/cancelBets/bet/<bet_id>", methods=['DELETE'])
def cancelBets(bet_id):
	ppy.bet_cancel(bet_id)
	return "Bet {} cancelled\n".format(bet_id)

@app.route("/sports", methods=['GET'])
def getSports():
	sports = Sports(peerplays_instance=ppy)
	sports = pretty_print(sports)
	# TODO format into JSON response
	return psports

@app.route("/sports/<sport_id>/eventGroups")
def getEventGroups(sport_id):
	event_groups = Sport(sport_id, peerplays_instance=ppy)
	pevent_groups = pretty_print(event_groups.eventgroups)
	# TODO format into JSON response
	return peventgroups

@app.route("/eventGroups/<event_group_id>/events")
def getEvents(event_group_id):
	events = EventGroup(event_group_id, peerplays_instance=ppy)
	pevents = pretty_print(events.events)
	# TODO format into JSON response
	return pevents

@app.route("/events/<event_id>/bettingMarketGroups")
def getBettingMarketGroups(event_id):
	bmgs = Event(event_id, peerplays_instance=ppy)
	pbmgs = pretty_print(bmgs.bettingmarketgroups)
	# TODO format into JSON response
	return pbmgs

@app.route("/bettingMarketGroups/<bmg_id>/bettingMarkets")
def getBettingMarkets(bmg_id):
	betting_markets = BettingMarketGroup(bmg_id, peerplays_instance=ppy)
	pbetting_markets = pretty_print(betting_markets.bettingmarkets)
	# TODO format into JSON response
	return pbetting_markets

@app.route("/rules/<rules_id>")
def getRules(rules_id):
	rules = Rule(rules_id, peerplays_instance=ppy)
	# TODO format into JSON response
	pprint(rules)
	return ""

if __name__ == '__main__':
	app.run(debug=False)
