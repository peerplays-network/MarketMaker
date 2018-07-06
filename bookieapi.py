import json
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask import make_response
from peerplays import PeerPlays
from peerplaysbase import operations
from peerplays.amount import Amount
from peerplays.exceptions import *
import bookie

app = Flask(__name__)
ppy = PeerPlays(nobroadcast=True)
ppy.wallet.unlock(bookie.pwd)

@app.route("/placeBets", methods=['POST'])
def placeBets():
	try:
		account = request.args.get("account")
		body = request.get_json()
		response = []
		for bet in body:
			asset_symbol = bet['asset_symbol']
			bet_amount = bet['bet_amount']
			betting_market_id = bet['betting_market_id']
			odds = bet['odds']
			back_or_lay = bet['back_or_lay']
			a  = Amount(bet_amount, asset_symbol)
			#right now, we will place bets successfully one by one until one breaks.
			#the user will be confused whether any of the bets got placed or not
			bet_response = ppy.bet_place(betting_market_id, a, odds, back_or_lay, account, fee_asset = asset_symbol)
			response.append(bet_response)
		return jsonify(response)
	except Exception as e:
		return jsonify(error=e.__doc__)

@app.route("/bets/<bet_id>", methods=['DELETE'])
def cancelBets(bet_id):
	try:
		# TODO cancel by event id, bmg id
		account = request.args.get("account")
		cancel_response = ppy.bet_cancel(bet_id, account)
		return jsonify(cancel_response)
	except Exception as e:
		return jsonify(error=e.__doc__)

@app.route("/bettors/<bettor_id>/unmatchedBets/", methods=['GET'])
def getUnmatchedBets(bettor_id):
	try:
		return jsonify(bookie.getUnmatchedBets(bettor_id))
	except Exception as e:
		return jsonify(error=e.__doc__)

# @app.route("/bettors/<bettor_id>/matchedBets", methods=['GET'])
# def getMatchedBets(bettor_id):
#	try:
# 		return jsonify(bookie.getMatchedBets(bettor_id))
#	except Exception as e:
#		return jsonify(error=e.__doc__)

@app.route("/bettors/<bettor_id>/history", methods=['GET'])
def getHistory(bettor_id):
	try:
		limit = int(request.args['limit'])
		return jsonify(bookie.getHistory(bettor_id,limit))
	except Exception as e:
		return jsonify(error=e.__doc__)

@app.route("/sports", methods=['GET'])
def getSports():
	try:
		return jsonify(bookie.getSports())
	except Exception as e:
		return jsonify(error=e.__doc__)

@app.route("/sports/<sport_id>/eventGroups", methods=['GET'])
def getEventGroups(sport_id):
	try:
		return jsonify(bookie.getEventGroups(sport_id))
	except Exception as e:
		return jsonify(error=e.__doc__)

@app.route("/eventGroups/<event_group_id>/events", methods=['GET'])
def getEvents(event_group_id):
	try:
		return jsonify(bookie.getEvents(event_group_id))
	except Exception as e:
		return jsonify(error=e.__doc__)

@app.route("/events/<event_id>/bettingMarketGroups", methods=['GET'])
def getBettingMarketGroups(event_id):
	try:
		return jsonify(bookie.getBettingMarketGroups(event_id))
	except Exception as e:
		return jsonify(error=e.__doc__)

@app.route("/bettingMarketGroups/<bmg_id>/bettingMarkets", methods=['GET'])
def getBettingMarkets(bmg_id):
	try:
		return jsonify(bookie.getBettingMarkets(bmg_id))
	except Exception as e:
		return jsonify(error=e.__doc__)

@app.route("/rules/<rules_id>", methods=['GET'])
def getRules(rules_id):
	try:
		return jsonify(bookie.getRules(rules_id))
	except Exception as e:
		return jsonify(error=e.__doc__)

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=5051)
