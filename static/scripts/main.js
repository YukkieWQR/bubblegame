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
            $('.userName').text(response.user);
            $('#energy_limit_level').text(response.energy_limit_level_digits);
            $('#level').text(response.userlevelname);
            let walletAmount = parseFloat(response.new_wallet).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
            $('#wallet').text(walletAmount);
            $('#energy').text(response.new_energy);
            $('#level_count').text(response.new_level);
            window.level_count = response.new_level
            console.log(window.level_count)
            updateImage();
            updateClickButtonState();
        },
        error: function(response){
            alert('Error loading content');
        }
    });
}
window.addEventListener('load', function() {
    sessionStorage.clear(); // Очищаем sessionStorage при загрузке страницы
});

console.log(sessionStorage.getItem('miningCardHandlerSetUp'))
$(document).ready(function () {
    // Проверяем, установлен ли already флаг сессии
    if (sessionStorage.getItem('miningCardHandlerSetUp') === null) {
        // Если нет, устанавливаем значение
        sessionStorage.setItem('miningCardHandlerSetUp', 'false');
    }
});
function updateMiningCount() {
    let isRequestInProgress = false;  // Флаг для отслеживания состояния запроса

    const fetchMiningBonus = () => {
        if (isRequestInProgress) {
            return; // Если предыдущий запрос еще в процессе, ничего не делаем
        }

        isRequestInProgress = true; // Установка флага, что запрос начался

        const url = "/get_mining_bonus/";
        let username = $('body').data('username');
        let csrfToken = $('body').data('csrftoken');

        $.ajax({
            url: url,
            method: "POST",
            data: {
                'username': username,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                let walletAmount = parseFloat(response.bonus).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
                $('.miningCountDigits').text(walletAmount);
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
            error: function(response) {
            },
            complete: function() {
                isRequestInProgress = false; // Сброс флага, как только запрос завершится
            }
        });
    }

    setInterval(fetchMiningBonus, 5000);
}

$(document).ready(function () {
    updateMiningCount();
});


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
                    getMiningCardsListData();
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





function updateClickButtonState() {
    let energy = parseInt($('#energy').text());
    if (energy < 1) {
        $('.clickButton').prop('disabled', true);
        $('#increment-btn').prop('disabled', true); // Disable the increment button if energy is less than 1
    } else {
        $('.clickButton').prop('disabled', false);
        $('#increment-btn').prop('disabled', false); // Enable the increment button if energy is greater than or equal to 1
    }
}

function incrementEnergy() {
    let energy = parseInt($('#energy').text());
    let energyLimit = parseInt($('#energy_limit_level').text());

    if (energy < energyLimit) {
        $('#energy').text(energy + 1);
        updateClickButtonState();
    }
}

function updateImage() {
    $('.imgButton2').attr('src', `../static/images/!!${window.level_count}-Photoroom.png`);
}

$(".currentPoints").bind("DOMSubtreeModified", function() {
    updateImage();
});

$(document).ready(function () {
    // Call getNewData immediately to initialize data and synchronize with server
    getNewData();

    // Call incrementEnergy every second to increment energy counter
    setInterval(function() {
        incrementEnergy();
    }, 1000);

    $('.activateBoost').click(function () {
        const url = "/load_boost_html/";
        $.ajax({
            url: url,
            method: "GET",
            success: function(response){
                // Update the content on the page with the received HTML
                $('#dynamicContent').html(response);
                getNewData(); // Synchronize with server on boost activation
                dailyEnergyBonusEligible()
                dailyTurboBonusEligible()
            },
            error: function(response){
                alert('Error loading content');
            }
        });
    });

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

    $('.miningClaimButton').click(function () {
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
            success: function(response){
                $('.miningCountDigits').text('0');
                alert('You have successfully claimed your reward!')
                getNewData()
            },
            error: function(response){
                alert('Error loading content');
            }
        });
    })

    $('#increment-btn').click(function () {
        let energy = parseInt($('#energy').text());
        if (energy < 1) {
            alert("Not enough energy to perform this action!");
            return; // Block interaction if energy is less than 1
        }

        const url = "/increment_wallet/";
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
                $('#level').text(response.userlevelname);
                $('#coins_per_tap').text("+" + response.efficiencypertap); // Add "+" here too
                $('#level_count').text(response.level);
                $('#energy_limit_level').text(response.energy_limit_level_digits)

                updateClickButtonState();
            }
        });
    });

    let points = 0;
    function setPoints(newPoints) {
        points = newPoints;
        // Update the points display on the webpage
        $('#pointsDisplay').text(points); // Assuming you have a div with id "pointsDisplay" to display the points
    }

    $(".clickButton").click(function(e) {
        let energy = parseInt($('#energy').text());
        if (energy < 1) {
            return; // Block interaction if energy is less than 1
        }

        var rect = $(this)[0].getBoundingClientRect();
        var x = e.clientX - rect.left - rect.width / 2;
        var y = e.clientY - rect.top - rect.height / 2;
        $(this).css("transform", "perspective(1000px) rotateX(" + (-y / 10) + "deg) rotateY(" + (x / 10) + "deg)");

        setTimeout(() => {
            $(this).css("transform", "");
        }, 100);

        var pointsToAdd = 1;
        setPoints(points + pointsToAdd);
        let cpt = window.cpt
        let displayCpt = "+" + cpt;

        var animationText = $(`<div>${displayCpt}</div>`).css({
            position: 'absolute',
            top: e.pageY + "px",
            left: e.pageX + "px",
            color: '#fff',
            fontSize: '30px',
            fontWeight: 800,
            letterSpacing: '-0.04em',
            fontFamily: 'var(--second-family)',
            zIndex: 9999,
            pointerEvents: 'none'
        });

        $("body").append(animationText);

        animationText.animate({
            top: e.pageY - 150,
            opacity: 0
        }, 500, function(){
            animationText.remove();
        });

        // Decrease energy by 1 after click
        $('#energy').text(energy - cpt);
        updateClickButtonState();
    });

    // Ensure this line is outside of any function, directly in the script section
    document.getElementById('purchase-energy-limit-btn').addEventListener('touchstart', function() {
        this.style.transform = 'scale(0.95)';
    });

    document.getElementById('purchase-energy-limit-btn').addEventListener('touchend', function() {
        this.style.transform = 'scale(1)';
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
                getMiningCardsListData();
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
});
Telegram.WebApp.ready();
Telegram.WebApp.expand();
Telegram.WebApp.setSwipeEnabled(false);
