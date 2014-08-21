var edit_assignment_type = function(assignment_type){
    document.getElementById(assignment_type+"-show-name").style.display='none';
    document.getElementById(assignment_type+'-show-weight').style.display='none';
    document.getElementById(assignment_type+"-edit-name").style.display='block';
    document.getElementById(assignment_type+'-edit-weight').style.display='block';
}

var save_assignment_type = function(assignment_type,assignment_type_pk,request){
    var new_weight = document.getElementById(assignment_type+'-weight-input').value;
    var url = "/student/assignment_type/edit/"+assignment_type_pk;
    data = {csrfmiddlewaretoken: request, weight: new_weight, name: assignment_type};
    $.post(url,data);
    // Make the editing windows invisible
    document.getElementById(assignment_type+"-edit-name").style.display='none';
    document.getElementById(assignment_type+'-edit-weight').style.display='none';
    // Make the show items visible again
    document.getElementById(assignment_type+'-show-name').style.display='block';
    var weight = document.getElementById(assignment_type+'-show-weight');
    weight.style.display = 'block';
    weight.innerHTML = new_weight;
}