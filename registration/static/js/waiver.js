

$(function () {

    var $submitButton = $("#id_submit_button");
    var $waiverParental = $("#waiver_parental");
    var $under18Fields = $("#under_18_fields");
    var $waiverSigned = $("#id_waiver_signed");
    var $guardianPhone = $("#id_guardian_phone");
    var $guardianName = $("#id_guardian_name");

    $waiverSigned.on("change", function(e){
        $submitButton.prop("disabled", !canSubmitWaiver());
    });

    $("#id_age_under_18").on("change", function(e){
        if(this.checked){
            $waiverParental.slideDown();
            $under18Fields.slideDown();
        } else {
            $waiverParental.slideUp();
            $under18Fields.slideUp();
        }
        $submitButton.prop("disabled", !canSubmitWaiver());
    });


    $("#id_guardian_phone, #id_guardian_name").on("keydown", function(){
        $submitButton.prop("disabled", !canSubmitWaiver());
    });



    var canSubmitWaiver = function(){

        var under18 = $("#id_age_under_18").prop("checked");
        var guardianPhone = $guardianPhone.val();
        var guardianName = $guardianName.val();

        if( !$waiverSigned.prop("checked") ){
            return false
        }

        if( under18 ){
            if( guardianName != '' && guardianPhone != ''){
                return true
            }
        } else {
            return true
        }


        return false;
    }

});