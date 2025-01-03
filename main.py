import telebot
from telebot import types
import logging
from datetime import datetime
import csv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "Токен телеграмм бота"
SECRET_USER = ['Фамилия специального пользователя']
black_list = set()
prise = "Сообщение с призом"

bot = telebot.TeleBot(TOKEN)


class UserSurvey:
    def __init__(self, user_id, user_last_name):
        self.user_id = user_id
        self.user_last_name = user_last_name
        self.questions = [
            "1) Вопрос номер 1",
            "2) Вопрос номер 2",
            "3) И т.д."
        ]
        self.answers = {}
        self.question_number = 1

    def next_question(self):
        if self.question_number <= len(self.questions):
            return self.questions[self.question_number - 1]
        else:
            return None

    def process_answer(self, answer):
        self.answers[self.question_number] = answer
        self.question_number += 1

    def is_finished(self):
        return self.question_number > len(self.questions)

    def save_answers(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['question_number', 'answer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for question_num, answer in self.answers.items():
                writer.writerow({'question_number': question_num, 'answer': answer})

    def load_answers(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self.answers = {}
                for row in reader:
                    self.answers[int(row['question_number'])] = row['answer']
        except FileNotFoundError:
            pass


user_surveys = {}  # Словарь для хранения состояния анкет для каждого пользователя


@bot.message_handler(commands=['start'])
def start(message):
    try:
        user_last_name = message.from_user.last_name
        if user_last_name not in black_list:
            logging.info(f"Сообщение 'start' отправлено пользователю {user_last_name}")
            if user_last_name in SECRET_USER:
                start_message = """
                            Приветственное сообщение, для специального пользователя
                            """
                markup_anket = types.InlineKeyboardMarkup()
                markup_anket.add((types.InlineKeyboardButton('Анкета', callback_data='question')))
                bot.send_message(message.chat.id, start_message, reply_markup=markup_anket)
            else:
                black_list.add(user_last_name)
                start_message = """
                Приветственное сообщение для не специального пользователя
                
                    """
                markup_exit = types.InlineKeyboardMarkup()
                markup_exit.add((types.InlineKeyboardButton('Выход', callback_data='exit')))
                bot.send_message(message.chat.id, start_message, reply_markup=markup_exit)
    except Exception as e:
        logging.error(f"Ошибка в обработчике start: {e}")


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    try:
        user_id = callback.from_user.id
        user_last_name = callback.from_user.last_name
        if callback.data == 'question':
            if user_id not in user_surveys:
                user_surveys[user_id] = UserSurvey(user_id, user_last_name)
            survey = user_surveys[user_id]
            next_q = survey.next_question()
            if next_q:
                bot.send_message(callback.message.chat.id, next_q)
                bot.register_next_step_handler(callback.message, process_user_answer, user_id, user_last_name)
            else:
                bot.send_message(callback.message.chat.id, "Анкета закончена!")
        elif callback.data == 'exit':
            bot.send_message(callback.message.chat.id, "Если не специальный пользователь, то больше взаимодействовать с ботом не сможет")
            logging.info(
                f"Логируем что -> {user_last_name} не специальный пользователь попытался пройти анкету")
    except Exception as e:
        logging.error(f"Ошибка в обработчике callback_query: {e}")


def process_user_answer(message, user_id, user_last_name):
    try:
        survey = user_surveys[user_id]
        survey.process_answer(message.text)
        if not survey.is_finished():
            next_q = survey.next_question()
            bot.send_message(message.chat.id, next_q)
            bot.register_next_step_handler(message, process_user_answer, user_id, user_last_name)
        else:
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M")
            filename = f"user_{user_last_name}_{timestamp}_answers.csv"
            survey.save_answers(filename)
            bot.send_message(message.chat.id, f"""
             {prise} Сообщение после прохождения ответов
            """)

            logging.info(
                f"Пользователь {user_last_name} Прошел анкету")
            # Обработка результатов survey.answers
    except Exception as e:
        logging.error(f"Ошибка в обработчике ответа: {e}")


@bot.message_handler(commands=['help'])
def help_tg(message):
    try:
        logging.info(f"Сообщение 'help' отправлено пользователю {message.from_user.last_name}")
        bot.send_message(message.chat.id, message)
    except Exception as e:
        logging.error(f"Ошибка в обработчике help: {e}")


bot.polling(none_stop=True)


