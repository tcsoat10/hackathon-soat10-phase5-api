import logging
import smtplib
from src.core.ports.gateways.i_notification_sender_gateway import INotificationSenderGateway
from config.settings import (
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_USE_TLS,
    EMAIL_USE_SSL,
    EMAIL_SENDER_ADDRESS,
)


class NotificationSenderGateway(INotificationSenderGateway):
    def __init__(self):    
        self.logger = logging.getLogger(__name__)
        
        self.email_server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        if EMAIL_USE_TLS:
            self.email_server.starttls()
        elif EMAIL_USE_SSL:
            self.email_server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        
        self.email_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        

    def send_email(self, recipient_email: str, subject: str, body: str):
        '''
        Essa implementação será feita com base no mailtrap usando smtplib
        '''
        try:
            message = f"Subject: {subject}\n\n{body}"
            self.email_server.sendmail(EMAIL_SENDER_ADDRESS, recipient_email, message)
            self.logger.info(f"Email sent to {recipient_email}")
        except Exception as e:
            self.logger.error(f"Failed to send email to {recipient_email}: {e}")
            raise

    def send_sms(self, phone_number: str, message: str):
        raise NotImplementedError("send_sms method is not implemented yet.")
    