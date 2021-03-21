from datetime import datetime
from decimal import Decimal
from typing import List

import tinvest
import tinvest.schemas

from utils import localize, get_now


class TinkoffApi:
    """Обёртка для работы с API Тинькова на основе библиотеки tinvest"""
    def __init__(self, api_token: str, broker_account_id: int):
        self._client = tinvest.SyncClient(api_token)
        self._broker_account_id = broker_account_id

    def get_usd_course(self) -> Decimal:
        """Отдаёт текущий курс доллара в брокере"""
        return Decimal(str(self
            ._client.get_market_orderbook(figi="BBG0013HGFT4", depth=1)
            .payload.last_price)
        )


    def get_portfolio_positions(self) \
                -> List[tinvest.schemas.PortfolioPosition]:
        """Возвращает все позиции в портфеле"""
        return (self._client.get_portfolio(self._broker_account_id).payload.positions)


    def get_all_operations(self, broker_account_started_at: datetime) \
                -> List[tinvest.schemas.Operation]:
        """Возвращает все операции в портфеле с указанной даты"""
        from_ = localize(broker_account_started_at)
        now = get_now()

        operations = (self._client.\
            get_operations(broker_account_id=self._broker_account_id, from_=from_, to=now)\
            .payload.operations)
        return operations