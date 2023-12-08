# 4156_final_project_client_app

## How to Run:

Run our service https://github.com/fzhang2716/COMS4156_AdvancedSoftwareEngineering in another terminal, then

```
pip install -r requirements.txt
python server.py
```
Then go the link generated

## Client App Overview
Our service's target clients are any SAAS providers or entities who provide subscriptions to their members. This client app is a general SAAS company. 

The client app allows members to securely sign up, log in, and manage their subscriptions to the company's services using our service's APIs. In addition, the admin of the SAAS company is able to securely manage their members' subscriptions and profile data and send reminders to members whose subscriptions are about to be due. Moreover, with our service APIs, the client app can generate a statistical report of its company's services for business plan insights.

Our service is secure and supports multiple clients' exercises. Each client needs to request a JWT token, and clients may hardcode its token in their client app. When using our service's APIs, clients need to include the JWT token in the request header. Member access is protected by session cookies, which are handled in our services so clients set up are easy to go. Clients may refer to our service API documentation when building their own client apps.

## Demo Client APP
### Homepage
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/97cb41f6-08ba-4150-9fcc-6d611ef3ff21)
---
## Member
---
### Member Signup
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/26092e87-441a-4e92-871e-298321878ebc)
### Member Login
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/f71ba9b4-651f-4654-8bd9-439ac8f831e9)
### Member Center
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/b76ae371-2b77-4f11-9e90-13c6a05713ae)

Modify Subscription:
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/1ca528dd-ddc8-4423-b70f-3a31ef8dd3aa)

---
## Admin
---
### Admin Login
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/dd059691-6c0c-4f5b-8fec-ee77823a17ef)
### Admin Center
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/64aba06e-5a5d-4999-9ed8-4c29faa7bb0c)
### Update Company Profile
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/d00d65fa-65c4-4add-83d4-c0b2e2ffb7a2)

### Manage Members
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/baee65d6-2b9d-4fef-876f-3bbff6524f59)

View a member's profile:
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/8544727d-0528-4aec-979a-3207b1427b25)
 
 Modify a subscription of a member:
 ![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/176720ad-37da-4646-9d45-3d3e483bf87f)

Add a subscription for a member:
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/8e05e747-e61c-4272-9067-7c27616c8b06)

Modify a member's profile:
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/de0213b7-5561-40f7-af54-7d0a5d8ada19)

Delete a member:
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/6601bb1b-4804-474e-84a2-fc5ea14c7c60)

### Directly Add a Subscription
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/508ceff3-72b7-4d07-baa9-b853a7ef2d3a)

### Directly Update a Subscription
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/6353a867-6443-4f81-ab99-13b3651a34ad)

### View All Subscriptions
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/26b88475-7407-4be1-b513-33e6c60866d2)

### Get an Email of Statistical Report
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/9cc79c98-4b8c-4e0f-a41a-7715f20b236d)

Email Received:
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/c6b403d4-2211-4276-ba17-74986f32a3ef)

### Send Email Reminder to Members
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/521b574e-084b-4c94-94c6-3ca926904641)

Email Received:
![image](https://github.com/everssun/4156_final_project_client_app/assets/30332629/a644ce4d-6f31-487f-9a0f-e4db5f502199)





