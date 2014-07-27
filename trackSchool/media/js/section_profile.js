var edit_assignment_type = function(assignment_type){
    var input = document.getElementById(assignment_type).style.display='block';
    var weight = document.getElementById(assignment_type+'-weight').style.display='none';
}

var save_assignment_type = function(assignment_type,assignment_type_pk,request){
    var new_weight = document.getElementById(assignment_type+'-input').value;
    var url = "/student/edit_assignment_type/"+assignment_type_pk;
    data = {csrfmiddlewaretoken:request,'weight':new_weight};
    console.log(request);
    console.log(data);
    $.post(url,data);
    var input = document.getElementById(assignment_type).style.display='none';
    var weight = document.getElementById(assignment_type+'-weight');
    weight.style.display='block';
    weight.innerHTML = new_weight;
}