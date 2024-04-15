from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MessageModel
from .serializers import MessageSerializer, UserGetMessagesQuerySerializer, UserDeleteMessageQuerySerializer
from django.db.models import Q

class UserMessagesView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # Example permission class

    def get(self, request):
        """
        Retrieves all messages belonging to the currently logged-in user.

        **Request:**

        - Method: GET
        - Authentication: Required (user must be logged in)
        - Optional Query Parameter:
            - unread (boolean):
                - True: Returns only unread messages for the logged-in user.
                - False: Returns only read messages for the logged-in user.
                - not provided: Returns all messages for the logged-in user

        **Response:**

        - Status Code:
            - 200 OK: Upon successful retrieval of messages.
            - 400 Bad Request: If missing required fields or invalid data types.
            - 404 Not Found: If no messages are found for the logged-in user (considering the applied filter, if any).
        - Content:
            - A JSON list representing the retrieved messages
        """

        query_serializer = UserGetMessagesQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        # fetching only the logged-in user messages if unread 
        if 'unread' in query_serializer.data:   
            user_messages = MessageModel.objects.filter(receiver=request.user, **query_serializer.data)
        else:
            user_messages = MessageModel.objects.filter(Q(receiver=request.user) | Q(sender=request.user), **query_serializer.data)

        if not user_messages:
            return Response(status=404)
        
        message_serializer = MessageSerializer(user_messages, many=True)
        return Response(message_serializer.data)
        
class UserMessageView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # Example permission class

    def get(self, request):
        """
        Retrieves and marks as read the first unread message for the currently logged-in user.

        **Request:**

        - Method: GET
        - Authentication: Required (user must be logged in)

        **Response:**

        - Status Code:
            - 200 OK: Upon successful retrieval and marking of the message as read.
            - 404 Not Found: If no unread messages are found for the logged-in user.
        - Content:
            - A JSON list representing the retrieved messages
        """

        try:
            user_messages = request.user.receiver.filter(unread=True)[0]
            user_messages.unread = False
            user_messages.save()

            message_serializer = MessageSerializer(user_messages)
            return Response(message_serializer.data)
        except (IndexError):
            return Response(status=404)

    def post(self, request):
        """
        Creates and sends a new message.

        **Request:**

        - Method: POST
        - Authentication: Required (user must be logged in)
        - Request Body (JSON):
            - Required:
                - receiver (string): Username of the recipient user.
                - subject (string): Subject of the message.
                - message (string): Content of the message.

        **Response:**

        - Status Code:
            - 201 Created: Upon successful message creation.
            - 400 Bad Request: If missing required fields or invalid data types.
        -Content:
            - No content is included in the response body.
        """


        request_body = request.data.dict() if request.data else {}
        request_body['sender'] = request.user.username

        message_serializer = MessageSerializer(data=request_body)
        message_serializer.is_valid(raise_exception=True)
        message_serializer.save()

        return Response(status=201)        
    
    def delete(self, request):
        """
        Deletes a message for the logged-in user.

        **Request:**

        - Method: DELETE
        - Authentication: Required (user must be logged in)
        - Required Query Parameter (one of the following):
            - sender (string): Username of the message sender (searches for messages sent by the provided sender to the logged-in user).
            - receiver (string): Username of the message recipient (searches for messages sent by the logged-in user to the provided recipient).

        **Response:**

        - Status Code:
            - 204 No Content: Upon successful message deletion.
            - 400 Bad Request: If missing required fields or invalid data types.
            - 404 Not Found: If no message is found matching the criteria (sender or receiver) and the logged-in user.
        - Content:
            - No content is included in the response body upon success (204).

        **Additional Notes:**

        - Only one of the `sender` or `receiver` parameters should be provided in the request (though both can be present, the search prioritizes `sender`).
        - The function deletes only the first matching message (if multiple messages are found).
        """
        
        query_serializer = UserDeleteMessageQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        
        if 'sender' in query_serializer.data:
            user_messages = request.user.receiver.filter(sender=query_serializer.data['sender'])
        elif 'receiver' in query_serializer.data:
            user_messages = request.user.sender.filter(receiver=query_serializer.data['receiver'])

        if user_messages:
            delete_message = user_messages[0]
            delete_message.delete()

            message_serializer = MessageSerializer(delete_message)
            return Response(message_serializer.data)

        return Response(status=404)
    