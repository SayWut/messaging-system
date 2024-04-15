from rest_framework import serializers
from collections import OrderedDict

from .models import MessageModel

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer class for representing MessageModel objects.
    """
    
    class Meta:
        model = MessageModel
        fields = ['sender', 'receiver', 'subject', 'message', 'creation_date']

class UserGetMessagesQuerySerializer(serializers.Serializer):
    unread = serializers.BooleanField(required=False, allow_null=True, default=None)

    def to_representation(self, instance):
        """
        Overrides the default `to_representation` method to filter out `None` values.

        This ensures that only non-null values are included in the response,
        providing a cleaner representation for the API consumer.
        """

        result = super(UserGetMessagesQuerySerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
    
class UserDeleteMessageQuerySerializer(serializers.Serializer):
    sender = serializers.CharField(required=False, allow_null=True, default=None)
    receiver = serializers.CharField(required=False, allow_null=True, default=None)

    def validate(self, attrs):
        """
        Validates the serializer data (query parameters).

        Checks if both `sender` and `receiver` are empty (None).
        If both are empty, raises a validation error indicating that one of them is required for message deletion.
        """

        if not attrs['sender'] and not attrs['receiver']:
            raise serializers.ValidationError({
                "sender": "One of the following fields must be passed: receiver, sender.",
                "receiver": "One of the following fields must be passed: receiver, sender."
            })

        return attrs
    
    def to_representation(self, instance):
        """
        Overrides the default `to_representation` method to filter out `None` values.

        This ensures that only non-null values are included in the response,
        providing a cleaner representation for the API consumer.
        """
                
        result = super(UserDeleteMessageQuerySerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])