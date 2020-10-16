"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/donors')
def all_donors():
    """View all donors/food companies."""

    return render_template('donors.html')


@app.route('/api/donors/<donor_id>')
def donor(donor_id):
    donor = crud.get_donor_by_id(donor_id)
    candidates = []
    for donation in donor.donations:
        info = {
            'firstlast': donation.candidate.firstlast,
            'party': donation.candidate.party,
            'state': donation.candidate.state,
            'total': donation.total
        }
        if info not in candidates:
            candidates.append(info)
    return jsonify({'donor': {
        # 'donor_id': donor.donor_id,
        # 'org_name': donor.org_name,
        'candidates': candidates
    }})

@app.route('/api/donors')
def donors():
    donor_list = []
    for donor in crud.get_all_donors():
        donor_list.append({'donor_id': donor.donor_id, 'org_name': donor.org_name})
    return jsonify({'donors': donor_list})
    

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


# """Server for movie ratings app."""


# app = Flask(__name__)
# app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined


# @app.route('/')
# def homepage():
#     """View homepage."""

#     return render_template('homepage.html')


# @app.route('/politicians')
# def all_politicians():
#     """View all politicians."""
#     return render_template('politicians.html')

# # API
# # add your routes here


# @app.route('/api/movies/<id>')
# def movie(id):
#     movie = crud.get_movie_by_id(id)
#     return jsonify({'movie': {'movie_id': movie.movie_id, 'title': movie.title, 'overview': movie.overview, 'release_date': movie.release_date, 'poster_path': movie.poster_path}})


# @app.route('/api/movies')
# def movies():
#     movie_list = []
#     for movie in crud.get_movies():
#         movie_list.append({'movie_id': movie.movie_id, 'title': movie.title, 'overview': movie.overview,
#                            'release_date': movie.release_date, 'poster_path': movie.poster_path})
#     return jsonify({'movies': movie_list})


# if __name__ == '__main__':
#     connect_to_db(app)
#     app.run(host='0.0.0.0', debug=True)
