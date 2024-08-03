import os
import random
import pandas as pd
from dotenv import load_dotenv
import openai
import telebot


def load_words(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    return df


def select_random_words(df, n_total=10, ratio=0.5):
    """
    Selects random words from the DataFrame.

    :param df: DataFrame containing words and their frequency
    :param n_total: Total number of words to select
    :param ratio: Ratio of frequent words to less frequent words
    :return: List of selected words
    """
    # Calculate the number of words to select from each category
    n_frequent = int(n_total * ratio)
    n_less_frequent = n_total - n_frequent

    # Sort the DataFrame by frequency
    df_sorted = df.sort_values(by='count', ascending=False)

    # Select words
    top_words = df_sorted.head(int(len(df) / 2))['word']
    bottom_words = df_sorted.tail(int(len(df) / 2))['word']

    random_top_words = top_words.sample(n=n_frequent).tolist()
    random_bottom_words = bottom_words.sample(n=n_less_frequent).tolist()

    return random_top_words + random_bottom_words


if __name__ == '__main__':
    load_dotenv()

    TELEGRAM_BOT_KEY = os.getenv('TELEGRAM_BOT_KEY')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

    # Load the words from the CSV file
    words_df = load_words('./top_czech_words.csv')
    selected_words = select_random_words(words_df)

    # Construct the prompt with the selected words
    prompt = (
        "I want to generate a Czech Language lesson. "
        f"Include the following words in the lesson: {', '.join(selected_words)}. "
        "For every word, there must be 1 simple sentence using it. "
        "Answer only with the lesson."
        
        "Example of a lesson is:"
        "1. Czech word (Translation): Sentence. (Translation to English)"
        "2. Czech word (Translation): Sentence. (Translation to English)"
        "etc."
    )

    bot = telebot.TeleBot(TELEGRAM_BOT_KEY)

    client = openai.OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="anthropic/claude-3-haiku",
        n=1,
        temperature=0.5
    )

    lesson = chat_completion.choices[0].message.content

    bot.send_message(TELEGRAM_CHAT_ID, lesson)