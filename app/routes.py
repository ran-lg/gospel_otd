from app import app
from flask import render_template

from app.generate_gospel_calendar import get_gospel_delta
from app.extract_verses import get_lines_gotd

from datetime import datetime


lang_list = ['pl', 'lat', 'gr']

@app.route('/')
def index():
    fragment = get_gospel_delta(delta = 1)[0]['gospel_otd']
    lines_gotd = get_lines_gotd(fragment, lang_list)
    date = datetime.now().strftime('%d/%m/%Y')
    
    return render_template('gotd.html', lang_list = lang_list, date = date, fragment = fragment, lines_gotd = lines_gotd)
