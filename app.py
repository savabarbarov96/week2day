from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

def week_to_date(week_string):
    if week_string.startswith("wk"):
        week_string = week_string[2:]

    year = int(week_string[:2]) + 2000
    week = int(week_string[2:4])
    weekday = int(week_string[5])

    first_day = datetime(year, 1, 1)
    first_monday = first_day + timedelta(days=(1 - first_day.isoweekday()) % 7)
    target_date = first_monday + timedelta(weeks=(week - 1), days=(weekday - 1))

    return target_date.strftime('%d %B, %A')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        week_string = request.form['week_string']
        result = week_to_date(week_string)
        return render_template('index.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)