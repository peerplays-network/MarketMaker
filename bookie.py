import json
from getpass import getpass
from peerplays import PeerPlays
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

def getSports():
	sports = Sports(peerplays_instance=ppy)
	# TODO Add pagination 
	return sports.sports

def getEventGroups(sport_id):
	event_groups = Sport(sport_id, peerplays_instance=ppy)
	# TODO add pagination
	return event_groups.eventgroups

def getEvents(event_group_id):
	events = EventGroup(event_group_id, peerplays_instance=ppy)
	# TODO add pagination
	return events.events

def getBettingMarketGroups(event_id):
	bmgs = Event(event_id, peerplays_instance=ppy)
	# TODO add pagination
	return bmgs.bettingmarketgroups

def getBettingMarkets(bmg_id):
	betting_markets = BettingMarketGroup(bmg_id, peerplays_instance=ppy)
	# TODO add pagination
	return betting_markets.bettingmarkets

def getRules(rules_id):
	rules = Rule(rules_id, peerplays_instance=ppy)
	# TODO add pagination
	return rules