import json
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

REMINDER_JSON = None

# localhost
service_url = "http://localhost:3000"
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
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
    
    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    response = requests.get(service_url+"/company", headers=headers)
   
    return render_template('admin_center.html', json_profile=response.json())

@app.route('/company-change-profile', methods=['GET', 'POST'])
def company_change_profile():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        newCompanyName = request.form['newname']
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type' : 'application/json'
        }
        
        request_body = {
           "company_name" : newCompanyName
        }
        try:
            response = requests.patch(service_url+"/company/changeCompany", headers=headers, json=request_body)
            api_data = response.content
            if response.status_code == 200:
                    flash("Update company's profile successfullly!", "primary")
                    return redirect(url_for('admin_center'))
            else:
                    # If the request was not successful, return an error message
                    print(f"Update profile error:{api_data}")
                    flash(f'Update profile error:{api_data}, please try again or cantact the service provider.', 'warning')
                    return redirect(url_for('admin_center')) 
        except Exception as e:
                    # Handle any exceptions that may occur during the request
                    return jsonify({'error': str(e)})

    return render_template('company_change_profile.html')

@app.route('/admin-manage-members')
def admin_manage_members():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type' : 'application/json'
    }

    page = request.args.get('page', 1, type=int)
    page_size = 10  
    
    # Send request to service with page and page size parameters
    pagination_url = f"{service_url}/company/getMembers?page={page}&pagesize={page_size}"
    
    try:
        response = requests.get(pagination_url, headers=headers)
        api_data = response.content
        
        if response.status_code == 200:
            paginated_data = response.json()
            members_data = paginated_data.get("members")
            total_members = int(paginated_data.get("total_members"))
            total_pages = int(paginated_data.get("total_pages"))
            return render_template('admin_manage_members.html', data=members_data, total_members=total_members, page=page, page_size=page_size, total_pages=total_pages)
        else:
                # If the request was not successful, return an error message
                print(f"Get Members error:{api_data}")
                flash(f'Get Members error:{api_data}, please try again or cantact the service provider.', 'warning')
                return redirect(url_for('admin_center')) 
    except Exception as e:
                    # Handle any exceptions that may occur during the request
                    return jsonify({'error': str(e)})

@app.route('/admin-view-member/<email>')
def admin_view_member(email):
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type' : 'application/json'
    }

    request_body = {
        "email" : email
    }

    try:
        profile_response = requests.get(service_url+"/admin/member/profile/"+email, headers=headers)
        profile_api_data = profile_response.content

        subscriptions_response = requests.get(service_url+"/admin/subscription/viewSubscriptions", headers=headers, json=request_body)
        subscription_api_data = subscriptions_response.content

        if profile_response.status_code and subscriptions_response.status_code == 200:
            subscriptions_json = subscriptions_response.json()
            subscriptions_data = subscriptions_json.get("subscriptions")
            total_subscriptions = int(subscriptions_json.get("total_subscriptions"))
            return render_template('member_profile.html', json_profile=profile_response.json(), subscriptions_data=subscriptions_data, total_subscriptions=total_subscriptions)
        else:
            # If the request was not successful, return an error message
            print(f"View member's profile error:{profile_api_data} or {subscription_api_data}")
            flash(f'View member\'s profile error:{profile_api_data} or {subscription_api_data}, please try again or cantact the service provider.', 'warning')
            return redirect(url_for('admin_manage_members')) 
    except Exception as e:
                    # Handle any exceptions that may occur during the request
                    return jsonify({'error': str(e)})

@app.route('/admin-change-member-info', methods=['GET', 'POST'])
def admin_change_member_info():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type' : 'application/json'
        }
        
        request_body = {
            "first_name" : first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number
        }

        try:
            response = requests.patch(service_url+"/admin/member/changeMemberInfo", headers=headers, json=request_body)
            api_data = response.content

            if response.status_code == 200:
                return redirect(url_for('admin_manage_members')) 
            else:
                # If the request was not successful, return an error message
                print(f"Update profile error:{api_data}")
                flash(f'Update profile error:{api_data}, please try again or cantact the service provider.', 'warning')
                return redirect(url_for('admin_manage_members')) 
        except Exception as e:
                        # Handle any exceptions that may occur during the request
                        return jsonify({'error': str(e)})
    return redirect(url_for('admin_manage_members'))  

