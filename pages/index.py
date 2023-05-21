from nicegui import ui
from pathlib import Path

from models.app_model import AppModel, Trade


def index_page(model: AppModel):
    def select_market_item(selection_args):
        if len(selection_args.selection) > 0:
            model.select_price(selection_args.selection[0]['instrument_pair'])
        else:
            model.select_price('')

    def execute_buy(qty: int):
        trade = model.buy(qty)
        add_new_trade(trade)
        ui.notify(f'BUY trade executed - ID {trade.id}', type='positive')

    def execute_sell(qty: int):
        trade = model.sell(qty)
        add_new_trade(trade)
        ui.notify(f'BUY trade executed - ID {trade.id}', type='positive')

    def add_new_trade(trade: Trade):
        trades.rows.append(
            {
                'id': trade.id,
                'date': trade.date.strftime('%Y-%m-%d %H:%M:%S'),
                'buy_sell': trade.buy_sell.value,
                'instrument_a': trade.instrument_a,
                'instrument_b': trade.instrument_b,
                'price': trade.price,
                'quantity': trade.quantity,
                'fee': trade.fee,
                'fee_instrument': trade.fee_instrument
            }
        )
        trades.update()
        # TODO: update positions table

    with ui.row():
        ui.html(Path('app_logo.svg').read_text()).tailwind('w-10 h-10')
        ui.label('Trading Simulator').tailwind('text-3xl font-bold text-center')
        ui.button('Next Day', on_click=model.next_day).tailwind('ml-auto')  # TODO: refresh prices

    with ui.row():
        ui.table(
            title='Positions',
            columns=[
                {'label': 'Instrument', 'field': 'instrument'},
                {'label': 'Quantity', 'field': 'quantity'}
            ],
            rows=[pos.__dict__ for pos in model.portfolio.positions],
        )

        price_data = [
            {
                'date': price.date.strftime('%Y-%m-%d %H:%M:%S'),
                'instrument_pair': f'{price.instrument_pair.id}',
                'bid': price.bid,
                'ask': price.ask,
                'fee_percent': price.fee_percent,
            } for price in model.prices
        ]
        ui.table(
            title='Market Prices',
            columns=[
                {'label': 'Date', 'field': 'date', 'align': 'left'},
                {'label': 'Instruments', 'field': 'instrument_pair'},
                {'label': 'Bid', 'field': 'bid'},
                {'label': 'Ask', 'field': 'ask'},
                {'label': 'Fee %', 'field': 'fee_percent'}
            ],
            rows=price_data,
            row_key='instrument_pair',
            selection='single',
            on_select=select_market_item
        )

    with ui.card().bind_visibility(model, 'sel_instrument_pair'):
        with ui.row():
            ui.label('').bind_text(model, 'sel_instrument_pair').tailwind('text-2xl font-bold')

        with ui.row():
            qty = ui.number(label='Quantity', min=1, max=100, step=1, value=1)
            ui.button('Buy', on_click=lambda: execute_buy(qty.value))
            ui.button('Sell', on_click=lambda: execute_sell(qty.value))

    trades = ui.table(
        title='Trade History',
        columns=[
            {'name': 'id', 'label': 'ID', 'field': 'id'},
            {'name': 'date', 'label': 'Date', 'field': 'date'},
            {'name': 'buy_sell', 'label': 'Buy/Sell', 'field': 'buy_sell'},
            {'name': 'instrument_a', 'label': 'Instrument A', 'field': 'instrument_a'},
            {'name': 'instrument_b', 'label': 'Instrument B', 'field': 'instrument_b'},
            {'name': 'price', 'label': 'Price', 'field': 'price'},
            {'name': 'quantity', 'label': 'Quantity', 'field': 'quantity'},
            {'name': 'fee', 'label': 'Fee', 'field': 'fee'},
            {'name': 'fee_instrument', 'label': 'Fee Instrument', 'field': 'fee_instrument'}
        ],
        rows=[{'id': trade.id} for trade in model.portfolio.trades],
    )

    # ui.table(
    #     title='Trade History',
    #     columns=[
    #         {'name': 'id', 'label': 'ID', 'field': 'id'},
    #         {'name': 'date', 'label': 'Date', 'field': 'date'},
    #         {'name': 'buy_sell', 'label': 'Buy/Sell', 'field': 'buy_sell'},
    #         {'name': 'symbol', 'label': 'Symbol', 'field': 'symbol'},
    #         {'name': 'ccy', 'label': 'CCY', 'field': 'ccy'},
    #         {'name': 'rate', 'label': 'Rate', 'field': 'rate'},
    #         {'name': 'quantity', 'label': 'Quantity', 'field': 'quantity'}
    #     ],
    #     rows=model.get_trades(),
    # )
