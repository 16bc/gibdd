from flask import Flask
from flask import render_template
from collector import readfile, convert, collect

DATAFILE = "data.json"
app = Flask(__name__)


@app.route("/")
def show_stats():
    data = readfile(DATAFILE)
    return render_template('index.html', date=data[0], count=data[1], dead=data[2], child_dead=data[3],
                           wounded=data[4], child_wounded=data[5])


@app.route("/dictdata")
def get_dict_data():
    text = convert(DATAFILE)
    return text


@app.route("/listdata")
def get_list_data():
    with open(DATAFILE, 'r') as file:
        text = file.read()
    return text


@app.route("/update")
def do_collect():
    print("Data updating...")
    return collect()



if __name__ == "__main__":

    app.run(host='0.0.0.0')
