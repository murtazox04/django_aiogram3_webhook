import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from aiogram import Bot


class Command(BaseCommand):
    help = 'Set the Telegram bot webhook'

    def handle(self, *args, **options):
        webhook_url = settings.WEBHOOK_URL
        asyncio.run(self.set_webhook(webhook_url))

    async def set_webhook(self, webhook_url):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        try:
            print(f"Setting webhook to: {webhook_url}")
            await bot.set_webhook(webhook_url)
            self.stdout.write(self.style.SUCCESS(
                f'Webhook set to {webhook_url}'))
        finally:
            await bot.session.close()
