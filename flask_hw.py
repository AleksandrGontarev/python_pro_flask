from flask import Flask, request
from faker import Faker
import csv
import statistics
import requests


flask_hw = Flask(__name__)


@flask_hw.route("/")
def head():
    return "Hello !!!"


@flask_hw.route("/requierements")
def requierements(filename = "requierements.txt"):
    result = []
    with open(filename, "r") as txt_file:
        data = txt_file.readlines()
        for i in data:
            result.append(f'<p>{i}</p>')
    return " ".join(result)


@flask_hw.route("/generate_users/")
def generate_users():
    fake = Faker()
    amount = int(request.args.get('count', 100))
    names = []
    result = []
    for i in range(amount):
        names.append(str(fake.first_name()) + " " + str(fake.ascii_email()))
    for i in names:
        result.append(f'<p>{i}</p>')
    return ' '.join(result)



@flask_hw.route("/mean/")
def mean():
    height = []
    weight = []
    with open("hw.csv", 'r') as file:
        reader = csv.DictReader(file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for row in reader:
            height.append(float(row["Height(Inches)"]))
            weight.append(float(row["Weight(Pounds)"]))
    mean_h = statistics.mean(height)*2.54
    mean_w = statistics.mean(weight)*0.453592
    return "<p>Mean height = {} cm</p><p>Mean weight = {} kg</p>".format(mean_h, mean_w)


@flask_hw.route("/space/")
def space():
    r = requests.get('http://api.open-notify.org/astros.json')
    result = r.json()['number']
    return f"{result}"


if __name__ == '__main__':
    flask_hw.run(debug=True)