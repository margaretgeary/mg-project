"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import db, connect_to_db, Organization, Donor
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/industries')
def all_industries():
    """View all donors/food companies."""

    return render_template('industries.html')

#SQLALCHEMY EAGER LOADING
#N+1 QUERIES
#JOIN DONOR, CANDIDATE, & DONATION TOGETHER
#RATHER THAN 3 SEPARATE REQUESTS
@app.route('/api/donors/<donor_id>')
def donor(donor_id):
    donor = crud.get_donor_by_id(donor_id)
    candidate_list = []
    totals = {
        'D': 0,
        'R': 0,
    }
    for donation in donor.donations:
        totals[donation.candidate.party] += int(donation.total)
        info = {
            'firstlast': donation.candidate.firstlast,
            'party': donation.candidate.party,
            'state': donation.candidate.state,
            'total': int(donation.total)
        }
        existing_candidates = list(candidate for candidate in candidate_list if candidate['firstlast'] == donation.candidate.firstlast)
        if existing_candidates == []:
            candidate_list.append(info)
        else:
            existing_candidates[0]['total'] += int(donation.total)
    candidates = sorted(candidate_list, key = lambda i: i['total'],reverse=True)
    totals['all'] = sum(totals.values())
    totals['d_perc'] = round((totals['D']/totals['all'])*100)
    totals['r_perc'] = round((totals['R']/totals['all'])*100)
    return jsonify({'donor': {
        'candidates': candidates,
        'totals': totals,
    }})

@app.route('/api/donors')
def donors():
    donor_list = []
    for donor in crud.get_all_donors():
        donor_list.append({'donor_id': donor.donor_id, 'org_name': donor.org_name})
    return jsonify({'donors': donor_list})


@app.route('/api/industries')
def industries():
    industry_list = []
    for industry in crud.get_industries():
        industry_list.append({'catcode': industry.catcode, 'catname': industry.catname})
    return jsonify({'industries': industry_list}) 


@app.route('/api/industries/<catcode>')
def industry(catcode):
    organizations = db.session.query(Organization.orgname, Donor.donor_id, Donor.org_name).\
        join(Donor, Donor.org_name == Organization.orgname).\
        filter(Organization.realcode == catcode).distinct(Organization.orgname).all()
    organization_list = []
    for organization in organizations:
        info = {'orgname': organization.orgname.strip(),
            'donor_id': organization.donor_id,
            'org_name': organization.org_name}
        if info not in organization_list:
            organization_list.append(info)
    return jsonify({'industry': {
        'organizations': organization_list
    }})


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


# organizations = Organization.query.filter(
#     Organization.realcode == catcode).distinct(Organization.orgname).all()
