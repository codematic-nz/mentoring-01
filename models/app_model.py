from enum import Enum
from datetime import datetime, timezone
from dataclasses import dataclass
import json
from pathlib import Path
from typing import List, Optional


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
    fee_percent: float = 0
    fee_instrument: str = ''


class AppModel:
    def __init__(self) -> None:
        self.portfolio: Portfolio = self.load_portfolio()
        self.day_no = 1
        self.prices: List[Price] = self.load_prices()
        self.next_trade_id: int = 1
        self.sel_instrument_pair: Optional[str] = None
        self.sel_price: Optional[Price] = None
        self.sel_price_ask_text = ''
        self.sel_price_bid_text = ''
        self.sel_price_fee_percent = ''

    def load_portfolio(self) -> Portfolio:
        data = json.loads(Path('data/portfolio.json').read_text())
        return Portfolio(
            positions=[Position(**pos) for pos in data['positions']],
            trades=[Trade(**trade) for trade in data['trades']],
            base_instrument=data['base_instrument']
        )

    def load_prices(self) -> List[Price]:
        prices = []
        data = json.loads(
            Path(f'data/prices_day_{self.day_no}.json').read_text()  # TODO: BUG handle missing price file
        )
        for price in data:
            prices.append(
                Price(
                    date=datetime.strptime(price['date'], '%Y-%m-%dT%H:%M:%S'),
                    instrument_pair=InstrumentPair(**price['instrument_pair']),
                    bid=price['bid'],
                    ask=price['ask'],
                    fee_percent=price['fee_percent'],
                    fee_instrument=price['fee_instrument']
                )
            )
        return prices

    def select_price(self, instrument_pair: Optional[str] = None) -> None:
        self.sel_instrument_pair = instrument_pair
        if self.sel_instrument_pair:
            self.sel_price = [price for price in self.prices
                              if price.instrument_pair.id == instrument_pair][0]
            self.sel_price_ask_text = str(self.sel_price.ask)
            self.sel_price_bid_text = str(self.sel_price.bid)
            self.sel_price_fee_percent = str(self.sel_price.fee_percent)
        else:
            self.sel_price_ask_text = ''
            self.sel_price_bid_text = ''
            self.sel_price_fee_percent = ''

    def buy(self, quantity: int) -> Trade:
        return self._buy_or_sell(BuySell.BUY, quantity)

    def sell(self, quantity: int) -> Trade:
        return self._buy_or_sell(BuySell.SELL, quantity)

    def _buy_or_sell(self, buy_sell: BuySell, quantity: int) -> Trade:
        if self.sel_price:
            trade = Trade(
                id=self.next_trade_id,
                date=datetime.now(timezone.utc),
                buy_sell=buy_sell,
                instrument_a=self.sel_price.instrument_pair.instrument_a,
                instrument_b=self.sel_price.instrument_pair.instrument_b,
                price=float(self.sel_price_ask_text),
                quantity=quantity * (1 if buy_sell == BuySell.BUY else -1),
                fee=0,  # TODO: BUG calculate fee
                fee_instrument=self.sel_price.fee_instrument,
                stage=TradeStage.NEW
            )
            self.execute_trade(trade)
            self.next_trade_id += 1
            return trade
        raise Exception('No price selected')

    def execute_trade(self, trade: Trade) -> None:
        self.portfolio.trades.append(trade)
        self.update_positions(trade)

    def clear_trade(self, trade: Trade) -> None:
        pass  # TODO: implement clear trade

    def settle_trade(self, trade: Trade) -> None:
        pass  # TODO: implement settle trade

    def cancel_trade(self, trade: Trade) -> None:
        pass  # TODO: implement cancel trade

    def get_position_for_instrument(self, instrument: str) -> Position:
        return [pos for pos in self.portfolio.positions
                if pos.instrument == instrument][0]

    def update_positions(self, trade: Trade) -> None:
        pos_a = self.get_position_for_instrument(trade.instrument_a)
        pos_b = self.get_position_for_instrument(trade.instrument_b)

        if trade.buy_sell == BuySell.BUY:
            pos_a.quantity += trade.quantity
            pos_b.quantity -= trade.quantity
        else:
            pos_a.quantity -= trade.quantity
            pos_b.quantity += trade.quantity

        pos_fee = self.get_position_for_instrument(trade.fee_instrument)
        pos_fee.quantity -= trade.fee
        # TODO: BUG handle going negative in positions

    def next_day(self):
        self.day_no += 1
        self.prices = self.load_prices()
        # TODO: BUG needs to reset selected price
