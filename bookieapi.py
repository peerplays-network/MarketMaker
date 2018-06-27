import json
from flask import Flask
from flask import request
from flask import jsonify
from peerplays import PeerPlays
from peerplaysbase import operations
from peerplays.amount import Amount
import bookie

app = Flask(__name__)
ppy = PeerPlays(nobroadcast=True)
ppy.wallet.unlock(bookie.pwd)

@app.route("/placeBets", methods=['POST'])
def placeBets():
	account = request.args['account']
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
		bet_response = ppy.bet_place(betting_market_id, a, odds, back_or_lay, account)
		response.append(bet_response)
	return jsonify(response)

@app.route("/cancelBets/bet/<bet_id>", methods=['DELETE'])
def cancelBets(bet_id):
	# TODO cancel by event id, bmg id
	cancel_response = ppy.bet_cancel(bet_id)
	return jsonify(cancel_response)

@app.route("/bettors/<bettor_id>/unmatchedBets/", methods=['GET'])
def getUnmatchedBets(bettor_id):
	return jsonify(bookie.getUnmatchedBets(bettor_id))

@app.route("/bettors/<bettor_id>/history", methods=['GET'])
def getHistory(bettor_id):
	limit = int(request.args['limit'])
	return jsonify(bookie.getHistory(bettor_id,limit))

@app.route("/sports", methods=['GET'])
def getSports():
	return jsonify(bookie.getSports())

@app.route("/sports/<sport_id>/eventGroups", methods=['GET'])
def getEventGroups(sport_id):
	return jsonify(bookie.getEventGroups(sport_id))

@app.route("/eventGroups/<event_group_id>/events", methods=['GET'])
def getEvents(event_group_id):
	return jsonify(bookie.getEvents(event_group_id))

@app.route("/events/<event_id>/bettingMarketGroups", methods=['GET'])
def getBettingMarketGroups(event_id):
	return jsonify(bookie.getBettingMarketGroups(event_id))

@app.route("/bettingMarketGroups/<bmg_id>/bettingMarkets", methods=['GET'])
def getBettingMarkets(bmg_id):
	return jsonify(bookie.getBettingMarkets(bmg_id))

@app.route("/rules/<rules_id>", methods=['GET'])
def getRules(rules_id):
	return jsonify(bookie.getRules(rules_id))

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=5001)
