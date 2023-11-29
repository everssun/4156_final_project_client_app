$(document).ready(function(){
    var tempdata = {}
    var b1=false
    var b2=false
    var b3=false
    var b4=false
    var b5=false
    $("#e3").click(function(){
        $("#d3").append('<br>')
        $("#d3").append('<input id="i3" type="text" placeholder="#NEW Subscription Type"/>')
        b1=true
    })
        
    $("#e4").click(function(){
        let newline = $("<input>").attr('type', "text")
        newline.attr('placeholder', "#NEW Subscription Status")
        newline.attr('id', 'i4')
        $("#d4").append('<br>')
        $("#d4").append(newline)
        b2=true
    })

    $("#e5").click(function(){
        $("#d5").append('<br>')
        $("#d5").append('<input id="i5" type="text" placeholder="#NEW Next Due Date"/>')
        b3=true
    })

    $("#e6").click(function(){
        $("#d6").append('<br>')
        $("#d6").append('<input id="i6" type="text" placeholder="#NEW Start Date"/>')
        b4=true
    })

    $("#e7").click(function(){
        $("#d7").append('<br>')
        $("#d7").append('<input id="i7" type="text" placeholder="#NEW Billing Info"/>')
        b5=true
    })

    $("#final_submit2").click(function(){
        if (b1==true){
            tempdata["subtype"]=$("#i3").val()
        }else{
            tempdata["subtype"]=$("#s3").html()
        }
        if (b2==true){
            tempdata["substa"]=$("#i4").val()
        }else{
            tempdata["substa"]=$("#s4").html()
        }
        if (b3==true){
            tempdata["nddate"]=$("#i5").val()
        }else{
            tempdata["nddate"]=$("#s5").html()
        }
        if (b4==true){
            tempdata["sdate"]=$("#i6").val()
        }else{
            tempdata["sdate"]=$("#s6").html()
        }
        if (b5==true){
            tempdata["binfo"]=$("#i7").val()
        }else{
            tempdata["binfo"]=$("#s7").html()
        }
        // console.log($("#s5").text())
        // console.log(tempdata["awards"])
        tempdata["id"]=$("#final_submit2").attr('name')
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
                window.location.href = "/view_subs/"+result["id_edit"]
            },
            error: function(request, status, error){
                console.log("Error");
                console.log(request)
                console.log(status)
                console.log(error)
            }
        });
        
    })

    $("#discard2").click(function(){
        var discard = confirm("Are you sure?")
        if (discard == true){
            window.location.href = "/view_subs/"+$("#discard2").attr('name')
        }
        
    })

})