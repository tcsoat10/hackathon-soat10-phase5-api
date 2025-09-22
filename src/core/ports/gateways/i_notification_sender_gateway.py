from abc import ABC, abstractmethod


class INotificationSenderGateway(ABC):
    @abstractmethod
    def send_sms(self, phone_number: str, message: str):
        """
        Envia uma mensagem SMS para o número de telefone especificado.
        """
        pass

    @abstractmethod
    def send_email(self, recipient_email: str, subject: str, data: dict):
        """
        Envia um e-mail para o endereço de e-mail especificado.
        """
        pass

__all__ = ["INotificationSenderGateway"]
