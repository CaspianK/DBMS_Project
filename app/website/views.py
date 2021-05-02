from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from base64 import b64encode
import sys, os
from . import pool
import numpy as np
import matplotlib.pyplot as plt, mpld3

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/athletes', defaults={'sort': 'name', 'page': 0}, methods=['GET', 'POST'])
@views.route('/athletes/<string:sort>/page/<int:page>')
def athletes(sort, page):
    connection = pool.acquire()
    cursor = connection.cursor()
    if request.method == "POST":
        search = "%" + request.form['search'] + "%"
        cursor.execute("SELECT * FROM ATHLETES WHERE NAME LIKE :search OR TEAM LIKE :search OR NOC LIKE :search OR CITY LIKE :search OR SPORT LIKE :search OR MEDAL LIKE :search", search=search)
    else:
        perpage = 500
        startat = 1+perpage*page
        endat = startat+perpage
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
    blob = b64encode(sport[1].read()).decode()
    response = make_response(blob)
    response.headers["Content-type"] = "image/jpeg"
    return render_template('sport.html', sport=sport, image=blob)

@views.route('athletes/charts')
def charts():
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("select 10 from dual")
    for row in cursor:
        totalemps=row[0]
    t=np.arange(totalemps)
    cursor.execute("SELECT * FROM (SELECT noc, count(medal) as count FROM athletes GROUP BY noc ORDER BY count DESC) WHERE ROWNUM <= 10")
    nocs=[]
    count=[]
    for row in cursor:
        nocs.append(row[0])
        count.append(row[1])
    bar_width=0.5
    plt.bar(t,count,bar_width,label="Count")
    plt.title("Top 10 countries by number of medals")
    plt.xlabel("Country")
    plt.ylabel("Count")
    plt.xticks(t,nocs)
    plt.grid(True)
    plt.legend()
    xs=[x for x in range(0,totalemps)]
    for x,y in zip(xs,count):
        plt.annotate(count[x],(x-bar_width/1.5,y))
    plt.savefig('website/static/img/bar.png')
    plt.cla()
    cursor.execute("select COUNT(DISTINCT(medal))+1 from athletes")
    for row in cursor:
        totalemps=row[0]
    cursor.execute("select case when medal IS NULL THEN 'No Medals' ELSE medal END AS medal, count(*) from athletes group by medal")
    medals=[]
    count=[]
    for row in cursor:
        medals.append(row[0])
        count.append(row[1])
    explode=[0.2 if count[x]==max(count) else 0 for x in np.arange(0,totalemps)]
    plt.pie(count,explode=explode,labels=medals,autopct="%1.1f%%",shadow=True)
    plt.savefig('website/static/img/pie.png')
    plt.switch_backend('agg')
    return render_template('charts.html')