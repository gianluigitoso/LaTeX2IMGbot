#!/usr/bin/env python3
"""
d
"""
from threading import current_thread
from LaTeX2IMG.LaTeX2IMG import latex2img
import telebot
from telebot import logging
from telebot import types
from time import gmtime, strftime


TOKEN = ''

with open("token.txt", "r") as file:
    TOKEN = file.readline().strip()

bot = telebot.TeleBot(TOKEN)

def send_equation(chat_id, text):
    bot.send_chat_action(chat_id, 'upload_document')

    filename = 'resultado' + current_thread().name

    latex2img(text, filename, 'webp')

    with open(filename + '.webp', 'rb') as equation:
        bot.send_sticker(chat_id, equation)

def print_in_terminal(message):
    if message.from_user.id == None:
        message.from_user.id = ' '
    if message.from_user.username == None:
        message.from_user.username = ' '
    if message.from_user.first_name == None:
        message.from_user.first_name = ' '
    if message.from_user.last_name == None:
        message.from_user.last_name = ' '
    if message.text == None:
        message.text = ' '
    print ("[" + strftime("%d-%m-%Y | %H:%M:%S", gmtime()) + "]" +
    " - (ID: " + str(message.from_user.id) + " | @" + message.from_user.username + ") > " +
    message.from_user.first_name + " " + message.from_user.last_name + ": " +
    message.text)

#Message handlers

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print_in_terminal(message)
    bot.reply_to(message, "You can convert LaTeX expression using\n\n/latex expression")

@bot.message_handler(commands=['latex'])
def send_expression(message):
    print_in_terminal(message)
    chat_id = message.chat.id
    text = message.text[7:]

    if text and text != "LaTeX2IMGbot":
        send_equation(chat_id, text)
    else:
        new_msg = bot.reply_to(message, "Please send your expression with \"/latex expression\"")

#If invalid commands
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print_in_terminal(message)
    bot.reply_to(message, "Invalid input. Please send your expression with \"/latex expression\"")

logger = telebot.logger
formatter = logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                                  '%m-%d %H:%M:%S')
ch = logging.FileHandler("log.txt")
logger.addHandler(ch)
logger.setLevel(logging.INFO)  # or use logging.INFO
ch.setFormatter(formatter)

bot.polling()
