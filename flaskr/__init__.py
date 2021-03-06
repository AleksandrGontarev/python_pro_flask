import os
from flask import (
   Flask, flash, g, redirect, render_template, request, session, url_for
)
from faker import Faker
import csv
import statistics
import requests
import functools
from flaskr.db import get_db
from pprint import pprint


def create_app(test_config=None):
    # create and configure the app
    flask_hw = Flask(__name__, instance_relative_config=True)
    flask_hw.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(flask_hw.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        flask_hw.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        flask_hw.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(flask_hw.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @flask_hw.route("/")
    def head():
        return "Hello !!!"

    @flask_hw.route("/requierements")
    def requierements(filename="requierements.txt"):
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
        mean_h = statistics.mean(height) * 2.54
        mean_w = statistics.mean(weight) * 0.453592
        return "<p>Mean height = {} cm</p><p>Mean weight = {} kg</p>".format(mean_h, mean_w)

    @flask_hw.route("/space/")
    def space():
        r = requests.get('http://api.open-notify.org/astros.json')
        result = r.json()['number']
        return f"{result}"

    @flask_hw.route('/names/')
    def names():
        db = get_db()
        names = db.execute(
            'SELECT COUNT(DISTINCT artist)'
            ' FROM track'
                ).fetchall()
        return  render_template('names.html', names=names)


    @flask_hw.route('/traks/')
    def traks():
        db = get_db()
        traks = db.execute(
            'SELECT COUNT(*)'
            ' FROM track'
        ).fetchone()
        return render_template('traks.html', traks=traks)


    @flask_hw.route('/tracks/<genre_1>')
    def genre(genre_1):
        db = get_db()
        result = db.execute(
            "SELECT COUNT (*) FROM track WHERE genre = ?",
            (genre_1,)
        ).fetchall()[0]
        return render_template('genre.html', result=result, genre_1=genre_1)


    @flask_hw.route('/tracks-sec/')
    def tracks_sec():
        tracks = []
        db = get_db()
        result = db.execute(
            "SELECT title, track_length FROM track"
            ).fetchall()
        for row in result:
            tracks.append(row[0:len(row)])
        return render_template('track_length.html', result=tracks)


    @flask_hw.route('/tracks-sec/statistics/')
    def statistics():
        db = get_db()
        result = db.execute(
            "SELECT AVG(track_length) FROM track"
            ).fetchone()[0]
        total_duration = db.execute(
            "SELECT SUM(track_length) FROM track"
            ).fetchone()[0]
        return render_template('statistics.html', result=result, total_duration=total_duration)



    return flask_hw