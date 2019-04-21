from app import api
from app.controllers import HealthCheck, InboundMessage, FailedMessage

api.add_resource(HealthCheck, '/')
api.add_resource(InboundMessage, '/inbound')
api.add_resource(FailedMessage, '/failed_message')
