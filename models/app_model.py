from enum import Enum
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import List, Dict


class BuySell(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class TradeStage(Enum):
    NEW = 'NEW'
    EXECUTED = 'EXECUTED'
    CLEARED = 'CLEARED'
    SETTLED = 'SETTLED'
    CANCELLED = 'CANCELLED'


@dataclass
class Trade:
    id: int
    date: datetime
    buy_sell: BuySell
    instrument_a: str
    instrument_b: str
    price: float
    quantity: int
    fee: float
    fee_instrument: str
    stage: TradeStage

@dataclass
class InstrumentPair:
    id: str
    instrument_a: str
    instrument_b: str


@dataclass
class Position:
    instrument: str
    quantity: float


@dataclass
class Portfolio:
    positions: List[Position]
    trades: List[Trade]
    base_instrument: str


@dataclass
class Price:
    date: datetime
    instrument_pair: InstrumentPair
    bid: float
    ask: float


class AppModel:
    def __init__(self) -> None:
        self.portfolio: Portfolio = self.load_portfolio()
        self.prices: List[Price] = self.load_prices()
        self.sel_instrument_pair = ''

    def load_portfolio(self) -> Portfolio:
        data = json.loads(Path('data/portfolio.json').read_text())
        return Portfolio(
            positions=[Position(**pos) for pos in data['positions']],
            trades=[Trade(**trade) for trade in data['trades']],
            base_instrument=data['base_instrument']
        )

    def load_prices(self) -> List[Price]:
        prices = []
        data = json.loads(Path('data/prices.json').read_text())
        for price in data:
            prices.append(
                Price(
                    date=datetime.strptime(price['date'], '%Y-%m-%dT%H:%M:%S'),
                    instrument_pair=InstrumentPair(**price['instrument_pair']),
                    bid=price['bid'],
                    ask=price['ask']
                )
            )
        return prices

    def execute_trade(self, trade: Trade) -> None:
        self.portfolio.trades.append(trade)
        self.update_positions(trade)

    def clear_trade(self, trade: Trade) -> None:
        pass

    def settle_trade(self, trade: Trade) -> None:
        pass

    def cancel_trade(self, trade: Trade) -> None:
        pass

    def update_positions(self, trade: Trade) -> None:
        # if trade.buy_sell == BuySell.BUY:
        #     self.portfolio.positions[trade.instrument_a] += trade.quantity
        #     self.portfolio.positions[trade.instrument_b] -= trade.quantity
        # else:
        #     self.portfolio.positions[trade.instrument_a] -= trade.quantity
        #     self.portfolio.positions[trade.instrument_b] += trade.quantity
        # self.portfolio.positions[trade.fee_instrument] -= trade.fee
        pass
