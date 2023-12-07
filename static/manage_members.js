function addHiddenField(form, name, value) {
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    form.appendChild(input);
}

//  ---- For andmin_manage_members.html ----

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


// ---- For member_profile.html ----

function submodifySaveChanges(url, subscription_id, index , email) {
    // Create a form element
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = url;

    // Add hidden input fields
    addHiddenField(form, 'subscription_name', document.getElementById('submodifiedName' + index).value);
    addHiddenField(form, 'subscription_status', document.getElementById('submodifiedStatus' + index).value);
    addHiddenField(form, 'subscription_type', document.getElementById('submodifiedType' + index).value);
    addHiddenField(form, 'start_date', document.getElementById('submodifiedStartDate' + index).value);
    addHiddenField(form, 'next_due_date', document.getElementById('submodifiedDueDate' + index).value);
    addHiddenField(form, 'billing_info', document.getElementById('submodifiedBilling' + index).value);
    addHiddenField(form, 'subscription_id', subscription_id);
    addHiddenField(form, 'email', email);
    addHiddenField(form, 'redirect_url', 'admin_view_member')
    // Append the form to the document and submit it
    document.body.appendChild(form);
    form.submit();
}


function subAddSaveChanges(url, email){
    // Create a form element
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = url;

    // Add hidden input fields
    addHiddenField(form, 'subs_name', document.getElementById('subAddModalName').value);
    addHiddenField(form, 'subs_type', document.getElementById('subAddModalType').value);
    addHiddenField(form, 'subs_sta', document.getElementById('subAddModalStatus').value);
    addHiddenField(form, 'start_date', document.getElementById('subAddModalStartDate').value);
    addHiddenField(form, 'next_date', document.getElementById('subAddModalDueDate').value);
    addHiddenField(form, 'bill_info', document.getElementById('subAddModalBilling').value);
    addHiddenField(form, 'mem_email', email);
    addHiddenField(form, 'change_from_admin', true);

    // Append the form to the document and submit it
    document.body.appendChild(form);
    form.submit();

}

// ---- For view_all_subs.html ----

function allsubmodifySaveChanges(url, subscription_id, index) {
    // Create a form element
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = url;

    // Add hidden input fields
    addHiddenField(form, 'subscription_name', document.getElementById('allsubmodifiedName' + index).value);
    addHiddenField(form, 'subscription_status', document.getElementById('allsubmodifiedStatus' + index).value);
    addHiddenField(form, 'subscription_type', document.getElementById('allsubmodifiedType' + index).value);
    addHiddenField(form, 'start_date', document.getElementById('allsubmodifiedStartDate' + index).value);
    addHiddenField(form, 'next_due_date', document.getElementById('allsubmodifiedDueDate' + index).value);
    addHiddenField(form, 'billing_info', document.getElementById('allsubmodifiedBilling' + index).value);
    addHiddenField(form, 'subscription_id', subscription_id);
    addHiddenField(form, 'email', 'NA'); // placeholder
    addHiddenField(form, 'redirect_url', 'view_all_subs');
    // Append the form to the document and submit it
    document.body.appendChild(form);
    form.submit();
}

// ---- For notification_center.html ----
function sendEmailReminder(url) {
    console.log("js func called")
    window.location.href = url;
}

// ---- For member_center.hrml ----
function membersubmodifySaveChanges(url, subscription_id, index) {
    // Create a form element
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = url;

    // Add hidden input fields
    addHiddenField(form, 'subscription_status', document.getElementById('membersubmodifiedStatus' + index).value);
    addHiddenField(form, 'billing_info', document.getElementById('membersubmodifiedBilling' + index).value);
    addHiddenField(form, 'subscription_id', subscription_id);
    // Append the form to the document and submit it
    document.body.appendChild(form);
    form.submit();
}