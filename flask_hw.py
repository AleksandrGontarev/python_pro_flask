from flask import Flask

flask_hw = Flask(__name__)


@flask_hw.route("/")
def head():
    return "Hello !!!"

@flask_hw.route("/requierements")
def requierements(filename = "requierements.txt"):
    with open(filename, "r") as txt_file:
        data = txt_file.readlines()
        return '<p></p>'.join(data)


if __name__ == '__main__':
    flask_hw.run(debug=True)