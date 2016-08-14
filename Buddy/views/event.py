from flask import (Flask, Blueprint, g, render_template, flash, redirect, url_for,
                  abort, jsonify, request)
from Buddy.models import User
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, current_user)
import requests, xmltodict, json

bp = Blueprint('event', __name__)

@bp.route('/create')
@login_required
def create():
	return render_template('event/create.html')

@bp.route('/explore')
@login_required
def explore():
	return render_template('event/explore.html')

@bp.route('/list')
@login_required
def list():
	return render_template('event/list.html')

@bp.route('/map')
@login_required
def map():
	return render_template('event/map.html')

@bp.route('/zillow', methods=('GET', 'POST'))
@login_required
def zillow():
	if request.method == "POST":
		street = request.json['street']
		city = request.json['city']
		state = request.json['state']
		APIkey = "X1-ZWz1dyb53fdhjf_6jziz"
		url = "http://www.zillow.com/webservice/GetSearchResults.htm"
		payload = {'zws-id': APIkey, 'address': street, 'citystatezip': city + " " + state}
		try:
			xmlResponse = requests.get(url, params=payload)
			dictResponse = xmltodict.parse(xmlResponse.content)
			if "response" in dictResponse["SearchResults:searchresults"]:
				if isinstance(dictResponse["SearchResults:searchresults"]["response"]["results"]["result"], dict):
					dictResponse["SearchResults:searchresults"]["response"]["results"]["result"] = [dictResponse["SearchResults:searchresults"]["response"]["results"]["result"]]
					return json.dumps(dictResponse["SearchResults:searchresults"])
			return json.dumps(dictResponse["SearchResults:searchresults"])
		except requests.exceptions.RequestException, e:
			return jsonify({"message": {"code": -999, "text": "Error"}})
		
	return jsonify({"message": {"code": -999, "text": "Error"}})