@app.route('/admin-delete-member',  methods=['GET', 'POST'])
def admin_delete_member():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))

    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        try:
            response = requests.delete(service_url+"/admin/member/removeMember/"+email, headers=headers)
            api_data = response.content

            if response.status_code == 204:
                return redirect(url_for('admin_manage_members')) 
            else:
                # If the request was not successful, return an error message
                print(f"Delete member error:{api_data}")
                flash(f'Delete member error:{api_data}, please try again or cantact the service provider.', 'warning')
                return redirect(url_for('admin_manage_members')) 
        except Exception as e:
                # Handle any exceptions that may occur during the request
                return jsonify({'error': str(e)})
    return redirect(url_for('admin_manage_members'))  


@app.route('/admin-change-member-sub', methods=['GET', 'POST'])
def admin_change_member_sub():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        subscription_name = request.form['subscription_name']
        subscription_status = request.form['subscription_status']
        subscription_type = request.form['subscription_type']
        start_date = request.form['start_date']
        next_due_date = request.form['next_due_date']
        billing_info = request.form['billing_info']
        subscription_id = request.form['subscription_id']
        email = request.form['email']
        redirect_url = request.form['redirect_url']

        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type' : 'application/json'
        }
        
        request_body = {
            "subscription_id" : subscription_id,
            "subscription_name" : subscription_name,
            "subscription_status": subscription_status,
            "subscription_type": subscription_type,
            "start_date": start_date,
            "next_due_date": next_due_date,
            "billing_info": billing_info
        }

        try:
            response = requests.patch(service_url+"/admin/subscription/updateSubscription", headers=headers, json=request_body)
            api_data = response.content

            if response.status_code == 200:
                if redirect_url == 'admin_view_member':
                    return redirect(url_for('admin_view_member', email=email))
                return redirect(url_for(redirect_url))
            else:
                # If the request was not successful, return an error message
                print(f"Update Member's Subscription error:{api_data}")
                flash(f'Update Member\'s Subscription error:{api_data}, please try again or cantact the service provider.', 'warning')
                if redirect_url == 'admin_view_member':
                    return redirect(url_for('admin_view_member', email=email))
                return redirect(url_for(redirect_url))
        except Exception as e:
                        # Handle any exceptions that may occur during the request
                        return jsonify({'error': str(e)})
    return redirect(url_for(redirect_url)) 

@app.route('/admin-logout')
def admin_logout():
    session.pop('authenticated', None)
    return redirect(url_for('admin_login'))

@app.route('/add-subs', methods=['GET','POST'])
def add_subs():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        mem_email = request.form.get('mem_email')
        subs_name = request.form.get('subs_name')
        subs_type = request.form.get('subs_type')
        subs_sta = request.form.get('subs_sta')
        next_date = request.form.get('next_date')
        start_date = request.form.get('start_date')
        bill_info = request.form.get('bill_info')

        from_admin = request.form.get('change_from_admin')

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
                if from_admin is not None:
                    return redirect(url_for('admin_view_member', email=mem_email)) 
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

@app.route('/update-subs', methods=['GET','POST'])
def update_subs():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        subscription_name = request.form['subs_name']
        subscription_status = request.form['subs_sta']
        subscription_type = request.form['subs_type']
        start_date = request.form['start_date']
        next_due_date = request.form['next_date']
        billing_info = request.form['bill_info']
        subscription_id = request.form['subs_id']

        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
        }

        request_body = {
            "subscription_id" : subscription_id,
            "subscription_name" : subscription_name,
            "subscription_status": subscription_status,
            "subscription_type": subscription_type,
            "start_date": start_date,
            "next_due_date": next_due_date,
            "billing_info": billing_info
        }

        try:
            # Make a GET request to the external API
            response = requests.patch(service_url+"/admin/subscription/updateSubscription", json=request_body, headers=headers)
            api_data = response.content

            
            if response.status_code == 200:
                flash("Update subscription successfullly!", "primary")
                return redirect(url_for('admin_center'))
            else:
                # If the request was not successful, return an error message
                flash(f'Error: {api_data}', 'warning')
                return redirect(url_for('update_subs')) 

        except Exception as e:
            # Handle any exceptions that may occur during the request
            return jsonify({'error': str(e)})
                  
    return render_template('update_subs.html')

