from nicegui import ui
import os

from models.app_model import AppModel
from pages.index import index_page


@ui.page('/')
def index():
    model = AppModel()
    index_page(model)


reload = os.getenv('RELOAD', 'false').lower() == 'true'

ui.run(title='Trading Simulator', favicon='app_logo.svg',
       reload=reload, native=False)
