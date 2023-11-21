function save_data_company(){
    let n = $("#cname").val();
    let e = $("#email").val();
    let data_to_save = {"cname": n, "email": e}
    $.ajax({
        type: "POST",
        url: "save_data_company",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data_to_save),
        success: function(result){
            let all_data = result["data"]
            console.log(all_data)
            console.log(result)
            console.log(result["id_add"])
            data = all_data

            let newline = $("<div>").addClass("size")
            newline.text("New item successfully created!")
            $("#success").append(newline)
            let newl = $("<div>").addClass("navbar-nav")
            let aa = $("<a>").addClass("nav-link")
            aa.text("See it here")
            //aa.attr('href', "/view/"+add)
            aa.attr('href', "/view/"+result["id_add"])
            newl.append(aa)
            $("#success").append(newl)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

function save_data_subscription(){
    let n = $("#cid").val();
    let r = $("#subtype").val();
    let i = $("#substa").val();
    let d = $("#nddate").val();
    let a = $("#sdate").val();
    let b = $("#binfo").val();
    let data_to_save = {"cid": n, "subtype": i, "substa": d, "nddate": r, "sdate": a, "binfo": b}
    $.ajax({
        type: "POST",
        url: "save_data_subscription",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data_to_save),
        success: function(result){
            let all_data = result["data"]
            console.log(all_data)
            console.log(result)
            console.log(result["id_add"])
            data = all_data

            let newline = $("<div>").addClass("size")
            newline.text("New item successfully created!")
            $("#success").append(newline)
            let newl = $("<div>").addClass("navbar-nav")
            let aa = $("<a>").addClass("nav-link")
            aa.text("See it here")
            //aa.attr('href', "/view/"+add)
            aa.attr('href', "/view/"+result["id_add"])
            newl.append(aa)
            $("#success").append(newl)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}
var count = 10

$(document).ready(function(){

    $("#submit1").click(function(){
        if ($("#cname").val()=="" && $("#email").val()==""){
            alert("Company name and email cannot be empty")
        }
        else if ($("#cname").val()=="" && $("#email").val()!=""){
            alert("Company name cannot be empty")
        }
        else if ($("#cname").val()!="" && $("#email").val()==""){
            alert("email cannot be empty")
        }
        else{
            save_data_company()            
            $("#cname").val("");
            $("#email").val("");
        }
        
    })

    $("#submit2").click(function(){
        let bool = true;
        if ($("#cid").val()==""){
            alert("Company Id cannot be empty")
            bool = false;
        }
        if ($("#subtype").val()==""){
            alert("Subscription type cannot be empty")
            bool = false;
        }
        if ($("#substa").val()==""){
            alert("Subscription status cannot be empty")
            bool = false;
        }
        if ($("#nndate").val()==""){
            alert("Next due date cannot be empty")
            bool = false;
        }
        if ($("#sdate").val()==""){
            alert("Start date cannot be empty")
            bool = false;
        }
        if (!parseInt($("#cid").val())){
            alert("Company Id should be a NUMBER!!!")
            bool = false;
        }
        if (bool) {
            save_data_subscription()            
            $("#cid").val("");
            $("#subtype").val("");
            $("#substa").val("");
            $("#nddate").val("");
            $("#sdate").val("");
            $("#binfo").val("");
        }
        
    })

})