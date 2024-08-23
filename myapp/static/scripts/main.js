function getNewData() {
    const url = "/get_data_about_user/";
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
            // Update the content on the page with the received HTML
            $('#coins_per_tap').text("+" + response.efficiencypertap);
            let cpt = response.efficiencypertap
            window.cpt = cpt
            $('.userNameContainer').text(response.user);
            $('#energy_limit_level').text(response.energy_limit_level_digits);
            $('#level').text(response.userlevelname);
            let walletAmount = parseFloat(response.new_wallet).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            $('#wallet').text(walletAmount);
            $('#energy').text(response.new_energy);
            $('#level_count').text(response.new_level);
            window.level_count = response.new_level
        },
        error: function(response){
            alert('Error loading content');
        }
    });
}
window.addEventListener('load', function() {
    sessionStorage.clear(); // Очищаем sessionStorage при загрузке страницы
});

(function () {
    const bonusUrl = "/get_bonus/";
    const claimUrl = "/get_daily_bonus_into_wallet/";
    let claimBubblesContainer = $('.claimBubblesContainer');
    let username = $('body').data('username');
    let csrfToken = $('body').data('csrftoken');

    function startTimer(duration, display, onComplete) {
        let timer = duration, hours, minutes;
        const interval = setInterval(function () {
            hours = Math.floor(timer / 3600);
            minutes = Math.floor((timer % 3600) / 60);

            let timeString = '';
            if (hours > 0) {
                timeString += hours + 'h ';
            }
            timeString += minutes + 'm';

            display.text(timeString);

            if (--timer < 0) {
                clearInterval(interval);
                if (onComplete && typeof onComplete === 'function') {
                    onComplete(); // Execute the callback function when the timer finishes
                }
            }
        }, 1000);
    }

    function parseTime(timeString) {
        // Split into hours and the fractional part
        let [hours, fraction] = timeString.split('.');
        hours = parseInt(hours, 10);
        let minutes = Math.round(parseFloat('0.' + fraction) * 60);
        return (hours * 3600) + (minutes * 60);
    }

    function displayProgress(response) {
        claimBubblesContainer.empty();
        claimBubblesContainer.append(`
            <div class="claimBubblesProgress">
                <div class="farmingInfo">
                    <div class="farmingText">Farming</div>
                    <div class="progressCount">B ${(response.income_per_hour).toFixed(3)}</div>
                </div>
                <div class="timerInfo" id="timerInfo"></div>
            </div>
        `);

        const timeUntilActive = parseTime(response.time_until_active.toFixed(2));
        let timerInfo = $('#timerInfo');
        let progressCount = $('.progressCount');
        let tokensEarned = parseFloat(progressCount.text().replace('B ', '')) || 0; // Initialize with the current value

        startTimer(timeUntilActive, timerInfo, function () {
            claimBubblesContainer.empty();
            claimBubblesContainer.append(`
                <div class="claimBubbles">Claim</div>
            `);
            $('.claimBubbles').on('click', claimPrize);
        });

        // Update token count every minute
        const updateTokenCount = setInterval(function () {
            $.ajax({
                url: bonusUrl,
                method: "POST",
                data: {
                    'username': username,
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function (response) {
                    const incomePerHour = parseFloat(response.income_per_hour);
                    const tokenIncrementPerMinute = incomePerHour / 60;
                    tokensEarned += tokenIncrementPerMinute;
                    progressCount.text(`B ${(tokensEarned).toFixed(3)}`);
                },
                error: function () {
                    alert('Error fetching updated income_per_hour');
                }
            });
        }, 60000); // 60000 milliseconds = 1 minute

        // Stop the interval when the timer finishes
        setTimeout(function() {
            clearInterval(updateTokenCount);
        }, timeUntilActive * 1000);
    }

    function claimPrize() {
        $.ajax({
            url: claimUrl,
            method: "POST",
            data: {
                'username': username,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function () {
                // After successfully claiming the prize, fetch updated data from /get_bonus/
                $.ajax({
                    url: bonusUrl,
                    method: "POST",
                    data: {
                        'username': username,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (response) {
                        displayProgress(response);
                        getNewData()
                    },
                    error: function () {
                        alert('Error loading updated content');
                    }
                });
            },
            error: function () {
                alert('Error claiming prize');
            }
        });
    }

    // Initial load of bonus data
    $.ajax({
        url: bonusUrl,
        method: "POST",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            if (response.status) {
                claimBubblesContainer.empty();
                claimBubblesContainer.append(`
                    <div class="claimBubbles">Claim</div>
                `);
                $('.claimBubbles').on('click', claimPrize);
            } else {
                displayProgress(response);
            }
        },
        error: function(){
            alert('Error loading content');
        }
    });
})();

console.log(sessionStorage.getItem('miningCardHandlerSetUp'))
$(document).ready(function () {
    // Проверяем, установлен ли already флаг сессии
    if (sessionStorage.getItem('miningCardHandlerSetUp') === null) {
        // Если нет, устанавливаем значение
        sessionStorage.setItem('miningCardHandlerSetUp', 'false');
    }
});
$(document).ready(function () {
    sessionStorage.setItem('currentTab', 'firstCat')
    console.log(sessionStorage.getItem('currentTab'))
})

$('.miningClaimButton').click(function () {
    $(this).css({
        transform: 'scale(0.9)',
        transition: 'opacity 0.4s ease, transform 0.4s ease'
    });

    setTimeout(() => {
        $(this).css({
            transform: 'scale(1)'
        });
    }, 100);
    const url = "/get_mining_bonus_into_wallet/"
    let username = $('body').data('username');
    let csrfToken = $('body').data('csrftoken');
    $.ajax({
        url: url,
        method: "POST",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function (response) {
            $('.miningCountDigits').text('0');
            getNewData()
        },
        error: function (response) {
            alert('Error loading content');
        }
    });
})

function setupBuyMiningCardHandler() {
    // Check if the handler has already been set up
    if (sessionStorage.getItem('miningCardHandlerSetUp') === 'true') {
        return; // Exit the function if it's already set
    }

    // Define the flag for in-progress requests
    let isRequestInProgress = false;

    // Handler for buying mining cards
    $('body').off('click', '.button').on('click', '.button', function () {
        $(this).animate({
            opacity: 0.5,
            width: "-=10px",
            height: "-=10px"
        }, 100, function() {
            $(this).animate({
                opacity: 1,
                width: "+=20px",
                height: "+=20px"
            }, 100);
        });
        let parentElem = $(this).parent()
        setTimeout(function () {
            parentElem.addClass('hidden')
        }, 200)

        if (isRequestInProgress) {
            return; // Block if there's an ongoing request
        }

        let miningId = $(this).closest('[data-mining]').data('mining');

        isRequestInProgress = true; // Mark the request as in progress

        setTimeout(function() {
            $.ajax({
                url: "/buy_mining_card/",
                method: "POST",
                data: {
                    'username': $('body').data('username'),
                    'mining_id': miningId,
                    'csrfmiddlewaretoken': $('body').data('csrftoken')
                },
                success: function (response) {
                    getNewData();

                    // Обновляем только ту вкладку, на которой пользователь был
                    if (sessionStorage.getItem('currentTab') === 'firstCat') {
                        getMiningCardsListData('/mining_card_1/');
                    } else if (sessionStorage.getItem('currentTab') === 'secondCat') {
                        getMiningCardsListData('/mining_card_2/');
                    } else if (sessionStorage.getItem('currentTab') === 'thirdCat') {
                        getMiningCardsListData('/mining_card_3/');
                    } else if (sessionStorage.getItem('currentTab') === 'fourthCat') {
                        getMiningCardsListData('/mining_card_4/');
                    }
                },
                error: function () {
                    alert('Покупка не удалась. Недостаточно средств или достигнут максимальный уровень.');
                },
                complete: function() {
                    isRequestInProgress = false; // Сбрасываем флаг
                }
            });
        }, 500); // Задержка в 500 мс перед выполнением AJAX-запроса
    });

    // Mark the handler as set up in session storage
    sessionStorage.setItem('miningCardHandlerSetUp', 'true');
}

$(document).ready(function () {
    // Call getNewData immediately to initialize data and synchronize with server
    getNewData();

    $('#game').click(function () {
        const url = "/load_main_page/";
        $.ajax({
            url: url,
            method: "GET",
            success: function(response){
                // Update the content on the page with the received HTML
                $('#dynamicContent').html(response);
                getNewData(); // Synchronize with server on game page load
            },
            error: function(response){
                alert('Error loading content');
            }
        });
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
                getNewData(); // Synchronize with server on friends page load
            },
            error: function(response){
                alert('Error loading content');
            }
        });
    });

    $('.wheelPage').click(function () {
        const url = "/load_wheel_page/";
        $.ajax({
            url: url,
            method: "GET",
            success: function(response){
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
});
Telegram.WebApp.ready();
Telegram.WebApp.expand();
Telegram.WebApp.setSwipeEnabled(false);
