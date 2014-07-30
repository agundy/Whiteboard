var edit_assignment_type = function(assignment_type){
    var input_name = document.getElementById(assignment_type+'-edit-name');
    input_name.style.display='block';
    var input_weight = document.getElementById(assignment_type+'-edit-weight');
    input_weight.style.display='block';

    var weight = document.getElementById(assignment_type+'-show-name').style.display='none';
    var weight = document.getElementById(assignment_type+'-show-weight').style.display='none';
}

var save_assignment_type = function(assignment_type,assignment_type_pk,request){
    // Get the values of the input fields
    var new_name = document.getElementById(assignment_type+'-name-input').value;
    var new_weight = document.getElementById(assignment_type+'-weight-input').value;
    // Set the url based on the assignment type we are editing
    var url = "/student/edit_assignment_type/"+assignment_type_pk;
    // Save the data to a dictionary and send via POST  
    data = {csrfmiddlewaretoken:request,'weight':new_weight,'name':new_name};
    $.post(url,data);
    // Hide the input fields and show the labels
    document.getElementById(assignment_type+'-edit-name').style.display='none';
    document.getElementById(assignment_type+'-edit-weight').style.display='none';
    document.getElementById(assignment_type+'-show-name').style.display='block';
    document.getElementById(assignment_type+'-show-weight').style.display='block';
    var weight = document.getElementById(assignment_type+'-show-weight');
    var name = document.getElementById(assignment_type+'-name');
    weight.style.display = 'block';
    weight.innerHTML = new_weight;
    name.style.display = 'block';
    name.innerHTML = new_name;
}