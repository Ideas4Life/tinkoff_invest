import os
import logging

from aiogram import Bot, Dispatcher, executor, types

from dotenv import load_dotenv

from go import show_condition, print_info_papers

import keyboards as kb

load_dotenv()


B_TOKEN = os.getenv('BOT_TOKEN')
#logging.basicConfig(level=logging.INFO)
bot = Bot(token=B_TOKEN)
dp = Dispatcher(bot)

def auth (func):
    async def wrapper (message):
        if message['from']['id'] != 560451099:  
            return await message.replay("Access Denied", reply=False)
        return await func(message)
    return wrapper


@dp.message_handler(commands=['help'])
@auth
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id,
        "Бот для вывода данных из портфеля ИИС Tinkoff\n\n"
        "Показать текущее состояние портфеля /start\n"
        "Вывести информацию обо всех акция в портфеле /stock\n"
        "Вывести информацию обо всех облигациях в портфеле /bond\n"
        "Вывести информацию обо всех etf в портфеле /etf\n"
        "Вывести информацию обо всех бумагах в портфеле /all\n\n"
        "Для вывода информации об отдельной бумаге введите её тикер",
        reply_markup=kb.greet_kb)


@dp.message_handler(commands=[ 'start'])
@auth
async def start_portfolio(message: types.Message):
    
    condition=show_condition()
    st=""
    for key in condition.keys():
        st+=key+str(condition[key])+"\n"
    #await message.reply(st)
    await bot.send_message(message.from_user.id, st, reply_markup=kb.greet_kb)

@dp.message_handler(commands=['stock', 'bond', 'etf', 'all'])
@auth
async def start_portfolio(message: types.Message):
    condition=print_info_papers(message.text[1:].capitalize())
    st=""
    for key in condition.keys():
        st+=str(key).ljust(20," ") +\
            str(condition[key][0]).ljust(30," ") +\
            str(condition[key][1]).ljust(20," ") +\
            str(condition[key][2]).ljust(20," ") +\
            str(condition[key][3]) + "\n"
    await bot.send_message(message.from_user.id,
        "\nТикер".ljust(10) +\
        "Ср. цена бумаги".ljust(18) +
        "Кол-во бумаг".ljust(15) +
        "Прибыль".ljust(11) + 
        "Стоимость".ljust(8) +
        "\n"+ 
        st,
        reply_markup=kb.greet_kb
    )

@dp.message_handler()
@auth
async def start_portfolio(message: types.Message):
    condition=print_info_papers(message.text.upper())
    if len(condition)==0:
        await message.reply("Неккоректный тикер, попробуйте другую команду")
    else:
        st=""
        for key in condition.keys():
            st+=str(key).ljust(20," ") +\
                str(condition[key][0]).ljust(30," ") +\
                str(condition[key][1]).ljust(20," ") +\
                str(condition[key][2]).ljust(20," ") +\
                str(condition[key][3]) + "\n"
        await bot.send_message(message.from_user.id,
            "\nТикер".ljust(10) +\
            "Ср. цена бумаги".ljust(18) +
            "Кол-во бумаг".ljust(15) +
            "Прибыль".ljust(11) + 
            "Стоимость".ljust(8) +
            "\n"+ 
            st,
            reply_markup=kb.greet_kb
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)