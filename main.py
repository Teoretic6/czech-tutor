import os

from dotenv import load_dotenv
import openai
import telebot


if __name__ == '__main__':
    load_dotenv()

    TELEGRAM_BOT_KEY = os.getenv('TELEGRAM_BOT_KEY')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

    bot = telebot.TeleBot(TELEGRAM_BOT_KEY)

    client = openai.OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "I want to generate a Czech Language lesson. "
                           "Lesson should include 10 new words (nouns). "
                           "For every word there must be 1 simple sentence of using them."
                           "Answer only with the lesson",
            }
        ],
        model="gpt-3.5-turbo",
        n=1,
        temperature=0.5
    )

    lesson = chat_completion.choices[0].message.content

    bot.send_message(TELEGRAM_CHAT_ID,
                     lesson)

    # This is how I got chat_id:
    # https://stackoverflow.com/questions/75116947/how-to-send-messages-to-telegram-using-python
    # import requests
    # url = f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY}/getUpdates"
    # print(requests.get(url).json())
