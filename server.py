import json
import datetime
from flask import Flask,render_template,request,redirect,flash,url_for

MAX_BOOKABLE_PLACES = 12 

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        date_format = "%Y/%m/%d %H:%M:%S"
        for competition in listOfCompetitions:
            competition['date']= datetime.datetime.strptime(competition['date'], date_format)
            if competition['date'] < datetime.datetime.now:
                competition['is_passed'] = True
            else:
                competition['is_passed'] = False
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for("index"))
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if competition['is_passed']==True:
        flash("Sorry- You can not book a passed competition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        if placesRequired > MAX_BOOKABLE_PLACES:
            flash("Try again - You cannot book more than 12 places. ")
            return render_template('booking.html', club=club, competition=competition)
        elif placesRequired > int(club["points"]):
            flash("Try again - your points is less than what you book. ")
            return render_template('booking.html', club=club, competition=competition)
        else:
            flash('Great-booking complete!')
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
            club["points"]= int(club["points"]) - placesRequired
            return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))