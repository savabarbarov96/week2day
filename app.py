import re
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

def week_to_date(week_string):
    try:
        if week_string.startswith("wk"):
            week_string = week_string[2:]

        pattern = re.compile(r'^\d{4}\.\d$')
        if not pattern.match(week_string):
            return "Error: Invalid input format. Please use 'wkXXXX.X' or 'XXXX.X"

        year = int(week_string[:2]) + 2000
        week = int(week_string[2:4])
        weekday = int(week_string[5])

        if week < 1 or week > 53 or weekday < 1 or weekday > 7:
            return "Error: Invalid week or weekday value. Week should be between 1 and 53, and weekday should be between 1 and 7."

        first_day = datetime(year, 1, 1)
        first_monday = first_day + timedelta(days=(1 - first_day.isoweekday()) % 7)
        target_date = first_monday + timedelta(weeks=(week - 1), days=(weekday - 1))

        return target_date.strftime('%d %B, %A')
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

@app.route('/<date>')
def json_response(date):
    return jsonify(week_to_date(date))



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        week_string = request.form['week_string']
        result = week_to_date(week_string)
        return render_template('index.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
