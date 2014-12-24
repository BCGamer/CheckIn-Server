$(function(){
    var ready2lanMessage = "Good to go.";

    var $initialDownloadBtn = $("#initial-download"),
        $verificationDiv = $("#verification-download"),
        $pleaseWaitDiv = $("#please-wait-div"),
        $resultsDiv = $("#results-div"),
        $firewall = $("#firewall-status"),
        $dhcp = $("#dhcp-status"),
        $antivirus = $("#antivirus-status");

    var previousResult = {};

    $initialDownloadBtn.on("click", function(){
        $verificationDiv.slideUp(500, function(){
            $pleaseWaitDiv.slideDown(500);

            //setTimeout(showVerificationResults, 6000);
        });
    });

    function showVerificationResults(results){
        if(!results) results = {}

        var firewallStatus = 'danger',
            antivirusStatus = 'danger',
            dhcpStatus = 'danger';

        var firewallMessage = 'Error with firewall',
            antivirusMessage = 'Error with antivirus',
            dhcpMessage = 'Error with DHCP';

        if(results.firewall){
            firewallMessage = ready2lanMessage;
            firewallStatus = 'success';
        } else {
            if(results.errors && results.errors.firewall){
                firewallMessage = results.errors.firewall;
            }
        }

        if(results.dhcp){
            dhcpMessage = ready2lanMessage;
            dhcpStatus = 'success';
        } else {
            if(results.errors && results.errors.dhcp){
                dhcpMessage = results.errors.dhcp;
            }
        }

        if(results.antivirus){
            antivirusMessage = ready2lanMessage;
            antivirusStatus = 'success';
        } else {
            if(results.errors && results.errors.antivirus){
                antivirusMessage = results.errors.antivirus;
            }
        }

        showSettingStatus($firewall, firewallStatus, firewallMessage);
        showSettingStatus($antivirus, antivirusStatus, antivirusMessage);
        showSettingStatus($dhcp, dhcpStatus, dhcpMessage);

        $pleaseWaitDiv.hide(600, function(){
            $resultsDiv.show(600);
        });
    }

    function showSettingStatus($container, status, message){
        $(".message", $container).text(message);
        $container.removeClass("alert-danger alert-success").addClass("alert-"+status);
    }


    function checkVerification(){

        $.ajax({
            url: '/verify/check/',
            type: 'GET',
            success: function(data){
                if(data.verification_received){
                    if(JSON.stringify(data) !== JSON.stringify(previousResult)){
                        showVerificationResults(data);
                    }
                    previousResult = data;
                }
            }
        });

    }

    setInterval(checkVerification, 1000);

});



