from app import app
import callbacks
from layout import layout

if __name__ == '__main__':
    app.title = 'Twitter HastTag Trend'
    app.layout = layout
    app.run_server(debug=True)
