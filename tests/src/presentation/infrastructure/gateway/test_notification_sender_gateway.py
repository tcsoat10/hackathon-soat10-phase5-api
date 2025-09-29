import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.infrastructure.gateways.notification_sender_gateway import NotificationSenderGateway
from email import message_from_string


@pytest.fixture
def gateway():
    return NotificationSenderGateway()


def test_send_sms_not_implemented(gateway):
    with pytest.raises(NotImplementedError, match="send_sms method is not implemented yet."):
        gateway.send_sms("+5511999999999", "Olá!")


@patch("builtins.open", new_callable=mock_open, read_data="<html>Olá {{nome_usuario}}, {{mensagem_dinamica}}</html>")
@patch.object(NotificationSenderGateway, "_create_connection")
def test_send_email_success(mock_connection, mock_file, gateway):
    mock_server = MagicMock()
    mock_connection.return_value.__enter__.return_value = mock_server

    # Simula configurações
    from config import settings
    settings.EMAIL_USE_SSL = True
    settings.EMAIL_USE_TLS = False

    data = {
        "nome_usuario": "Maria",
        "mensagem_dinamica": "Seu vídeo está pronto!"
    }

    gateway.send_email("maria@example.com", "Notificação", data)

    mock_file.assert_called_once_with(
        'src/application/templates/email_ready_notification.html', 'r', encoding='utf-8'
    )
    mock_server.sendmail.assert_called_once()
    raw_message = mock_server.sendmail.call_args[0][2]
    email_msg = message_from_string(raw_message)

    # Extrai partes do e-mail
    parts = {part.get_content_type(): part.get_payload(decode=True).decode('utf-8')
         for part in email_msg.walk() if part.get_content_type() in ['text/plain', 'text/html']}

    assert "Maria" in parts['text/plain']
    assert "Seu vídeo está pronto!" in parts['text/plain']

#    assert "Maria" in mock_server.sendmail.call_args[0][2]
#    assert "Seu vídeo está pronto!" in mock_server.sendmail.call_args[0][2]


@patch("builtins.open", new_callable=mock_open, read_data="<html>Olá {{nome_usuario}}, {{mensagem_dinamica}}</html>")
@patch("smtplib.SMTP")
def test_send_email_with_tls(mock_smtp, mock_file, gateway):
    mock_server = MagicMock()
    mock_smtp.return_value = mock_server

    from config import settings
    settings.EMAIL_USE_SSL = False
    settings.EMAIL_USE_TLS = True

    data = {
        "nome_usuario": "João",
        "mensagem_dinamica": "Seu vídeo está pronto!"
    }

    gateway.send_email("joao@example.com", "Notificação", data)

    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()


@patch("builtins.open", side_effect=FileNotFoundError("template not found"))
def test_send_email_template_not_found(mock_file, gateway):
    from config import settings
    settings.EMAIL_USE_SSL = True

    data = {
        "nome_usuario": "Ana",
        "mensagem_dinamica": "Seu vídeo está pronto!"
    }

    with pytest.raises(FileNotFoundError, match="template not found"):
        gateway.send_email("ana@example.com", "Notificação", data)