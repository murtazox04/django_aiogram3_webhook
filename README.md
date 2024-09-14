# Telegram Bot with Django 5.x and aiogram 3.x

This project demonstrates how to create a Telegram bot using **Django 5.1.1** and **aiogram 3.13.0**, utilizing webhooks for efficient communication.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Setting Up the Webhook](#setting-up-the-webhook)
- [Testing the Bot](#testing-the-bot)
- [Deployment Considerations](#deployment-considerations)
- [Troubleshooting](#troubleshooting)

## Features

- Handles `/start`, `/help`, and `/menu` commands.
- Echoes user messages.
- Utilizes **aiogram 3.13.0**'s routers for organizing handlers.
- Integrates with **Django 5.1.1** web framework.
- Uses webhooks for efficient message handling.

## Prerequisites

- **Python 3.10+** (Required by Django 5.0)
- **Django 5.x**
- **aiogram 3.x** (pre-release)
- **ngrok**
- **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)
- **Git** (for cloning the repository)
- **Virtualenv** or **venv** (recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```
 Note: Replace https://github.com/murtazox04/django_aiogram3_webhook.git with the actual repository URL if applicable.

### 2. Set Up a Virtual Environment
Create and activate a virtual environment to isolate the project dependencies.
```bash
# For Linux/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```


## Configuration

### 1. Create a .env File
Create a .env file in the project's root directory to store environment variables.
```
cp .env.sample .env
```

### 2. Update Django Settings
Ensure your settings.py includes the environment variables:
```python
# mybot/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

INSTALLED_APPS = [
    # ...
    'botapp',
]
```

## Running the Project

### 1. Start ngrok
```bash
ngrok http 8000
```

### 2. Run Database Migrations
```bash
python manage.py migrate
```

### 3. Run the Django Development Server
```bash
python manage.py runserver
```

## Setting Up the Webhook

### 1. Create the `set_webhook` Management Command
Ensure the management command is correctly set up to close the bot session:
```python
# botapp/management/commands/set_webhook.py

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
            self.stdout.write(self.style.SUCCESS(f'Webhook set to {webhook_url}'))
        finally:
            await bot.session.close()
```

### 2. Set the Webhook
Run the following command to set the webhook URL with Telegram:
```bash
python manage.py set_webhook
```
You should see a success message confirming the webhook is set.

## Testing the Bot
Interact with your bot on Telegram:
 - Send `/start` to receive a welcome message.
 - Use `/help` to get assistance.
 - Send any message to see it echoed back.
 - Use `/menu` to see an interactive menu.

### Deployment Considerations
 - <b>HTTPS Requirement</b>: Ensure your webhook URL is accessible over HTTPS with a valid SSL certificate.
 - <b>Persistent Server</b>: For production, deploy your app on a server accessible 24/7.
 - <b>ASGI Server</b>: Use an ASGI server like uvicorn or daphne for asynchronous support.

## Troubleshooting
### Common Issues
#### 1. Bad Webhook: Failed to Resolve Host
 - Cause: The webhook URL is not accessible by Telegram.
 - Solution:
   - Ensure ngrok is running and the URL is correct.
   - Upgrade to a paid ngrok plan to remove the interstitial page.
   - Verify that the webhook URL is correctly set in the .env file.

#### 2. Unclosed Client Session
 - <b>Cause</b>: The aiohttp client session is not properly closed.
 - <b>Solution</b>:
   - Ensure bot.session.close() is called after setting the webhook.
   - Use a try...finally block in your set_webhook.py.

#### 3. Event Loop is Closed
 - <b>Cause</b>: The asyncio event loop is closed prematurely.
 - <b>Solution</b>:
     - Properly await all asynchronous functions.
     - Ensure all tasks are completed before the loop closes.

## Testing Webhook Accessibility
 - Access the webhook URL in a browser: `https://your_ngrok_subdomain.ngrok.io/webhook/`.
 - Use `curl` to test:
   ```bash
   curl -k https://your_ngrok_subdomain.ngrok.io/webhook/
   ```
   A 200 OK response indicates the endpoint is accessible.

## License
This project is licensed under the MIT License.