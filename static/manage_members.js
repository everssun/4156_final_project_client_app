function modifySaveChanges(url, email, index) {
//     var modifiedFirstName = document.getElementById('modifiedFirstName' + index).value;
//     var modifiedLastName = document.getElementById('modifiedLastName' + index).value;
//     var modifiedPhoneNumber = document.getElementById('modifiedPhoneNumber' + index).value;
//     console.log(modifiedFirstName)
//     console.log(modifiedLastName)
//     console.log(modifiedPhoneNumber)

//    // Construct the data you want to send in the request body
//    var requestData = {
//         first_name: modifiedFirstName,
//         last_name: modifiedLastName,
//         email: email,
//         phone_number: modifiedPhoneNumber
//     };

//     // Get the JWT token from wherever you store it (e.g., localStorage)
//     var jwtToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI1NzM1NjEsImlzcyI6IlN1Yk1hbmFnZXIiLCJzdWIiOiIyMSJ9.gPSQ91ze5GL4CkCE_sRWyPoQRRcEuQsogoQEJ9cxeQs"


//     // Construct the headers for the request
//     var headers = new Headers({
//         'Content-Type': 'application/json',
//         'Authorization': 'Bearer ' + jwtToken
//     });

//     // Construct the request options
//     var requestOptions = {
//         method: 'PATCH', 
//         headers: headers,
//         body: JSON.stringify(requestData),
        
//     };

//     // Replace 'your_service_url' with the actual URL of your service
//     var serviceUrl = 'http://localhost:3000/admin/member/changeMemberInfo';

//     // Send the fetch request
//     fetch(serviceUrl, requestOptions)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.content;
//         })
//         .then(data => {
//             // Handle the response data as needed
//             console.log('Response from the server:', data);
//         })
//         .catch(error => {
//             console.error('Error during fetch operation:', error);
//         })
//         .finally(() => {
//             // Close the modal
//             $('#modifyModal' + index).modal('hide');
//         });

     // Create a form element
     var form = document.createElement('form');
     form.method = 'POST';
     form.action = url;
 
     // Add hidden input fields
     addHiddenField(form, 'first_name', document.getElementById('modifiedFirstName' + index).value);
     addHiddenField(form, 'last_name', document.getElementById('modifiedLastName' + index).value);
     addHiddenField(form, 'phone_number', document.getElementById('modifiedPhoneNumber' + index).value);
     addHiddenField(form, 'email', email);
 
     // Append the form to the document and submit it
     document.body.appendChild(form);
     form.submit();
}

function addHiddenField(form, name, value) {
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    form.appendChild(input);
}
