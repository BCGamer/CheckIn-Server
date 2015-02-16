$(function(){
    var ready2lanMessage = "Good to go.";

    var $initialDownloadBtn = $("#initial-download"),
        $verificationDiv = $("#verification-download"),
        $pleaseWaitDiv = $("#please-wait-div"),
        $resultsDiv = $("#results-div"),
        $firewall = $("#firewall-status"),
        $dhcp = $("#dhcp-status"),
        $antivirus = $("#antivirus-status"),
        $connectingDiv = $("#connecting-div");

    var previousResult = {};
    var connectingIID =  "";

    var ready2lan = false
    var hasIPChangedIID

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

        if((results.firewall)&&(results.dhcp)&&(results.antivirus)){
            ready2lan = true
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
        if(ready2lan){
            clearInterval(checkVerificationIID);
            checkConnection();
        }else{
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
    }

    function checkConnection(){
        // Hide everything after 3 seconds
        // Show spinner gif
        setTimeout(function(){
            $resultsDiv.hide(600);
            $initialDownloadBtn.hide(600);
            $verificationDiv.hide(600);
            $pleaseWaitDiv.hide(600);
            $connectingDiv.show(600);
        }, 3000);

        setInterval(hasIPChanged, 1000)

        //setTimeout(function() {
        //    window.location.replace("http://checkin.bcgamer.lan/verified");
        //}, 15000);
    }

    function hasIPChanged(){
        $.ajax({
                url: '/verify/checkip/',
                type: 'GET',
                success: function(data){
                    // If there is a response
                    if(data){
                        // Check if browser and user match
                        //if(data.browser != data.user){
                        if(data.ip_address_changed){
                            clearInterval(hasIPChangedIID);
                            window.location.replace("http://checkin.bcgamer.lan/verified");
                        }
                    }
                }
            });
    }

    var checkVerificationIID = setInterval(checkVerification, 1000);
});