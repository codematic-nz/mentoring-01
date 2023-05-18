from nicegui import ui
from pathlib import Path

from models.app_model import AppModel


def index_page(model: AppModel):
    def select_market_item(selection_args):
        if len(selection_args.selection) > 0:
            model.sel_instrument_pair = selection_args.selection[0]['instrument_pair']
        else:
            model.sel_instrument_pair = ''

    with ui.row():
        ui.html(Path('app_logo.svg').read_text()).tailwind('w-10 h-10')
        ui.label('Trading Simulator').tailwind('text-3xl font-bold text-center')

    ui.table(
        title='Positions',
        columns=[{'label': 'Instrument', 'field': 'instrument'},
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
        } for price in model.prices
    ]
    market = ui.table(
        title='Market',
        columns=[
            {'label': 'Date', 'field': 'date', 'align': 'left'},
            {'label': 'Instruments', 'field': 'instrument_pair'},
            {'label': 'Bid', 'field': 'bid'},
            {'label': 'Ask', 'field': 'ask'}
        ],
        rows=price_data,
        row_key='instrument_pair',
        selection='single',
        on_select=select_market_item
    )

    with ui.card().bind_visibility(model, 'sel_instrument_pair'):
        with ui.grid(columns=2):
            ui.label('Instruments:')
            ui.label('').bind_text(model, 'sel_instrument_pair')
            ui.label('Quantity:')
            ui.number(label='Quantity', min=1, max=100, step=1, value=1)
            ui.label('Bid:')
            ui.label('')
            ui.label('Ask:')
            ui.label('')
            ui.button('Buy')
            ui.button('Sell')

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
