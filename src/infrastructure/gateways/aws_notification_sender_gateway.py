
import boto3
import logging
from core.ports.gateways.i_notification_sender_gateway import INotificationSenderGateway
from botocore.exceptions import ClientError
from botocore.config import Config
from config.settings import (
    AWS_DEFAULT_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN,
    BOTO_MAX_ATTEMPTS,
    EMAIL_SENDER_ADDRESS,
)


class AwsNotificationSenderGateway(INotificationSenderGateway):
    def __init__(self):
        config = Config(retries={"max_attempts": BOTO_MAX_ATTEMPTS})
        
        client_kwargs = {"region_name": AWS_DEFAULT_REGION, "config": config}
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            client_kwargs.update({
                "aws_access_key_id": AWS_ACCESS_KEY_ID,
                "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            })
            if AWS_SESSION_TOKEN:
                client_kwargs["aws_session_token"] = AWS_SESSION_TOKEN
        
        self.sns_client = boto3.client("sns", **client_kwargs)
        self.ses_client = boto3.client("ses", **client_kwargs)
        self.logger = logging.getLogger(__name__)

    def send_sms(self, phone_number: str, message: str):
        try:
            response = self.sns_client.publish(
                PhoneNumber=phone_number,
                Message=message
            )
            self.logger.info(f"SMS sent successfully to {phone_number}: {response}")
            return response
        except ClientError as e:
            self.logger.error(f"Error sending SMS to {phone_number}: {e}")
            raise

    def send_email(self, recipient_email: str, subject: str, body: str):
        try:
            response = self.ses_client.send_email(
                Source=EMAIL_SENDER_ADDRESS,
                Destination={"ToAddresses": [recipient_email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": body}},
                },
            )
            self.logger.info(f"Email sent successfully to {recipient_email}: {response}")
            return response
        except ClientError as e:
            self.logger.error(f"Error sending email to {recipient_email}: {e}")
            raise
