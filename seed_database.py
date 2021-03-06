# """Script to seed database."""

import os
import json
from random import choice, randint
import pprint

import crud
from model import Candidate, Donor
import model
import server
from opensecrets_api import get_candidates, get_donors


if False:
    os.system('dropdb donations')
    os.system('createdb donations')
    model.connect_to_db(server.app)
    model.db.create_all()
    candidates = get_candidates()
    created_cids = set()
    for candidate in candidates:
        cid = candidate['cid']
        if cid not in created_cids:
            db_candidate = crud.create_candidate(
                cid, candidate['firstlast'], candidate['party'], candidate['state'])
            created_cids.add(cid)
else:
    model.connect_to_db(server.app)