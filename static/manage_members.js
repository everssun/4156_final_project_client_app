function modifySaveChanges(url, email, index) {
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

function confirmDelete(url, email){
    var result = confirm("Are you sure you want to delete this member?");
    console.log(url)
    if (result) {
        // Create a form dynamically
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = url;

        addHiddenField(form, 'email', email);

        // Append the form to the body and submit it
        document.body.appendChild(form);
        form.submit();
    }
}

function addHiddenField(form, name, value) {
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    form.appendChild(input);
}