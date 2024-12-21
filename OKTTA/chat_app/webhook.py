import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

from chatGPT_app.models import ChatGPT
from chat_app.models import Chat, Message
from integrations_app.models import Integration
from user_app.models import Manager

logger = logging.getLogger(__name__)


@csrf_exempt
def webhook(request, id_integration):
    """
    Обработчик вебхука
    """
    logger.info('Webhook called')
    if request.method == 'POST':
        update = json.loads(request.body)
        logger.info(f'Received update: {update}')

        if 'message' not in update:
            logger.error('No message found in update')
            return JsonResponse({'status': 'error', 'message': 'No message found'}, status=400)

        chat_id = update['message']['chat']['id']
        nickname = update['message']['from'].get('username', 'Unknown')
        user_id = update['message']['from'].get('id')
        message_text = update['message']['text']

        try:
            integration = Integration.objects.get(id_integration=id_integration)
            user = integration.user
            api_key = integration.api_key
        except Integration.DoesNotExist:
            logger.error(f'Integration not found for token: {id_integration}')
            return JsonResponse({'status': 'error', 'message': 'Integration not found'}, status=404)

        chat, created = Chat.objects.get_or_create(
            integration=integration,
            user=user,
            messanger_chat_id=chat_id,
            defaults={'name': integration.name}
        )
        if created:
            logger.info(f'Chat created: {chat}')
        else:
            logger.info(f'Chat already exists: {chat}')

        try:
            Message.objects.create(
                nickname=nickname,
                chat=chat,
                messages=message_text,
                sender_type=user_id,
            )
            logger.info(f'Message created: {message_text}')

            if message_text == '/start':
                send_message(chat_id, 'Добро пожаловать!', api_key)
                return JsonResponse({'status': 'ok'})

            response_text = respond_to_gpt(message_text, chat)
            if response_text:
                send_message(chat_id, response_text, api_key)

            return JsonResponse({'status': 'ok'})

        except Exception as e:
            logger.error(f'Error processing message: {e}')
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

    elif request.method == 'GET':
        return JsonResponse({'status': 'success', 'message': 'Webhook is active'})

    return JsonResponse({'status': 'error'}, status=400)


def respond_to_gpt(response_text, chat):
    """
    Ответ на GPT
    """
    chatGpt = ChatGPT.objects.first()

    if chatGpt:
        logger.info(f'Response message created: {response_text} by chatGpt: {chatGpt}')
        message = Message.objects.create(
            sender_type='chatGpt',
            chat=chat,
            nickname=chatGpt.name,
            messages=response_text
        )
        logger.info(f'Response message created: {response_text} by chatGpt: {chatGpt}')

        return message.messages

    return None


def send_message(chat_id, text, api_key):
    """
    Отправка сообщения в Telegram
    """
    url = f'{settings.TELEGRAM_URL}{api_key}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)
