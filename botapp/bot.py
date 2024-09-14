from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer("Hello! I'm your bot built with aiogram 3.x and Django 5.0.")


@router.message()
async def echo(message: Message):
    await message.answer(f"You said: {message.text}")
