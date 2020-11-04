from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import db, connect_to_db, Candidate, Organization, Industry
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
@app.route('/industries')
@app.route('/candidates')
def pages():
    """View pages."""

    return render_template('industries.html')


@app.route('/api/states')
def states():
    states_list = []
    candidates = (db.session.query(Candidate.state).
        join(Organization, Organization.recip_id == Candidate.cid).
        distinct().order_by(Candidate.state))
    for candidate in candidates:
        states_list.append({'state': candidate.state})
    return jsonify({'states': states_list})


@app.route('/api/states/<state>')
def state_candidate(state):
    candidates = (db.session.query(Candidate.party, Candidate.state, Candidate.firstlast,
        Organization.orgname, Organization.amount).
        join(Organization, Organization.recip_id == Candidate.cid).
        filter(Candidate.state == state).
        distinct().order_by(Candidate.firstlast).all())
    candidate_list = []
    for candidate in candidates:
        info = {
            'firstlast': candidate.firstlast,
            'party': candidate.party
        }
        if info not in candidate_list:
            candidate_list.append(info)
    return jsonify({'state': {
        'candidates': candidate_list,
    }})


@app.route('/api/candidates')
def candidates():
    candidate_list = []
    candidates = (db.session.query(Candidate.party, Candidate.state, Candidate.firstlast).\
        join(Organization, Organization.recip_id == Candidate.cid).\
        distinct().order_by(Candidate.state, Candidate.party, Candidate.firstlast))
    for candidate in candidates:
        candidate_list.append({'firstlast': candidate.firstlast,
        'party': candidate.party,
        'state': candidate.state})
    return jsonify({'candidates': candidate_list})


@app.route('/api/candidates/<firstlast>')
def candidate(firstlast):
    candidates = (db.session.query(Candidate.party, Candidate.state, Candidate.firstlast,
        Organization.orgname, Organization.amount).
        join(Organization, Organization.recip_id == Candidate.cid).
        join(Industry, Organization.realcode == Industry.catcode).
        filter(Candidate.firstlast == firstlast).
        distinct().order_by(Candidate.firstlast).all())
    organization_list = []
    for candidate in candidates:
        info = {
            'orgname': candidate.orgname,
            'amount': int(candidate.amount)
        }
        existing_orgs = list(
            organization for organization in organization_list if organization['orgname'] == candidate.orgname)
        if existing_orgs == []:
            organization_list.append(info)
        else:
            existing_orgs[0]['amount'] += int(candidate.amount)
    all_orgs = sorted(organization_list, key=lambda i: i['amount'], reverse=True)
    orgs = [o for o in all_orgs if o['amount'] > 2800]
    return jsonify({'candidate': {
        'orgs': orgs,
    }})


@app.route('/api/donors/<orgname>')
def donor(orgname):
    donor = db.session.query(Organization.cycle, Candidate.party, Candidate.state,
    Candidate.firstlast, Organization.orgname, Organization.amount).\
    join(Candidate, Candidate.cid == Organization.recip_id).\
    filter(Organization.orgname == orgname).\
    order_by(Organization.cycle, Organization.amount).all()
    candidate_list = []
    totals = {
        'D': 0,
        'R': 0,
        'I': 0,
    }
    for donation in donor:
        totals[donation.party] += int(donation.amount)
        info = {
            'firstlast': donation.firstlast,
            'party': donation.party,
            'state': donation.state,
            'total': int(donation.amount)
        }
        existing_candidates = list(candidate for candidate in candidate_list if candidate['firstlast'] == donation.firstlast)
        if existing_candidates == []:
            candidate_list.append(info)
        else:
            existing_candidates[0]['total'] += int(donation.amount)
    candidates = sorted(candidate_list, key = lambda i: i['total'],reverse=True)
    totals['all'] = sum(totals.values())
    totals['d_perc'] = round((totals['D']/totals['all'])*100)
    totals['r_perc'] = round((totals['R']/totals['all'])*100)
    totals['i_perc'] = round((totals['I']/totals['all'])*100)
    return jsonify({'donor': {
        'candidates': candidates,
        'totals': totals,
    }})


@app.route('/api/donors')
def donors():
    donor_list = []
    donors = (db.session.query(Organization.cycle, Candidate.party, Candidate.state,
    Candidate.firstlast, Organization.orgname, Organization.amount).
    join(Candidate, Candidate.cid == Organization.recip_id).
    distinct().order_by(Organization.cycle, Organization.amount))
    for donor in donors:
        donor_list.append({'orgname': donor.orgname})
    return jsonify({'donors': donor_list})


@app.route('/api/industries')
def industries():
    industry_list = []
    for industry in crud.get_industries():
        industry_list.append({'catcode': industry.catcode, 'catname': industry.catname})
    return jsonify({'industries': industry_list}) 


@app.route('/api/industries/<catcode>')
def industry(catcode):
    organizations = db.session.query(Organization.cycle, Candidate.party, Candidate.state,
        Candidate.firstlast, Organization.orgname, Organization.fec_trans_id, Organization.amount).\
        join(Candidate, Candidate.cid == Organization.recip_id).\
        filter(Organization.realcode == catcode).\
        order_by(Organization.cycle, Organization.amount).all()
    unsorted_total_donated = {}
    unsorted_organization_list = []
    for organization in organizations:
        if organization.orgname not in unsorted_total_donated:
            unsorted_total_donated[organization.orgname.strip()] = 0
        unsorted_total_donated[organization.orgname.strip()] += int(organization.amount)
        info = {'orgname': organization.orgname.strip(),
            'amount': organization.amount}
        if info not in unsorted_organization_list:
            unsorted_organization_list.append(info)
    organization_list = sorted(unsorted_organization_list, key=lambda i: i['amount'])
    total_donated = {k: v for k, v in sorted(
        unsorted_total_donated.items(), key=lambda item: -item[1])}
    print("total_donated is:", total_donated)
    for org in list(total_donated.keys()):
        if total_donated[org] < 2800:
            del total_donated[org]
    return jsonify({'industry': {
        'organizations': organization_list,
        'total_donated': total_donated
    }})


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


# organizations = Organization.query.filter(
#     Organization.realcode == catcode).distinct(Organization.orgname).all()
