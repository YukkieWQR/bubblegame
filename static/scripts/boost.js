function getNewData() {
    const url = "/get_data_about_user/"
    let username = $('body').data('username');
    let csrfToken = $('body').data('csrftoken');
    $.ajax({
        url: url,
        method: "POST",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response){
            // Update content on the page with the received HTML
            $('#coins_per_tap').text("+" + response.efficiencypertap);
            $('.userName').text(response.user);
            $('#energy_limit_level').text(response.energy_limit_level_digits);
            $('#level').text(response.userlevelname);

            // Format wallet amount with spaces for thousands separator
            let walletAmount = parseFloat(response.new_wallet).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
            $('#wallet').text(walletAmount);

            $('#energy').text(response.new_energy);
            $('#level_count').text(response.new_level);
            $('#multitap_cost').text(response.next_multitap_upgrade_cost);
            $('#multitap_cost_full').text(response.next_multitap_upgrade_cost);
            $('#energyLimit_cost').text(response.next_energy_upgrade_cost);
            $('#energyLimit_cost_full').text(response.next_energy_upgrade_cost);
            $('#energyLimit_lvl').text(response.next_multitap_level);
            $('#multitap_lvl').text(response.next_energy_level);
        },
        error: function(response){
            alert('Error loading content');
        }
    });
}

$(document).ready(function () {
    $('.button3').click(function(){
        const url = "/purchase_multitap/"
        let username = $('body').data('username');
        let csrfToken = $('body').data('csrftoken');
        $.ajax({
            url: url,
            method: "POST",
            data: {
                'username': username,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response){
                let walletAmount = parseFloat(response.new_wallet).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
                $('#wallet').text(walletAmount);

                $('#multitap_level').text(response.new_multitap_level);
                $('#tap_efficiency').text(response.new_tap_efficiency);
            },
            error: function(response){
                alert(response.responseJSON.error);
            }
        });
    });
})

$(document).ready(function () {
    $('.button4').click(function(){
        const url = "/purchase_energy_limit/"
        let username = $('body').data('username');
        let csrfToken = $('body').data('csrftoken');
        $.ajax({
            url: url,
            method: "POST",
            data: {
                'username': username,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response){
                let walletAmount = parseFloat(response.new_wallet).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
                $('#wallet').text(walletAmount);

                $('#energy_limit_level').text(response.new_energy_limit_level);
                $('#energy').text(response.new_energy);
            },
            error: function(response){
                alert(response.responseJSON.error);
            }
        });
    });
})

$(document).ready(function (){
    $('#game').click(function (){
        const url = "/load_main_page/"
        $.ajax({
            url: url,
            method: "GET",
            success: function(response){
                // Обновление контента на странице с полученным HTML
                $('#dynamicContent').html(response);
                getNewData()
            },
            error: function(response){
                alert('Error loading content');
            }
        });
    })
});

$('#mine').click(function () {
    const url = "/load_mine_page/";
    $.ajax({
        url: url,
        method: "GET",
        success: function(response){
            // Update the content on the page with the received HTML
            $('#dynamicContent').html(response);
            getNewData();
        },
        error: function(response){
            alert('Error loading content');
        }
    });
});

$('.friends').click(function () {
    const url = "/load_friends_page/";
    $.ajax({
        url: url,
        method: "GET",
        success: function(response){
            // Update the content on the page with the received HTML
            $('#dynamicContent').html(response);
            getNewData();
        },
        error: function(response){
            alert('Error loading content');
        }
    });
});

$('.tasks').click(function () {
    const url = "/load_tasks_page/";
    $.ajax({
        url: url,
        method: "GET",
        success: function(response){
            // Update the content on the page with the received HTML
            $('#dynamicContent').html(response);
            getNewData(); // Synchronize with server on friends page load
            taskList()
            bonusEligible()
        },
        error: function(response){
            alert('Error loading content');
        }
    });
});

$('.airdrop').click(function () {
    const url = "/load_airdrop_page/";
    $.ajax({
        url: url,
        method: "GET",
        success: function(response){
            // Update the content on the page with the received HTML
            $('#dynamicContent').html(response);
            getNewData(); // Synchronize with server on friends page load
        },
        error: function(response){
            alert('Error loading content');
        }
    });
});
$(document).ready(function () {
        let turbo = document.getElementById('turbo');
        let fullEnergy = document.getElementById('fullEnergy');
        let Multitap = document.getElementById('Multitap');
        let energyLimit = document.getElementById('energyLimit');
        let menu1 = document.getElementsByClassName('menu1');
        let menu2 = document.getElementsByClassName('menu2');
        let menu3 = document.getElementsByClassName('menu3');
        let menu4 = document.getElementsByClassName('menu4');
        let closeButton1 = document.getElementById('closeButton1')
        let closeButton2 = document.getElementById('closeButton2')
        let closeButton3 = document.getElementById('closeButton3')
        let closeButton4 = document.getElementById('closeButton4')

    turbo.addEventListener('click', function() {
        menu1[0].classList.toggle('hidden');
    });
    fullEnergy.addEventListener('click', function() {
        menu2[0].classList.toggle('hidden');
    });
    Multitap.addEventListener('click', function() {
        menu3[0].classList.toggle('hidden');
    });
    energyLimit.addEventListener('click', function() {
        menu4[0].classList.toggle('hidden');
    });

    closeButton1.addEventListener('click', function() {
        menu1[0].classList.add('hidden');
    });
    closeButton2.addEventListener('click', function() {
        menu2[0].classList.add('hidden');
    });
    closeButton3.addEventListener('click', function() {
        menu3[0].classList.add('hidden');
    });
    closeButton4.addEventListener('click', function() {
        menu4[0].classList.add('hidden');
    });
    }
)