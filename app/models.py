import logging

from twilio.base.exceptions import TwilioRestException

from app import db, tc

logger = logging.getLevelName(__name__)

ADMIN_ROLE = 1
USER_ROLE = 0


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    date_created = db.Column(db.DateTime(), default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )


class Service(Base):
    __tablename__ = 'services'

    name = db.Column(db.String(120))
    # FIXME: This should be an enum or limited
    category = db.Column(db.String())
    description = db.Column(db.Text())
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())
    address = db.Column(db.String())
    city = db.Column(db.String())
    state_abbreviation = db.Column(db.String(2))
    postal_code = db.Column(db.SmallInteger())
    operating_hours = db.Column(db.JSON())
    active = db.Column(db.Boolean())

    def __init__(
        self,
        name: str,
        category: str,
        description: str,
        lat: float,
        lng: float,
        address: str,
        city: str,
        state_abbreviation: str,
        postal_code: int,
        operating_hours: dict,
        active: bool = True,
    ):
        self.name = name
        self.category = category
        self.description = description
        self.lat = lat
        self.lng = lng
        self.address = address
        self.city = city
        self.state_abbreviation = state_abbreviation
        self.postal_code = postal_code
        self.operating_hours = operating_hours
        self.active = active


class User(Base):
    __tablename__ = 'users'

    alias = db.Column(db.String(35))
    age = db.Column(db.Integer())
    phone_number = db.Column(db.String(15), unique=True)
    active = db.Column(db.Boolean())
    high_risk = db.Column(db.Boolean())
    question_context = db.Column(db.Integer())
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())
    onboarding_completed = db.Column(db.Boolean)

    saved_state = db.relationship(
        'UserState', back_populates='user', lazy='dynamic'
    )

    messages = db.relationship(
        'Message', back_populates='user', lazy='dynamic'
    )

    def __init__(
        self,
        alias: str,
        age: int,
        phone_number: str,
        lat: float,
        lng: float,
        active: bool = True,
        high_risk: bool = False,
        onboarding_completed: bool = False,
    ):
        self.alias = alias
        self.age = age
        self.phone_number = phone_number
        self.lat = lat
        self.lng = lng
        self.active = active
        self.high_risk = high_risk
        self.onboarding_completed = onboarding_completed

    def template_message(self, message):
        return f'''
        {message.body}\n
        - from: {self.alias}
        '''

    def send_message(self, to_user, body, media_url=None):
        if to_user.active:
            try:
                tc.messages.create(
                    to=to_user.phone_number,
                    from_=self.phone_number,
                    body=body,
                    media_url=media_url,
                )
            except TwilioRestException as e:
                logger.error(e)
                raise
            except Exception as e:
                logger.error(e)
                raise


class UserState(Base):
    __tablename__ = 'user_states'

    last_question = db.Column(db.Integer)
    message_body = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="saved_state")


class Message(Base):
    __tablename__ = 'messages'

    sms_message_sid = db.Column(db.String(160))
    body = db.Column(db.Text)
    sms_status = db.Column(db.String(20))
    to_number = db.Column(db.String(15))
    to_zip = db.Column(db.Integer)
    to_city = db.Column(db.String, nullable=True)
    to_country = db.Column(db.String(5))
    from_number = db.Column(db.String(15))
    from_zip = db.Column(db.Integer)
    from_city = db.Column(db.String, nullable=True)
    from_country = db.Column(db.String(5))
    media_url = db.Column(db.String, nullable=True)
    media_content_type = db.Column(db.String, nullable=True)
    api_version = db.Column(db.String, nullable=True)
    num_segments = db.Column(db.Integer, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="messages")

    def __init__(
        self,
        body,
        sms_message_sid,
        sms_status,
        to_number,
        media_url,
        to_country,
        from_number,
        from_country,
        media_content_type,
        to_city=None,
        to_postal_code=None,
        from_city=None,
        from_postal_code=None,
    ):
        self.body = body
        self.sms_message_sid = sms_message_sid
        self.sms_status = sms_status
        self.to_number = to_number
        self.to_postal_code = self._fill_null_postal_code(to_postal_code)
        self.to_city = to_city
        self.to_country = to_country
        self.from_number = from_number
        self.from_postal_code = self._fill_null_postal_code(from_postal_code)
        self.from_city = from_city
        self.from_country = from_country
        self.media_url = media_url
        self.media_content_type = media_content_type

    @staticmethod
    def _fill_null_postal_code(postal_code):
        if not postal_code:
            return 0
        return postal_code
