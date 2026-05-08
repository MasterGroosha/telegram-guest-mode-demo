import asyncio
import random
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineQueryResultArticle, InputTextMessageContent

dp = Dispatcher()

RESPONSES = {
    "ru": [
        "Не знаю.",
        "Не уверен.",
        "Может быть.",
        "Трудно сказать.",
        "Возможно.",
    ],
    "en": [
        "I don't know.",
        "I'm not sure.",
        "Maybe.",
        "It's hard to say.",
        "Possibly.",
    ],
}


def detect_message_language(text: str) -> str:
    """
    Определяет язык сообщения, сравнивая количество кириллицы и латиницы.
    :param text: исходный текст
    :return: ru или en
    """
    filtered_text = " ".join(
        word for word in text.split() if not word.startswith("@")
    ).lower()
    cyrillic_count = sum("а" <= char <= "я" or char == "ё" for char in filtered_text)
    latin_count = sum("a" <= char <= "z" for char in filtered_text)
    return "ru" if cyrillic_count > latin_count else "en"


def get_message_text(message: Message | None) -> str | None:
    if message is None:
        return None
    return message.text or message.caption



@dp.guest_message(F.text)
async def any_message(
        message: Message,
):
    text = message.text or ""
    language = detect_message_language(text)
    response_text = random.choice(RESPONSES.get(language, RESPONSES["en"]))
    await message.answer_guest_query(
        result=InlineQueryResultArticle(
            id="1",
            title="Guest mode",
            input_message_content=InputTextMessageContent(message_text=response_text),
        )
    )

async def main():
    bot_token = getenv("BOT_TOKEN")
    if not bot_token:
        error = "No token provided"
        raise ValueError(error)

    bot = Bot(token=bot_token)
    print("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        print("Bot stopped")


if __name__ == '__main__':
    asyncio.run(main())
