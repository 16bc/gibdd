import json
from flask import Flask
from flask import render_template


def readfile(path="data.json") -> list:
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
    print(lists)
    return lists



app = Flask(__name__)


@app.route("/")
def show_stats():
    data = readfile()

    return render_template('index.html', date=data[0], count=data[1], dead=data[2], child_dead=data[3],
                           wounded=data[4], child_wounded=data[5])

# @app.route("/update")



if __name__ == "__main__":
    app.run()
