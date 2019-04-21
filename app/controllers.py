import logging
from datetime import datetime

from flask import Response
from flask_restful import Resource

from app import db
from app.adapters import MessageRequest
from app.models import Message, User, UserState
from app.templates.failure import failure_message
from app.templates import service_onboarding

# from twilio.twiml import Response as TwiMLResponse


logger = logging.getLogger(__name__)


class HealthCheck(Resource):
    """
    Just a test to show API is running
    """

    def get(self):
        return True


class BaseMessage(Resource, MessageRequest):
    """
    docstring for BaseMessage
    """

    @staticmethod
    def parse_message(parsed_request):
        # Phone number format validation
        message = Message(
            sms_message_sid=parsed_request.sms_message_sid,
            body=parsed_request.body,
            sms_status=parsed_request.sms_status,
            to_number=parsed_request.to_number,
            to_postal_code=parsed_request.to_postal_code,
            to_city=parsed_request.to_city,
            to_country=parsed_request.to_country,
            from_number=parsed_request.from_number,
            from_postal_code=parsed_request.from_postal_code,
            from_city=parsed_request.from_city,
            from_country=parsed_request.from_country,
            media_url=parsed_request.media_url,
            media_content_type=parsed_request.media_content_type,
        )

        # Find or create user
        user = (
            db.session.query(User)
            .filter_by(phone_number=parsed_request.from_number)
            .filter_by(active=True)
            .first()
        ) or (
            User(
                alias=None,
                age=None,
                phone_number=message.from_number,
                lat=None,
                lng=None,
            )
        )
        user.messages.append(message)

        return user, message


class InboundMessage(BaseMessage):
    """
    docstring for InboundMessage
    """

    def post(self):
        try:
            user, message = self.parse_message(self.request())
            # FIXME: Need to add the sending logic here

            if not user.onboarding_completed:
                onboarding_steps = [
                    'welcome_1',
                    'welcome_2',
                    'welcome_3',
                    'welcome_4',
                    'welcome_5'
                ]

                saved_state = user.saved_state[:-1] or UserState()
                if saved_state.last_question is None:
                    saved_state.last_question = 0
                    current_question = 0
                else:
                    current_question = saved_state.last_question + 1

                # FIXE: Need to put the tree choice here
                saved_state.next_question = current_question + 1

                user.saved_state.append(saved_state)

                response = (
                    getattr(
                        service_onboarding,
                        onboarding_steps[0]
                    )(**user.__dict__)
                )
            else:
                response = 'foo'
                logger.info(
                    f'''
                    Message {message.sms_message_sid}
                    sent at {str(datetime.now())}
                    '''
                )

            db.session.add(user)
            db.session.add(message)
            db.session.commit()

            return Response(
                    response, status=200, mimetype='text/plain; charset=utf-8'
                )
        except Exception as e:
            logger.error(e)
            return Response(
                'Server Error, Please try again later, {0}'.format(e),
                status=500,
                mimetype='text/plain; charset=utf-8',
            )

        return Response(status=204, mimetype='text/plain; charset=utf-8')


class OutboundMessage(BaseMessage):
    """
    docstring for OutboundMessage
    """

    # FIXME
    pass


class FailedMessage(BaseMessage):
    """
    There was a message failure in InboundMessage and the API returned a 5XX
    """

    def get(self):
        return Response(
            failure_message(), status=200, mimetype='text/plain; charset=utf-8'
        )
