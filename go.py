import os
import tinvest
import locale

from decimal import Decimal
from datetime import datetime

from dotenv import load_dotenv
from tinkoffapi import TinkoffApi

load_dotenv()

TOKEN = os.getenv('TINVEST_TOKEN')
BROKER_ACCOUNT_ID = os.getenv('BROKER_ACCOUNT_ID')
BROKER_ACCOUNT_STARTED_AT = datetime(2020, 8, 18, 0, 0, 0)

api=TinkoffApi(api_token=TOKEN, broker_account_id=BROKER_ACCOUNT_ID)
usd_course = api.get_usd_course()


def get_portfolio_sum() -> Decimal:
    """Возвращает текущую стоимость портфеля в рублях без учета свободных денег"""

    # получить характиристики портфеля (включая id)
    #account = tinvest.SyncClient(TOKEN).get_accounts().payload.accounts[0].broker_account_id

    positions = api.get_portfolio_positions()

    portfolio_sum = Decimal('0')
    for position in positions:
        current_ticker_cost = (Decimal(str(position.balance))
                               * Decimal(str(position.average_position_price.value))
                               + Decimal(str(position.expected_yield.value)))
        if position.average_position_price.currency.name == "usd":
            current_ticker_cost *= usd_course
        portfolio_sum += current_ticker_cost
    return portfolio_sum


def get_sum_pay_in() -> Decimal:
    """Возвращает сумму всех пополнений в рублях"""

    operations = api.get_all_operations(BROKER_ACCOUNT_STARTED_AT)

    sum_pay_in = Decimal('0')
    for operation in operations:
        if operation.operation_type.value == "PayIn":
            sum_pay_in += Decimal(str(operation.payment))
    return sum_pay_in


def get_balance_rub() -> Decimal:
    # Возвращаем остаток денежных средств в портфеле
    return api._client.get_portfolio_currencies(BROKER_ACCOUNT_ID)\
        .payload.currencies[0].balance


def get_nalog_rub() -> Decimal:
    """Возвращаем уплаченный налог за все операции в рублях"""
    operations = api.get_all_operations(BROKER_ACCOUNT_STARTED_AT)

    sum_nalog_rub = Decimal('0')
    for operation in operations:
        if (operation.operation_type.value == "BrokerCommission" or
                operation.operation_type.value == "TaxDividend" or
                operation.operation_type.value == "TaxCoupon"):
            sum_nalog_rub += Decimal(str(operation.payment))
    return sum_nalog_rub * (-1)


def get_dividend_rub() -> Decimal:
    """Возвращаем сумму полученных купонов в рублях"""
    operations = api.get_all_operations(BROKER_ACCOUNT_STARTED_AT)

    sum_dividend_rub = Decimal('0')
    for operation in operations:
        if operation.operation_type.value == "Dividend":
            sum_dividend_rub += Decimal(str(operation.payment))
    return sum_dividend_rub


def get_coupon_rub() -> Decimal:
    """Возвращаем сумму полученных дивидендов в рублях"""
    operations = api.get_all_operations(BROKER_ACCOUNT_STARTED_AT)

    sum_coupon_rub = Decimal('0')
    for operation in operations:
        if operation.operation_type.value == "Coupon":
            sum_coupon_rub += Decimal(str(operation.payment))
    return sum_coupon_rub


def print_info_papers(key) -> dict:
    """Выводит информацию об указанной категории бумаг или о конретной бумаге по её тикеру"""
    positions=api.get_portfolio_positions()
    
    dt={}
    for position in positions:
        if key=="All":
            pass
        elif position.instrument_type != key and position.ticker != key:
            continue

        ticker = position.ticker
        average_price = round(Decimal(position.average_position_price.value), 2)
        balance = int(position.balance)
        expected_yield = round(Decimal(position.expected_yield.value), 2)
        sum_price = average_price * balance + expected_yield
                
        dt[ticker]=(average_price, str(balance), str(expected_yield), str(sum_price))

    return dt


def show_condition() -> dict:
    portfolio_sum = round(get_portfolio_sum(), 2)  # Суммарная стоимость всех бумаг в портфеле
    sum_pay_in = round(get_sum_pay_in(), 2)  # Все пополнения портфеля
    balance_rub = round(get_balance_rub(), 2)  # Остаток денежных средств в рублях
    sum_size_portfel = portfolio_sum + balance_rub  # Денежный обхем портфеля
    sum_nalog_rub = round(get_nalog_rub(), 2)  # Заплаченный налог в рублях
    sum_dividend_rub = round(get_dividend_rub(), 2)  # Сумма полченных дивидендов в рублях
    sum_coupon_rub = round(get_coupon_rub(), 2)  # Сумма полученных купонов в рублях
    profit_in_rub = portfolio_sum - (
            sum_pay_in - balance_rub) + sum_dividend_rub + sum_coupon_rub  # Прибыль портфеля в рублях
    profit_in_percent = round(100 * profit_in_rub / portfolio_sum, 2)  # Прибыль в процентах

    return {
        "Дата открытия портфеля: ": BROKER_ACCOUNT_STARTED_AT,
        "Текущий курс доллара: ": usd_course,
        "\nПополнения: ": sum_pay_in,
        "Стоимость бумаг в портфеле: ": portfolio_sum,
        "Денежный остаток в рублях: ": balance_rub,
        "Денежный объем портфеля: ": sum_size_portfel,
        "\nЗаплаченный налог: ": sum_nalog_rub,
        "Полученные дивиденды: ": sum_dividend_rub,
        "Полученные купоны: ": sum_coupon_rub,
        "\nПрибыль в руб: ": profit_in_rub,
        "Прибыль в %: ": profit_in_percent
    }
    