from flask import Flask, request
from faker import Faker


flask_hw = Flask(__name__)


@flask_hw.route("/")
def head():
    return "Hello !!!"

@flask_hw.route("/requierements")
def requierements(filename = "requierements.txt"):
    with open(filename, "r") as txt_file:
        data = txt_file.readlines()
        return '<p></p>'.join(data)


@flask_hw.route("/generate_users/")
def generate_users():
    fake =Faker()
    amount = int(request.args.get('count'))
    a=[]
    for i in range(amount):
        a.append(str(fake.first_name()) + " " + str(fake.ascii_email()))

    return '<p></p>'.join(a)


if __name__ == '__main__':
    flask_hw.run(debug=True)