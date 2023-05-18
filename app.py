from nicegui import ui

from models.app_model import AppModel
from pages.index import index_page


@ui.page('/')
def index():
    model = AppModel()
    index_page(model)


ui.run(title='Trading Simulator', port=8080, favicon='app_logo.svg',
       reload=True, native=False)
