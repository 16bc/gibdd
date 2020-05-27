import json
from flask import Flask
from flask import render_template
from apscheduler.schedulers.background import BackgroundScheduler
import collector

DATAFILE = "data.json"
update_interval = 4
app = Flask(__name__)


def readfile(path) -> list:
    lists = [[], [], [], [], [], []]  # [date], [count], [dead], [child_death], [wounded], [child_wounded]
    with open(path, 'r') as file:
        print('File opened')
        for string in file:
            try:
                lst = json.loads(string)
                lists[0].append(lst[0])  # Чтобы сохранить как текст.
                for i in range(1, 6):
                    lists[i].append(int(lst[i]))
            except:
                print(f"Read string in file error! Check the file {path}")
                continue
    return lists

# C 25.05.2020 виджет с данными на главной странице сайта гибдд.рф убрали. :’-(
# @app.before_first_request
# def initialize():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(do_collect, 'interval', hours=update_interval, id='my_job')
#     scheduler.start()


@app.route("/")
def show_stats():
    data = readfile(DATAFILE)
    return render_template('index.html', date=data[0], count=data[1], dead=data[2], child_dead=data[3],
                           wounded=data[4], child_wounded=data[5])


@app.route("/data")
def get_data():
    with open(DATAFILE, 'r') as file:
        text = file.read()
    return text


@app.route("/update")
def do_collect():
    print("Data updating...")
    try:
        return collector.collect()
    except:
        return collector.send_sms()



if __name__ == "__main__":

    app.run(host='0.0.0.0')
