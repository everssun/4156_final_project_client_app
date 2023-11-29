$(document).ready(function(){
    var tempdata = {}
    var b1=false
    var b2=false
    $("#e1").click(function(){
        $("#d1").append('<br>')
        $("#d1").append('<input id="i1" type="text" placeholder="#NEW name"/>')
        b1=true
    })
        
    $("#e2").click(function(){
        let newline = $("<input>").attr('type', "text")
        newline.attr('placeholder', "#NEW email")
        newline.attr('id', 'i2')
        $("#d2").append('<br>')
        $("#d2").append(newline)
        b2=true
    })

    $("#final_submit1").click(function(){
        if (b1==true){
            tempdata["name"]=$("#i1").val()
        }else{
            tempdata["name"]=$("#s1").html()
        }
        if (b2==true){
            tempdata["email"]=$("#i2").val()
        }else{
            tempdata["email"]=$("#s2").html()
        }
        // console.log($("#s5").text())
        // console.log(tempdata["awards"])
        tempdata["id"]=$("#final_submit1").attr('name')
        //console.log(tempdata)
        $.ajax({
            type: "POST",
            url: "save_edit",                
            dataType : "json",
            contentType: "application/json; charset=utf-8",
            data : JSON.stringify(tempdata),
            success: function(result){
                let all_data = result["data"]
                console.log(result)
                data = all_data
                window.location.href = "/view_company/"+result["id_edit"]
            },
            error: function(request, status, error){
                console.log("Error");
                console.log(request)
                console.log(status)
                console.log(error)
            }
        });
        
    })

    $("#discard1").click(function(){
        var discard = confirm("Are you sure?")
        if (discard == true){
            window.location.href = "/view_company/"+$("#discard1").attr('name')
        }
        
    })

})