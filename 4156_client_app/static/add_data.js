
function save_data(){
    let n = $("#name").val();
    let r = $("#rate").val();
    let i = $("#image").val();
    let d = $("#des").val();
    let a = $("#award").val();
    let data_to_save = {"name": n, "image": i, "summary": d, "rating": r, "awards": a}
    $.ajax({
        type: "POST",
        url: "save_data",                
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

    $("#submit").click(function(){
        if ($("#name").val()=="" && $("#rate").val()==""){
            alert("name and rating cannot be empty")
        }
        else if ($("#name").val()=="" && $("#rate").val()!=""){
            alert("name cannot be empty")
        }
        else if ($("#name").val()!="" && $("#rate").val()==""){
            alert("rating cannot be empty")
        }
        else if (!parseInt($("#rate").val())){
            alert("rating should be a NUMBER!!!")
        }
        else if (parseInt($("#rate").val()) && $("#rate").val()>=100){
            alert("rating should not exceed 100")
        }
        else{
            save_data()            
            $("#name").val("");
            $("#rate").val("");
            $("#image").val("");
            $("#des").val("");
            $("#award").val("");
        }
        
    })

})