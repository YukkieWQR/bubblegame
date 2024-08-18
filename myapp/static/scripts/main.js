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
            let walletAmount = parseFloat(response.new_wallet).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
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
(function () {
    "use strict";

    const items = [
        "berry.png",
        "berry.png",
        "seven.png",
        "berry.png",
        "berry.png",
        "seven.png",
        "seven.png",
        "melon.png",
        "melon.png",
        "seven.png",
        "melon.png",
        "melon.png",
    ];

    const imagePath = "../static/images/";

    const doors = document.querySelectorAll(".door");
    let results = ["", "", ""];
    let resultsForServer = ["", "", ""];

    const spinner = document.querySelector("#spinner");

    spinner.addEventListener("click", function () {
        if (!spinner.disabled) { // Check if the button is not disabled
            spin();

            this.style.transition = 'all 0.2s';
            this.style.transform = 'scale(0.9)';

            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        }
    });

    async function spin() {
        spinner.disabled = true; // Disable the button
        init(false, 1, 2);
        for (const door of doors) {
            const boxes = door.querySelector(".boxes");
            const duration = parseInt(boxes.style.transitionDuration);
            boxes.style.transform = "translateY(0)";
            await new Promise((resolve) => setTimeout(resolve, duration * 100));
        }
        extractResults();
    }

    function init(firstInit = true, groups = 1, duration = 1) {
        for (let i = 0; i < doors.length; i++) {
            const door = doors[i];
            const boxes = door.querySelector(".boxes");
            const boxesClone = boxes.cloneNode(false);

            const pool = firstInit ? [items[Math.floor(Math.random() * items.length)]] : [results[i]];

            if (!firstInit) {
                const arr = [];
                for (let n = 0; n < (groups > 0 ? groups : 1); n++) {
                    arr.push(...items);
                }
                pool.push(...shuffle(arr));

                boxesClone.addEventListener(
                    "transitionstart",
                    function () {
                        door.dataset.spinned = "1";
                        this.querySelectorAll(".box").forEach((box) => {
                            box.style.filter = "blur(1px)";
                        });
                    },
                    { once: true }
                );

                boxesClone.addEventListener(
                    "transitionend",
                    function () {
                        this.querySelectorAll(".box").forEach((box, index) => {
                            box.style.filter = "blur(0)";
                            if (index > 0) this.removeChild(box);
                        });
                    },
                    { once: true }
                );
            }

            for (let j = pool.length - 1; j >= 0; j--) {
                const box = document.createElement("div");
                box.classList.add("box");
                box.style.width = door.clientWidth + "px";
                box.style.height = door.clientHeight + "px";
                const img = document.createElement("img");
                img.src = imagePath + pool[j];
                img.style.width = "50px";
                img.style.height = "50px";
                box.appendChild(img);
                boxesClone.appendChild(box);
            }

            boxesClone.style.transitionDuration = `0.66s`;
            const translateDistance = door.clientHeight * (pool.length - 1);

            boxesClone.style.transform = `translateY(-${translateDistance}px)`;
            door.replaceChild(boxesClone, boxes);
        }
    }

    function extractResults() {
        results = [];
        resultsForServer = [];

        for (const door of doors) {
            const boxes = door.querySelector(".boxes");
            const box = boxes.querySelector(".box img"); // Get the <img> element
            const fileName = box.src.split("/").pop(); // Extract the file name from the src
            const nameWithoutExtension = fileName.replace(".png", ""); // Remove the .png extension
            results.push(fileName);
            resultsForServer.push(nameWithoutExtension);
        }
        console.log("Результаты:", results);

        // Delay the AJAX request by 1 second (1000 milliseconds)
        setTimeout(() => {
            spinner.disabled = false;

            $.ajax({
                url: "/get_slot_spin_result/",
                method: "POST",
                data: {
                    'username': $('body').data('username'),
                    'result_1': resultsForServer[0],
                    'result_2': resultsForServer[1],
                    'result_3': resultsForServer[2],
                    'csrfmiddlewaretoken': $('body').data('csrftoken')
                },
                success: function (response) {
                    getNewData();
                },
                error: function () {
                    alert('Error');
                }
            });
        }, 660); // 1000 milliseconds = 1 second
    }

    function shuffle([...arr]) {
        let m = arr.length;
        while (m) {
            const i = Math.floor(Math.random() * m--);
            [arr[m], arr[i]] = [arr[i], arr[m]];
        }
        return arr;
    }

    init();
})();

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
$(document).ready(function () {
    sessionStorage.setItem('currentTab', 'firstCat')
    console.log(sessionStorage.getItem('currentTab'))
})

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
        success: function (response) {
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
        error: function (response) {
            alert('Error loading content');
        }
    });
})
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
