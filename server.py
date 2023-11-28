from flask import Flask
from flask import render_template, redirect, url_for, session
from flask import Response, request, jsonify
import requests

app = Flask(__name__)

admin_credentials = {'username': 'admin', 'password': '123456'}
app.secret_key = 'debugTeam'  

company_id = 1
subscription_id = 1

company_data = {
	"1":{
		"cid": "1",
		"cname": "CompanyA",
		"email": "1@gmail.com"
        }
}

subscription_data = {
	"1":{
        "sid": "1",
		"cid": "1",
		"subtype": "Free",
		"substa": "active",
		"nddate": "2023-10-29 00:00:00",
		"sdate": "2023-9-29 00:00:00",
		"binfo": "sth"
        }
}

# localhost
service_url = "http://0.0.0.0:3000"
# JWT token
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI1NzM1NjEsImlzcyI6IlN1Yk1hbmFnZXIiLCJzdWIiOiIyMSJ9.gPSQ91ze5GL4CkCE_sRWyPoQRRcEuQsogoQEJ9cxeQs"

# ROUTES

@app.route('/test')
def test():
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }

    try:
        # Make a GET request to the external API
        response = requests.get(service_url+"/company", headers=headers)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse and return the API response
            api_data = response.content
            return api_data
        else:
            # If the request was not successful, return an error message
            return jsonify({'error': f'Request failed with status code {response.status_code}'})

    except Exception as e:
        # Handle any exceptions that may occur during the request
        return jsonify({'error': str(e)})


@app.route('/')
def hello_world():
    return render_template('welcome.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Retrieve form data
        entered_username = request.form['username']
        entered_password = request.form['password']

        # Check if entered credentials match the dummy admin credentials
        if entered_username == admin_credentials['username'] and entered_password == admin_credentials['password']:
            session['authenticated'] = True
            return redirect(url_for('admin_center'))
        else:
            # Render the login page with an error message
            return render_template('admin_login.html', error='Invalid username or password')

    # Render the login page for GET requests
    return render_template('admin_login.html', error=None)
   
@app.route('/admin-center')
def admin_center():
    if not session.get('authenticated'):
        return redirect(url_for('admin_login'))
    return render_template('admin_center.html')

@app.route('/admin-logout')
def admin_logout():
    session.pop('authenticated', None)
    return redirect(url_for('admin_login'))
    
@app.route('/add_company')
def add_company():
    global company_data
    return render_template('add_company.html', d=company_data)

@app.route('/add_susbscription')
def add_susbcription():
    global subscription_data
    return render_template('add_subscription.html', d=subscription_data)

@app.route('/view_company/<id>')
def view_company(id=None):
    global company_data
    i = company_data[id]
    return render_template('view_company.html', i = i)

@app.route('/view_subs/<id>')
def view_subscription(id=None):
    global subscription_data
    global company_data
    i = subscription_data[id]
    cid = subscription_data[id]["cid"]
    cname = company_data[cid]["cname"]
    return render_template('view_subs.html', i = i, name = cname)

@app.route('/view_all_subs')
def view_all(id=None):
    global subscription_data
    all_subs = []
    for key in subscription_data:
        all_subs.append(subscription_data[key])
    return render_template('view_all_subs.html', all_subs = all_subs)

@app.route('/edit_company/<id>')
def edit_company(id=None):
    global company_data
    i = company_data[id]
    return render_template('edit_company.html', i = i)

@app.route('/edit_subscription/<id>')
def edit_subscription(id=None):
    global subscription_data
    i = subscription_data[id]
    cname = company_data[i["cid"]]["cname"]
    return render_template('edit_subscription.html', i = i, cname = cname)

@app.route('/save_data_company', methods=['GET', 'POST'])
def save_data_company():
    global company_data
    global company_id
    
    json_data = request.get_json()
    cname = json_data["cname"]
    email = json_data["email"]

    company_id += 1
    new_name_entry = {
        "cid": str(company_id),
        "cname": cname,
        "email": email
    }
    company_data[str(company_id)]=new_name_entry

    # send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data=company_data, id_add = str(company_id))

@app.route('/save_data_subscription', methods=['GET', 'POST'])
def save_data_subscription():
    global subscription_data
    global subscription_id
    
    json_data = request.get_json()
    cid = json_data["cid"]
    subtype = json_data["subtype"]
    substa = json_data["substa"]
    nddate = json_data["nddate"]
    sdate = json_data["sdate"]
    binfo = json_data["binfo"]
    
    subscription_id += 1
    new_name_entry = {
        "sid": str(subscription_id),
        "cid": cid,
        "subtype": subtype,
        "substa": substa,
        "nddate": nddate,
        "sdate": sdate,
        "binfo": binfo
    }
    subscription_data[str(subscription_id)]=new_name_entry

    # send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data=subscription_data, id_add = str(subscription_id))

@app.route('/edit_company/save_edit', methods=['GET', 'POST'])
def save_edit_comp():
    global company_data
    
    json_data = request.get_json()
    edit_id = json_data["id"]
    name = json_data["name"]
    email = json_data["email"]

    new_name_entry = {
        "cid": edit_id,
        "cname": name,
        "email": email
    }

    company_data[str(edit_id)]=new_name_entry

    # send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data=company_data, id_edit = str(edit_id))

@app.route('/edit_subscription/save_edit', methods=['GET', 'POST'])
def save_edit_subs():
    global subscription_data
    
    json_data = request.get_json()
    edit_id = json_data["id"]
    cid = subscription_data[str(edit_id)]['cid']
    subtype = json_data["subtype"]
    substa = json_data["substa"]
    nddate = json_data["nddate"]
    sdate = json_data["sdate"]
    binfo = json_data["binfo"]

    new_name_entry = {
        "sid": edit_id,
        "cid": cid,
        "subtype": subtype,
        "substa": substa,
        "nddate": nddate,
        "sdate": sdate,
        "binfo": binfo
    }

    subscription_data[str(edit_id)]=new_name_entry

    # send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data=subscription_data, id_edit = str(edit_id))

if __name__ == '__main__':
    app.run(debug=True)
