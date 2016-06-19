from rest_framework import serializers
from api.models import User, TimeKeeper, Rotowire, RotogrindersBatters

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