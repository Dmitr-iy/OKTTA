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

            response_user = respond_to_user(chat, user)
            if response_user:
                send_message(chat_id, response_user, api_key)

            response_manager = respond_to_manager(chat, user)
            if response_manager:
                send_message(chat_id, response_manager, api_key)

            return JsonResponse({'status': 'ok'})

        except Exception as e:
            logger.error(f'Error processing message: {e}')
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

    elif request.method == 'GET':
        return JsonResponse({'status': 'success', 'message': 'Webhook is active'})

    return JsonResponse({'status': 'error'}, status=400)


def respond_to_gpt(response_text, chat):
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


def respond_to_user(chat, user):
    if user:
        response_text = f'Я ваш админ: {user.first_name} {user.last_name}'

        Message.objects.create(
            nickname=user.email,
            chat=chat,
            sender_type=user.email,
            messages=response_text
        )
        logger.info(f'Response message created: {response_text} by user: {user.email}')

        return response_text

    return None


def respond_to_manager(chat, user):
    if not user:
        logger.warning('No user found to respond to manager.')
        return

    manager = Manager.objects.filter(user=user).first()

    if not manager:
        logger.warning('No manager found for user.')
        return

    if manager:
        message_text = f'Я ваш менеджер: {manager.email}'

        Message.objects.create(
            nickname=manager.email,
            chat=chat,
            sender_type=manager.email,
            messages=message_text
        )
        logger.info(f'Response message created: {message_text} by manager: {manager.email}')

        return message_text

    return None

def send_message(chat_id, text, api_key):
    url = f'{settings.TELEGRAM_URL}{api_key}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)
