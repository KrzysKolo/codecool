from distutils.log import error
import psycopg2
import psycopg2.extras
from flask import Flask, render_template


hostname = 'localhost'
database = 'dbMovie'
username = 'postgres'
password = 'passwd'
port_id = 5432
conn = None
cur = None
try:
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=password,
        port=port_id
    )
    cur = conn.cursor()
    cur.execute('SELECT id, title FROM shows;')
    showsFromData = cur.fetchall()

    def get_shows():
        return showsFromData

    cur.execute(
        "SELECT shows.title, shows.year, shows.runtime, shows.rating, STRING_AGG(genres.name, ', '), shows.trailer, shows.homepage FROM shows, show_genres, genres WHERE show_genres.genre_id=genres.id AND show_genres.show_id=shows.id GROUP BY shows.title, shows.year, shows.runtime, shows.rating, shows.trailer, shows.homepage ORDER BY shows.rating DESC LIMIT 15;")
    showsMostRated = cur.fetchall()

    def get_showsMostRated():
        return showsMostRated

    conn.commit()
except Exception as error:
    print(error)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

app = Flask(__name__)


@app.route('/')
def index():
    shows = get_shows()
    print(shows)
    return render_template('index.html', shows=shows)


@app.route('/most-rated')
def mostRated():
    mostRated = get_showsMostRated()
    return render_template('most-rated.html', mostRated=mostRated)


@app.route('/show/<id>')
def showItem(id):
    return render_template('show-movie.html', mostRated=mostRated)


@app.route('/tv-show')
def design():
    return render_template('design.html')


if __name__ == '__main__':
    app.run()
