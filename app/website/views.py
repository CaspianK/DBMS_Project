from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from base64 import b64encode
import sys, os
from . import pool

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/athletes', defaults={'sort': 'name', 'page': 0})
@views.route('/athletes/<string:sort>/page/<int:page>')
def athletes(sort, page):
    perpage = 500
    startat = 1+perpage*page
    endat = startat+perpage
    connection = pool.acquire()
    cursor = connection.cursor()
    if sort == 'name':
        cursor.execute("SELECT * FROM(SELECT a.*, Row_Number() OVER (ORDER BY name) MyRow FROM Athletes a) WHERE MyRow BETWEEN :startat AND :endat", startat=startat, endat=endat)
    elif sort == 'age':
        cursor.execute("SELECT * FROM(SELECT a.*, Row_Number() OVER (ORDER BY age) MyRow FROM Athletes a) WHERE MyRow BETWEEN :startat AND :endat", startat=startat, endat=endat)
    elif sort == 'height':
        cursor.execute("SELECT * FROM(SELECT a.*, Row_Number() OVER (ORDER BY height) MyRow FROM Athletes a) WHERE MyRow BETWEEN :startat AND :endat", startat=startat, endat=endat)
    elif sort == 'weight':
        cursor.execute("SELECT * FROM(SELECT a.*, Row_Number() OVER (ORDER BY weight) MyRow FROM Athletes a) WHERE MyRow BETWEEN :startat AND :endat", startat=startat, endat=endat)
    elif sort == 'bmi':
        cursor.execute("SELECT * FROM(SELECT a.*, Row_Number() OVER (ORDER BY bmi) MyRow FROM Athletes a) WHERE MyRow BETWEEN :startat AND :endat", startat=startat, endat=endat)
    result = list(cursor.fetchall())
    return render_template("athletes.html", athletes=result, page=page, sort=sort)

@views.route('/athletes/add', methods=['GET', 'POST'])
def add():
    connection = pool.acquire()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        sex = request.form['sex']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        team = request.form['team']
        noc = request.form['noc']
        games = request.form['games']
        year = request.form['year']
        season = request.form['season']
        city = request.form['city']
        sport = request.form['sport']
        event = request.form['event']
        medal = request.form['medal']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ATHLETES (id, name, sex, age, height, weight, team, noc, games, year, season, city, sport, event, medal)" +
                        " VALUES (:id ,:name, :sex, :age, :height, :weight, :team, :noc, :games, :year, :season, :city, :sport, :event, :medal)",
                        id=id, name=name, sex=sex, age=age, height=height, weight=weight, team=team, noc=noc, games=games, year=year, season=season, city=city, sport=sport, event=event, medal=medal)  
        connection.commit()
        cursor.execute("SELECT * FROM ATHLETES WHERE ID = :id", id=id)
        athlete = list(cursor.fetchone())
        connection.close()
        return render_template('athlete.html', athlete=athlete)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM NOC")
    noc = list(cursor.fetchall())
    cursor.execute("SELECT * FROM SPORTS")
    sports = list(cursor.fetchall())
    return render_template('add.html', nocs=noc, sports=sports)

@views.route('/athletes/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ATHLETES WHERE ID = :id", id=id)
    connection.commit()
    connection.close()
    return redirect(url_for('views.athletes'))

@views.route('/athletes/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    connection = pool.acquire()
    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        team = request.form['team']
        noc = request.form['noc']
        games = request.form['games']
        year = request.form['year']
        season = request.form['season']
        city = request.form['city']
        sport = request.form['sport']
        event = request.form['event']
        medal = request.form['medal']
        cursor = connection.cursor()
        cursor.execute("UPDATE ATHLETES SET name = :name, sex = :sex, age = :age, height = :height, weight = :weight, team = :team, noc = :noc, games = :games, year = :year, season = :season, city = :city, sport = :sport, event = :event, medal = :medal WHERE id = :id",
                        id=id, name=name, sex=sex, age=age, height=height, weight=weight, team=team, noc=noc, games=games, year=year, season=season, city=city, sport=sport, event=event, medal=medal)  
        connection.commit()
        cursor.execute("SELECT * FROM ATHLETES WHERE ID = :id", id=id)
        athlete = list(cursor.fetchone())
        connection.close()
        return render_template('athlete.html', athlete=athlete)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM ATHLETES WHERE ID = :id', id=id)
    result = list(cursor.fetchone())
    cursor.execute("SELECT * FROM NOC")
    noc = list(cursor.fetchall())
    cursor.execute("SELECT * FROM SPORTS")
    sports = list(cursor.fetchall())
    return render_template('edit.html', id=id, athlete=result, nocs=noc, sports=sports)

@views.route('/athletes/<int:id>')
def athlete(id):
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ATHLETES WHERE ID = :id", id=id)
    athlete = list(cursor.fetchone())
    return render_template('athlete.html', athlete=athlete)

@views.route('/sports/<string:sport>')
def sport(sport):
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM SPORTS WHERE SPORT = :sport", sport=sport)
    sport = list(cursor.fetchone())
    blob = sport[1].read()
    response = make_response(blob)
    response.headers["Content-type"] = "image/jpeg"
    return render_template('sport.html', sport=sport, image=blob)