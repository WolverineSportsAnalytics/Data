from rest_framework import serializers
from api.models import User, TimeKeeper, Rotowire

'''
Serializing and deserializing objects into JSON to be sent 
Model Serializer = simple way of creating serializers for objects
'''

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('pk', 'username', 'password')
'''
	pk = serializers.IntegerField(read_only=True)
	username = serializers.CharField(required=True, max_length=50)
	password = serializers.CharField(required=True, max_length=20)

	def create(self, validated_data): 
		return User.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.username = validated_data.get('username', instance.username)
		instance.password = validated_data.get('password', instance.password)
		instance.save()
		return instance
'''

class RotowireSerializer(serializers.ModelSerializer):

	class Meta:
		model = Rotowire
		fields = ('name', 'bats', 'team', 'position', 'orderInLU', 'opponent', 'opponentThrows', 'salary', 'projPoints',
				  'ceiling', 'floor', 'value', 'moneyLine', 'overUnder')


class TimeKeeperSerializer(serializers.ModelSerializer):
	class Meta:
		model = TimeKeeper
		fields = ('id', 'name', 'scraped')

