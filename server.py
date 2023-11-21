from flask import Flask
from flask import render_template, redirect, url_for, session
from flask import Response, request, jsonify

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


# ROUTES

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
    global data
    return render_template('add_company.html', d=data)

@app.route('/add_susbscription')
def add_susbcription():
    global data
    return render_template('add_subscription.html', d=data)

@app.route('/save_data_company', methods=['GET', 'POST'])
def save_data_company():
    global company_datadata
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
    data[str(company_id)]=new_name_entry

    # send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data=data, id_add = str(company_id))

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
    data[str(subscription_id)]=new_name_entry

    # send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data=data, id_add = str(subscription_id))

if __name__ == '__main__':
    app.run(debug=True)
    #print(add_name())
