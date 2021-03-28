from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnStock = KeyboardButton("/stock")
btnBond = KeyboardButton("/bond")
btnEtf = KeyboardButton("/etf")
btnAll = KeyboardButton("/all")
btnStart = KeyboardButton("/start")
btnHelp = KeyboardButton("/help")

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
    .row(btnStock, btnBond, btnEtf)\
    .add(btnAll, btnHelp, btnStart)
