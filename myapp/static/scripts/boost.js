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
            $('.userNameContainer').text(response.user);
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
function dailyEnergyBonusEligible() {
    const url = "/daily_energy_bonus_eligibility/"
    let username = $('body').data('username');
    let csrfToken = $('body').data('csrftoken');
    const button2 = $('.button2');
    const menu2 = $('.menu2');
    $.ajax({
        url: url,
        method: "POST",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function (response) {
            if (response.bonus_eligible === false) {
                button2.remove();
                menu2.append(`<div id="notButton">Come back tomorrow for a new bonus!</div>`)
            }
        },
        error: function (response) {
            alert('Error loading content');
        }
    })
}
function dailyTurboBonusEligible() {
    const url = "/daily_turbo_bonus_eligibility/"
    let username = $('body').data('username');
    let csrfToken = $('body').data('csrftoken');
    const button1 = $('.button1');
    const menu1 = $('.menu1');
    $.ajax({
        url: url,
        method: "POST",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function (response) {
            if (response.bonus_eligible === false) {
                button1.remove();
                menu1.append(`<div id="notButton" ">Come back tomorrow for a new bonus!</div>`)
            }
        },
        error: function (response) {
            alert('Error loading content');
        }
    })
}
$(document).ready(function () {
    const url = "/get_mining_bonus/"
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
            let walletAmount = parseFloat(response.bonus).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
            $('.miningCountDigits').text(walletAmount)
            function formatMiningAmount(amount) {
                const parsedAmount = parseFloat(amount);

                if (parsedAmount >= 1000000) {
                    return (parsedAmount / 1000000).toFixed(1) + 'M'; // Для миллионов
                } else if (parsedAmount >= 100000) {
                    return (parsedAmount / 1000).toFixed(0) + 'K'; // Для тысяч
                } else {
                    return parsedAmount.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " "); // Обычный форматирование
                }
            }

            let miningAmount = formatMiningAmount(response.income_per_hour);

            $('#coins_per_hour').text("+" + miningAmount);
        },
        error: function(response){
            alert('Error loading content');
        }
    });
})
$(document).ready(function () {
    $('.button1').click(function(){
        $(this).animate({
            opacity: 0.5,
            width: "-=10px",
            height: "-=10px"
        }, 100, function() {
            $(this).animate({
                opacity: 1,
                width: "+=10px",
                height: "+=10px"
            }, 100);
        });
        const url = "/daily_turbo/"
        let username = $('body').data('username');
        let csrfToken = $('body').data('csrftoken');
        let menu1 = document.getElementsByClassName('menu1');
        $.ajax({
            url: url,
            method: "POST",
            data: {
                'username': username,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response){
                getNewData()
                menu1[0].classList.add('hidden');
            },
            error: function(response){
                alert(response.responseJSON.error);
                menu1[0].classList.add('hidden');
            }
        });
    });
})
$(document).ready(function () {
    $('.button2').click(function(){
        $(this).animate({
            opacity: 0.5,
            width: "-=10px",
            height: "-=10px"
        }, 100, function() {
            $(this).animate({
                opacity: 1,
                width: "+=10px",
                height: "+=10px"
            }, 100);
        });
        const url = "/daily_energy/"
        let username = $('body').data('username');
        let csrfToken = $('body').data('csrftoken');
        let menu2 = document.getElementsByClassName('menu2');
        $.ajax({
            url: url,
            method: "POST",
            data: {
                'username': username,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response){
                getNewData()
                menu2[0].classList.add('hidden');
            },
            error: function(response){
                alert(response.responseJSON.error);
                menu2[0].classList.add('hidden');
            }
        });
    });
})
$(document).ready(function () {
    $('.button3').click(function(){
        $(this).animate({
            opacity: 0.5,
            width: "-=10px",
            height: "-=10px"
        }, 100, function() {
            $(this).animate({
                opacity: 1,
                width: "+=10px",
                height: "+=10px"
            }, 100);
        });
        const url = "/purchase_multitap/"
        let username = $('body').data('username');
        let csrfToken = $('body').data('csrftoken');
        let menu3 = document.getElementsByClassName('menu3');
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
                menu3[0].classList.add('hidden');
                $('#multitap_level').text(response.new_multitap_level);
                $('#tap_efficiency').text(response.new_tap_efficiency);
            },
            error: function(response){
                alert(response.responseJSON.error);
                menu3[0].classList.add('hidden');
            }
        });
    });
})

$(document).ready(function () {
    $('.button4').click(function(){
        $(this).animate({
            opacity: 0.5,
            width: "-=10px",
            height: "-=10px"
        }, 100, function() {
            $(this).animate({
                opacity: 1,
                width: "+=10px",
                height: "+=10px"
            }, 100);
        });
        const url = "/purchase_energy_limit/"
        let username = $('body').data('username');
        let csrfToken = $('body').data('csrftoken');
        let menu4 = document.getElementsByClassName('menu4');
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
                menu4[0].classList.add('hidden');
                $('#energy_limit_level').text(response.new_energy_limit_level);
                $('#energy').text(response.new_energy);
            },
            error: function(response){
                alert(response.responseJSON.error);
                menu4[0].classList.add('hidden');
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
            $('#dynamicContent').html(response);
            getNewData(); // Synchronize with server
            setupBuyMiningCardHandler(); // Set up the handler here
            sessionStorage.setItem('currentTab', 'firstCat')
            getMiningCardsListData('/mining_card_1/');
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