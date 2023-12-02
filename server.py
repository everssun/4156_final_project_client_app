from flask import Flask
from flask import render_template, redirect, url_for, session, flash
from flask import Response, request, jsonify
import requests

app = Flask(__name__)

admin_credentials = {'username': 'admin', 'password': '123456'}
app.secret_key = 'debugTeam'  

company_id = 1
subscription_id = 1
cookies = ""

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
service_url = "http://localhost:3000"
# JWT token
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI1NzM1NjEsImlzcyI6IlN1Yk1hbmFnZXIiLCJzdWIiOiIyMSJ9.gPSQ91ze5GL4CkCE_sRWyPoQRRcEuQsogoQEJ9cxeQs"

# ROUTES

# 快过期email

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

@app.route('/test-session')
def test_session():
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }

    try:
        # Make a GET request to the external API
        response = requests.get(service_url, headers=headers)

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
def welcome():
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

@app.route('/add_subscription')
def add_susbcription():
    global subscription_data
    return render_template('add_subscription.html', d=subscription_data)

@app.route('/add_subs', methods=['GET','POST'])
def add_subs():
    if request.method == 'POST':
        mem_email = request.form.get('mem_email')
        subs_name = request.form.get('subs_name')
        subs_type = request.form.get('subs_type')
        subs_sta = request.form.get('subs_sta')
        next_date = request.form.get('next_date')
        start_date = request.form.get('start_date')
        bill_info = request.form.get('bill_info')

        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
        }

        request_body = {
            "member_email" : mem_email,
            "subscription_name" : subs_name,
            "subscription_type" : subs_type,
            "subscription_status": subs_sta,
            "next_due_date" : next_date,
            "start_date": start_date,
            "billing_info": bill_info
        }

        try:
            # Make a POST request to the external API
            response = requests.post(service_url+"/subscription/addSubscription", json=request_body, headers=headers)
            api_data = response.content
            print(api_data)
            
            if response.status_code == 200:
                flash("Add subscription successfullly!", "primary")
                return redirect(url_for('add_subs'))
            else:
                # If the request was not successful, return an error message
                print(f"subscription add error:{api_data}")
                flash(f'Error: {api_data}', 'warning')
                return redirect(url_for('add_subs')) 

        except Exception as e:
            # Handle any exceptions that may occur during the request
            return jsonify({'error': str(e)})
            
            
    return render_template('add_subs.html')

@app.route('/update_subs', methods=['GET','POST'])
def update_subs():
    if request.method == 'POST':
        mem_email = request.form.get('mem_email')
        subs_name = request.form.get('subs_name')
        new_act = request.form.get('new_act')
        
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
        }

        request_body = {
            "email" : mem_email,
            "subscription_name" : subs_name,
            "new_action" : new_act
        }

        try:
            # Make a GET request to the external API
            response = requests.patch(service_url+"/subscription/updateSubscription", json=request_body, headers=headers)
            api_data = response.content
            print(api_data)
            
            if response.status_code == 200:
                return redirect(url_for('admin_center'))
            else:
                # If the request was not successful, return an error message
                print(f"subscription update error:{api_data}")
                flash('This subscription is not found, please check the email and subscription name', 'warning')
                return redirect(url_for('update_subs')) 

        except Exception as e:
            # Handle any exceptions that may occur during the request
            return jsonify({'error': str(e)})
            
            
    return render_template('update_subs.html')

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

@app.route('/member-signup', methods=['GET','POST'])
def member_signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        phone = request.form.get('phone')

        # print(f"Email: {email}, First Name: {first_name}, Last Name: {last_name}, Password: {password}, Phone: {phone}")
        # TODO: Add some sql injection attack protection (also protect on service side)
        
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
        }

        request_body = {
            "first_name" : first_name,
            "last_name" : last_name,
            "email" : email,
            "password": password,
            "phone_number" : phone
        }

        try:
            # Make a GET request to the external API
            response = requests.post(service_url+"/member/addMember", json=request_body, headers=headers)
            api_data = response.content
            print(api_data)
            
            if response.status_code == 200:
                return redirect(url_for('member_login'))
            else:
                # If the request was not successful, return an error message
                print(f"member sign up error:{api_data}")
                flash('Your email has been registered before, please login here', 'warning')
                return redirect(url_for('member_login')) 

        except Exception as e:
            # Handle any exceptions that may occur during the request
            return jsonify({'error': str(e)})
            
            
    return render_template('member_signup.html')


@app.route('/member-login', methods=['GET','POST'])
def member_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # TODO: Add some sql injection attack protection (also protect on service side)
        
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
        }

        request_body = {
            "email" : email,
            "password": password
        }

        try:
            # Make a GET request to the external API
            response = requests.post(service_url+"/member/login", json=request_body, headers=headers)
            api_data = response.content
            print(api_data)
            
            if response.status_code == 200:
                # set_cookie_header = response.headers.get('Set-Cookie')
                cookies_list = [{'name': cookie.name, 'value': cookie.value} for cookie in response.cookies]
                
                # Store the cookies in the Flask session
                session['cookies'] = cookies_list
                print(session['cookies'])
                return redirect(url_for('member_center'))
            elif response.status_code == 401:
                flash('Invalid email or password. Please try again.', 'primary')
            else:
                # If the request was not successful, return an error message
                return api_data

        except Exception as e:
            # Handle any exceptions that may occur during the request
            return jsonify({'error': str(e)})
       
    return render_template('member_login.html')

@app.route('/member-center', methods=['GET','POST'])
def member_center():
    cookies_list = session.get('cookies')

    if not cookies_list:
        flash('Please log in to access the member center.', 'warning')
        return redirect(url_for('member_login')) 
    
    # Reconstruct the RequestsCookieJar from the list of dictionaries
    cookies = {cookie['name']: cookie['value'] for cookie in cookies_list}
    print(cookies)

    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    response = requests.get(service_url+"/member/profile", headers=headers, cookies=cookies)
    print(response.json())
    if response.status_code == 200:
        return render_template('member_center.html', json_profile=response.json())
    
    flash('Your session expired, please login again.', 'warning')
    return redirect(url_for('member_login')) 

@app.route('/logout')
def logout():
    # Clear session cookies
    session.clear()
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True)
