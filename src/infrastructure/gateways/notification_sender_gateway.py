import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
    
    def send_sms(self, phone_number: str, message: str):
        raise NotImplementedError("send_sms method is not implemented yet.")
    
    def send_email(self, recipient_email: str, subject: str, data: dict):
        try:
            with open('src/application/templates/email_ready_notification.html', 'r', encoding='utf-8') as f:
                html_template = f.read()

            html_body = html_template
            for key, value in data.items():
                html_body = html_body.replace(f'{{{{{key}}}}}', str(value))

            plain_text_body = f"Olá, {data.get('nome_usuario', 'Usuário')}!\n\n" \
                f"{data.get('mensagem_dinamica', '')}\n\n" \
                f"Equipe do Projeto SOAT10"
            
            message = MIMEMultipart('alternative')
            message['From'] = EMAIL_SENDER_ADDRESS
            message['To'] = recipient_email
            message['Subject'] = subject
            
            part1 = MIMEText(plain_text_body, 'plain', 'utf-8')
            part2 = MIMEText(html_body, 'html', 'utf-8')
            
            message.attach(part1)
            message.attach(part2)
            
            # self.email_server.sendmail(EMAIL_SENDER_ADDRESS, [recipient_email], message.as_string())
            with self._create_connection() as server:
                server.sendmail(EMAIL_SENDER_ADDRESS, [recipient_email], message.as_string())

            self.logger.info(f"Email sent to {recipient_email}")
        except Exception as e:
            self.logger.error(f"Failed to send email to {recipient_email}: {e}")
            raise

    def _create_connection(self):
        email_server = None
        if EMAIL_USE_SSL:
            email_server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        else:
            email_server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            if EMAIL_USE_TLS:
                email_server.starttls()

        email_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        
        return email_server


__all__ = ["NotificationSenderGateway"]
