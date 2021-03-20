# tinkoff_invest
Обработка данных из инвестиционного портфеля в tinkoff

Для работы скрипта нужно прописать три переменных окружения в файле .env, который следует добавить в .gitignore:

TINKOFF_TOKEN=some_tinkoff_token
TINKOFF_BROKER_ACCOUNT=some_broker_account
TINKOFF_ACCOUNT_STARTED=01.06.2020

Здесь:
TINKOFF_TOKEN это токен Тиньков инвестиций, который можно получить в личном кабинете tinkoff инвестиций;
TINKOFF_BROKER_ACCOUNT - это ID портфеля в Тинькофе (его можно получить с помощью tinvest.SyncClient(TOKEN).get_accounts().payload.accounts[num].broker_account_id, где num - номер портфеля (0 или 1), если имеется ещё ИИС); 
TINKOFF_ACCOUNT_STARTED это дата открытия портфеля в формате дд.мм.гггг, от этой даты будут считаться пополнения.

Использование: python go.py
