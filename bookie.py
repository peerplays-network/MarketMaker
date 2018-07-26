import json
from getpass import getpass
from peerplays import PeerPlays
from peerplays.account import Account
from peerplays.sport import Sport, Sports
from peerplays.eventgroup import EventGroup, EventGroups
from peerplays.event import Event, Events
from peerplays.bettingmarketgroup import BettingMarketGroup, BettingMarketGroups
from peerplays.bettingmarket import BettingMarket, BettingMarkets
from peerplays.rule import Rule, Rules

pwd = getpass()
ppy = PeerPlays(nobroadcast=True)
ppy.wallet.unlock(pwd)

def getUnmatchedBets(bettor_id):
	unmatched_bets = ppy.rpc.get_all_unmatched_bets_for_bettor(bettor_id)
	return unmatched_bets

def getMatchedBets(bettor_id):
	matched_bets = ppy.rpc.get_matched_bets_for_bettor(bettor_id, api="bookie")
	return matched_bets

def getSport(sport_id):
	return Sport(sport_id, peerplays_instance=ppy)

def getSports():
	sports = Sports(peerplays_instance=ppy)
	# TODO Add pagination
	return sports.sports

def getEventGroup(event_group_id):
	return EventGroup(event_group_id, peerplays_instance=ppy)

def getEventGroups(sport_id):
	event_groups = Sport(sport_id, peerplays_instance=ppy)
	# TODO add pagination
	return event_groups.eventgroups

def getEvent(event_id):
	return Event(event_id, peerplays_instance=ppy)

def getEvents(event_group_id):
	events = EventGroup(event_group_id, peerplays_instance=ppy)
	# TODO add pagination
	return events.events

def getBettingMarketGroup(bmg_id):
	return BettingMarketGroup(bmg_id, peerplays_instance=ppy)

def getBettingMarketGroups(event_id):
	bmgs = Event(event_id, peerplays_instance=ppy)
	# TODO add pagination
	return bmgs.bettingmarketgroups

def getBettingMarket(bm_id):
	return BettingMarket(bm_id, peerplays_instance=ppy)

def getBettingMarkets(bmg_id):
	betting_markets = BettingMarketGroup(bmg_id, peerplays_instance=ppy)
	# TODO add pagination
	return betting_markets.bettingmarkets

def getRules(rules_id):
	# TODO add pagination
	return Rule(rules_id, peerplays_instance=ppy)

def getResolutions(bettor_id, bmg_id=None):
	a = Account(bettor_id, peerplays_instance=ppy, full=True)
	history=[]
	for line in a.history(limit=1000): # sufficiently large to get all resolutions
		if line['op'][0] == 64:
			if bmg_id is not None:
				if line['op'][1]['betting_market_group_id'] == bmg_id:
					history.append(line)
			else:
				history.append(line)
	return history

def getHistory(bettor_id, limit=10):
	a = Account(bettor_id, peerplays_instance=ppy, full=True)
	history = []
	for line in a.history(limit=limit):
		history.append(line)
	return history

def getAccountDetails(bettor_id):
	a = Account(bettor_id, peerplays_instance=ppy, full=True)
	return a