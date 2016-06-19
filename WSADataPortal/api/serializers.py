from rest_framework import serializers
from api.models import User, TimeKeeper, Rotowire, RotogrindersBatters, RotogrindersPitchers, SwishAnalyticsBatters

'''
Serializing and deserializing objects into JSON to be sent 
Model Serializer = simple way of creating serializers for objects
'''

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('pk', 'username', 'password')

class RotowireSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rotowire
		fields = ('name', 'bats', 'team', 'position', 'orderInLU', 'opponent', 'opponentThrows', 'salary', 'projPoints',
				  'ceiling', 'floor', 'value', 'moneyLine', 'overUnder')


class TimeKeeperSerializer(serializers.ModelSerializer):
	class Meta:
		model = TimeKeeper
		fields = ('id', 'name', 'scraped')

class RotogrindersBattersSerializer(serializers.ModelSerializer):
	class Meta:
		model = RotogrindersBatters
		fields = ('name', 'position', 'secondaryPosition', 'salary', 'team', 'opponent', 'bats', 'ceiling', 'floor',
				  'projPoints', 'value', 'pitcherName', 'pitcherThrows', 'seasonAB', 'average', 'wOBA', 'ISO', 'OBP',
				  'BABIP', 'SLG', 'kPercentage', 'BB', 'OPS')

class RotogrindersPitchersSerializer(serializers.ModelSerializer):
	class Meta:
		model = RotogrindersPitchers
		fields = ('name', 'position', 'salary', 'team', 'opponent', 'playerThrows', 'ceiling', 'floor', 'projPoints',
				  'value', 'xISO', 'xR', 'xSLG', 'xWOBA', 'xL', 'GP', 'lWOBA', 'rWOBA', 'lSLG',
				  'rSLG', 'SIERA', 'xFIP', 'lISO', 'rISO', 'GBPercentage', 'FBPercentage', 'IP')

class SwishAnalyticsBattersSerializer(serializers.ModelSerializer):
	class Meta:
		model = SwishAnalyticsBatters
		fields = ('name', 'salary', 'bats', 'position', 'team', 'opponent', 'projPoints', 'value', 'outs', 'AB',
				  'BB', 'HBP', 'singles', 'doubles', 'triples', 'HR', 'RBI', 'SB', 'CS', 'averageDKPoints')