@app.route('/view-all-subs')
def view_all_subs():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
     
    headers = {
        'Authorization': f'Bearer {jwt_token}',
    }

    page = request.args.get('page', 1, type=int)
    page_size = 10  
    
    # Send request to service with page and page size parameters
    pagination_url = f"{service_url}/subscription/allSubscriptions?page={page}&pagesize={page_size}"
    
    try:
        response = requests.get(pagination_url, headers=headers)
        api_data = response.content
        
        if response.status_code == 200:
            paginated_data = response.json()
            subscriptions_data = paginated_data.get("subscriptions")
            total_subscriptions = int(paginated_data.get("total_subscriptions"))
            total_pages = int(paginated_data.get("total_pages"))
            return render_template('view_all_subs.html', data=subscriptions_data, total_subscriptions=total_subscriptions, page=page, page_size=page_size, total_pages=total_pages)
        else:
                # If the request was not successful, return an error message
                print(f"Get Members error:{api_data}")
                flash(f'Get Members error:{api_data}, please try again or cantact the service provider.', 'warning')
                return redirect(url_for('admin_center')) 
    except Exception as e:
                    # Handle any exceptions that may occur during the request
                    return jsonify({'error': str(e)})
    
@app.route('/analyzer', methods=['GET', 'POST'])
def analyzer():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        recipient_email = request.form['analysisEmail']

        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
        }

        request_body = {
            'email' : recipient_email
        }

        try:
            response = requests.post(service_url+"/company/analyzeSubDuration", headers=headers, json=request_body)
            api_data = response.content
            
            if response.status_code == 200:
                flash('Send email successfully', 'info')
            else:
                # If the request was not successful, return an error message
                print(f"Send Analysis error:{api_data}")
                flash(f'Send Analysis error:{api_data}, please try again or cantact the service provider.', 'warning')
        except Exception as e:
                        # Handle any exceptions that may occur during the request
                        return jsonify({'error': str(e)})
    return render_template('analyzer.html')

@app.route('/notification-center', methods=['GET', 'POST'])
def notification_center():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        due_in = request.form['due_in']
        sub_name = request.form['sub_name']


        headers = {
            'Authorization': f'Bearer {jwt_token}',
        }

        try:
            response = requests.get(service_url+f"/company/getExpiringSubscriptionByTime?subscription_name={sub_name}&days={due_in}", headers=headers)
            api_data = response.content
            
            if response.status_code == 200:
               response_data = response.json()
               num_recipients = int(response_data.get('number'))
               global REMINDER_JSON
               REMINDER_JSON = response_data 
               print(response_data)
               print("global save")
               return render_template('notification_center.html', number=num_recipients, json=response_data)
            else:
                # If the request was not successful, return an error message
                print(f"Send Notification error:{api_data}")
                flash(f'Send Notification error:{api_data}, please try again or cantact the service provider.', 'warning')
        except Exception as e:
                        # Handle any exceptions that may occur during the request
                        return jsonify({'error': str(e)})
    return render_template('notification_center.html', number=None, json=None)

@app.route('/send-due-emails', methods=['GET', 'POST'])
def send_due_emails():
    if not session.get('authenticated'):
        flash('You don\'t have permission, please log in as admin to continue', 'warning')
        return redirect(url_for('admin_login'))
    
 
    headers = {
        'Authorization': f'Bearer {jwt_token}',
    }
    print(REMINDER_JSON)
    try:
        response = requests.post(service_url+"/company/sendReminder", headers=headers, json=REMINDER_JSON)
        api_data = response.content
        
        if response.status_code == 200:
            flash('Email send successfully to members', 'info')
        else:
            # If the request was not successful, return an error message
            print(f"Send emails error:{api_data}")
            flash(f'Send emails error:{api_data}, please try again or cantact the service provider.', 'warning')
    except Exception as e:
                    # Handle any exceptions that may occur during the request
                    return jsonify({'error': str(e)})
    return render_template('notification_center.html', number=None, json=None)




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
