# Import statements
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from flask import abort
from backend.db_connection import db

# Creating new blueprint object
companies = Blueprint('companies', __name__)

# Routes

# Return all of the company profiles in the database
@companies.route('/companies', methods=['GET'])
def get_all_companies():
    cursor = db.get_db().cursor()

    query = '''SELECT * FROM companies'''

    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Return the company profile of a specific company
@companies.route('/companies/profile/<id>', methods=['GET'])
def get_comp_prof(id):
    cursor = db.get_db().cursor()

    query = '''SELECT *
               FROM companies
               WHERE CompanyID = %s'''
    cursor.execute(query,(id,))

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Add a new company profile into the database
@companies.route('/companies', methods=['POST'])
def add_new_comp():

    company_data = request.json

    required_fields = ['CompanyName', 'Industry', 'Location', 'Size', 'ProfileManager']
    if not all(field in company_data for field in required_fields):
        return "Missing required fields in the request data."
    
    name = company_data['CompanyName']
    industry = company_data['Industry']
    loc = company_data['Location']
    size = company_data['Size']
    manager = company_data['ProfileManager']

    data = (name, industry, loc, size, manager)

    query = '''INSERT INTO companies (CompanyName, Industry, Location, Size,
                                      ProfileManager)
               VALUES (%s, %s, %s, %s, %s)
            '''
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    response = make_response('Successfully added company profile!')
    response.status_code = 200
    return response

# Update an existing company profile
@companies.route('/companies', methods=['PUT'])
def updated_company_profile():

    company_data = request.json

    required_fields = ['CompanyName', 'Industry', 'Location', 'Size', 'ProfileManager',
                       'CompanyID']
    if not all(field in company_data for field in required_fields):
        return "Missing required fields in the request data."
    
    name = company_data['CompanyName']
    industry = company_data['Industry']
    loc = company_data['Location']
    size = company_data['Size']
    manager = company_data['ProfileManager']
    id = company_data['CompanyID']

    data = (name, industry, loc, size, manager, id)

    query = '''UPDATE companies
               SET CompanyName = %s, Industry = %s, Location = %s,
                   Size = %s, ProfileManager = %s
               WHERE CompanyID = %s
            '''
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    response = make_response('Successfully updated company profile!')
    response.status_code = 200
    return response

# Delete an existing profile from the database
@companies.route('/companies/<company>', methods=['DELETE'])
def delete_company_profile(company):

    query = '''DELETE FROM companies WHERE CompanyName = %s'''

    cursor = db.get_db().cursor()
    cursor.execute(query, (company,))
    db.get_db().commit()

    response = make_response('Successfully company profile!')
    response.status_code = 200
    return response

# Return all of the company names who have internships
@companies.route('/companies/internships', methods=['GET'])
def companies_w_internships():

    query = '''SELECT DISTINCT c.CompanyName
               FROM companies c
               JOIN internships i ON c.CompanyID = i.Company'''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status = 200
    return the_response
    

# returns the company id of a company given the name
@companies.route('/companies/<name>', methods=['GET'])
def get_company_id(name):
    cursor = db.get_db().cursor()

    query = '''SELECT CompanyID
               FROM companies
               WHERE CompanyName = %s'''
    cursor.execute(query, (name,))
    
    theData = cursor.fetchone()  # Use fetchone since it's a single record
    if not theData:
        return make_response(jsonify({"error": "Company not found"}), 404)

    response = make_response(jsonify({"CompanyID": theData[0]}))
    response.status_code = 200
    return response