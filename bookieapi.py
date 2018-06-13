import json
from flask import Flask
from flask import request
from flask import jsonify
from peerplays import PeerPlays
from peerplaysbase import operations
from peerplays.account import Account
from peerplays.amount import Amount
import bookie

app = Flask(__name__)
ppy = PeerPlays(nobroadcast=True)
ppy.wallet.unlock(bookie.pwd)

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
def getUnmatchedBets(bettor_id):
	return jsonify(bookie.getUnmatchedBets(bettor_id))

@app.route("/sports", methods=['GET'])
def getSports():
	return jsonify(bookie.getSports())

@app.route("/sports/<sport_id>/eventGroups")
def getEventGroups(sport_id):
	return jsonify(bookie.getEventGroups(sport_id))

@app.route("/eventGroups/<event_group_id>/events")
def getEvents(event_group_id):
	return jsonify(bookie.getEvents(event_group_id))

@app.route("/events/<event_id>/bettingMarketGroups")
def getBettingMarketGroups(event_id):
	return jsonify(bookie.getBettingMarketGroups(event_id))

@app.route("/bettingMarketGroups/<bmg_id>/bettingMarkets")
def getBettingMarkets(bmg_id):
	return jsonify(bookie.getBettingMarkets(bmg_id))

@app.route("/rules/<rules_id>")
def getRules(rules_id):
	return jsonify(bookie.getRules(rules_id))

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')
