/**
 * Created by dobbyn_a on 12/23/2014.
 */
$(function(){

});

$('#id_age_under_18').change(function(){
    // Initial Hide
    if(this.checked){
        $('#div_id_guardian_name').show("slow");
        $('#div_id_guardian_phone').show("slow");
        $('#waiver_parental').show("slow");
    }else{
        $('#div_id_guardian_name').hide("slow");
        $('#div_id_guardian_phone').hide("slow");
        $('#waiver_parental').hide("slow");
    }
    isValid()
});

$('#id_waiver_signed').change(function(){
    isValid()
});

$('#id_guardian_name').change(function(){
    isValid()
});

$('#id_guardian_phone').change(function(){
    isValid()
});

/*
When 'id_waiver_signed' checkbox is checked:
 1. If 'id_age_under_18' isn't checked, enable the submit button
 2. If 'id_age_under_18' is checked and 'id_guardian_name' and
    'id_guardian_phone' are filled, enable the submit button
 3. Else disable the submit button
*/
function isValid(){
    var $waiver_signed = document.getElementById("id_waiver_signed");
    var $under_18 = document.getElementById("id_age_under_18");
    var $guardian_name = document.getElementById("id_guardian_name");
    var $guardian_phone = document.getElementById("id_guardian_phone");

    if(($waiver_signed).checked && !($under_18).checked){
        $('#id_submit_button').prop('disabled',false);
    }
    else if(($waiver_signed).checked && ($under_18).checked && true){
        if(($guardian_name.value != '') && ($guardian_phone.value != '')){
            $('#id_submit_button').prop('disabled',false);
        }
        else{
            $('#id_submit_button').prop('disabled',true);
        }
    }
    else{
        $('#id_submit_button').prop('disabled',true);
    }
}