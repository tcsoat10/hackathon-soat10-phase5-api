"""
Essa classe abstrata fornece métodos de envio de mensagem SMS e E-mail.
A classe que implementa-la poderá definir como o envio será feito.
Para este projeto a classe que implementará esses métodos utilizará recursos da AWS (SNS e SES).
"""
from abc import ABC, abstractmethod


class INotificationSenderGateway(ABC):
    @abstractmethod
    def send_sms(self, phone_number: str, message: str):
        """
        Envia uma mensagem SMS para o número de telefone especificado.
        """
        pass

    @abstractmethod
    def send_email(self, recipient_email: str, subject: str, body: str):
        """
        Envia um e-mail para o endereço de e-mail especificado.
        """
        pass

__all__ = ["INotificationSenderGateway"]
