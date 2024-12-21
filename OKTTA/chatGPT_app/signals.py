from django.db.models.signals import post_save
from django.dispatch import receiver

from chatGPT_app.models import ChatGPT


@receiver(post_save, sender=ChatGPT)
def spending_tokens(sender, instance, created, **kwargs):
    """
    Оплата токенов при создании интеграции. Вычитание токенов из баланса. 1 токен = 2 символам текста
    """
    if created:
        user_tokens = instance.user.tokens_purchased
        text_length = len(instance.text)
        tokens_purchase = user_tokens - (text_length / 2)
        instance.user.tokens_purchased = tokens_purchase
        instance.user.save()
        print(f"Tokens purchased: {tokens_purchase}")
