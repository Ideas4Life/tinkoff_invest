#from decimal import Decimal
from pytz import timezone
from datetime import datetime
#from pycbrf.toolbox import ExchangeRates


def _get_current_timezone() -> timezone:
    return timezone('Europe/Moscow')


def get_now() -> str:
    return _get_current_timezone().localize(datetime.now())


def localize(d: datetime) -> datetime:
    return _get_current_timezone().localize(d)
