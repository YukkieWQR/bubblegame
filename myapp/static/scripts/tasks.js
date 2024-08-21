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
            // Обновление контента на странице с полученным HTML
            $('#coins_per_tap').text("+" + response.efficiencypertap);
            $('.userNameContainer').text(response.user);
            $('#energy_limit_level').text(response.energy_limit_level_digits);
            $('#level').text(response.userlevelname);
            $('#wallet').text(response.new_wallet);
            let newWallet = parseFloat(response.new_wallet);
            $('#wallet').text(Math.round(newWallet));
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
function taskList() {
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
                const specialTasks = $('#specialTasks')
                if (response.tasks.length > 0) {
                    response.tasks.forEach((task, i) => {
                        let taskName = task.name;
                        let taskCost = task.cost;
                        let taskImg = task.picture.replace('myapp/', '../');
                        taskCost = parseFloat(taskCost).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                        let taskStatus = "Start";
                        let taskPk = null
                        response.tasks.forEach((task) => {
                            if (task.name === taskName) {
                                taskPk = task.id;
                            }
                        });
                        response.user_tasks.forEach((userTask) => {
                            if (userTask.task__name === taskName) {
                                if (userTask.status === 3) {
                                    taskStatus = "Done";
                                } else if (userTask.status === 2) {
                                    taskStatus = "Claim";
                                }
                            }
                        });
                        if (taskStatus === "Done") {
                            specialTasks.append(`
                            <div class="taskContainer container${i}" data-taskPk="${taskPk}">
                                <div class="dailyCount task${i}">
                                    <div style="margin-right: 14px">
                                        <img src="../static/images/calendar.png" alt="" width="36px" height="auto">
                                    </div>
                                    <div style="gap: 3px; display: flex; flex-direction: column">
                                        <div style="display: flex; flex-direction: row; gap: 5px; font: 600 13px var(--font-family); letter-spacing: -0.03em; color: var(--white);">
                                            <div>${taskName}</div>
                                        </div>
                                        <div style="font: 600 11px var(--font-family);letter-spacing: -0.04em;background: linear-gradient(89deg, #d1317a 0%, #da294c 17.57%, #dd263d 35.33%, #e87d31 81.66%, #eda62c 91.09%, #f2d026 98.64%);background-clip: text;-webkit-background-clip: text;-webkit-text-fill-color: transparent; display: flex; flex-direction: row; align-items: center; gap: 5px">
                                            <div id="rewardCost">+ ${taskCost} BUBBLES</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="doneButton start${i}">Done</div>
                            </div>
                        `);
                        } else if (taskStatus === "Claim") {
                            specialTasks.append(`
                            <div class="taskContainer container${i}" data-taskPk="${taskPk}">
                                <div class="dailyCount task${i}">
                                    <div style="margin-right: 14px;">
                                        <img src="../static/images/calendar.png" alt="" width="36px" height="auto">
                                    </div>
                                    <div style="gap: 3px; display: flex; flex-direction: column">
                                        <div style="display: flex; flex-direction: row; gap: 5px; font: 600 13px var(--font-family); letter-spacing: -0.03em; color: var(--white);">
                                            <div>${taskName}</div>
                                        </div>
                                        <div style="font: 600 11px var(--second-family); letter-spacing: -0.04em; color: #fff; display: flex; flex-direction: row; align-items: center; gap: 5px">
                                            <div id="rewardCost">+ ${taskCost} BUBBLES</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="claimButton start${i}">Claim</div>
                            </div>
                        `);
                        } else {
                            specialTasks.append(`
                            <div class="taskContainer container${i}" data-taskPk="${taskPk}">
                                <div class="dailyCount task${i}">
                                    <div style="margin-right: 14px;">
                                        <img src="../static/images/calendar.png" alt="" width="36px" height="auto">
                                    </div>
                                    <div style="gap: 3px; display: flex; flex-direction: column">
                                        <div style="display: flex; flex-direction: row; gap: 5px; font: 600 13px var(--font-family); letter-spacing: -0.03em; color: var(--white);">
                                            <div>${taskName}</div>
                                        </div>
                                        <div style="font: 600 11px var(--second-family); letter-spacing: -0.04em; color: #fff; display: flex; flex-direction: row; align-items: center; gap: 5px">
                                            <div id="rewardCost">+ ${taskCost} BUBBLES</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="startButton start${i}">Start</div>
                            </div>
                        `);
                        }
                    });
                } else {
                    specialTasks.append('<div class="noFriends">No tasks yet</div>');
                }
            },
            error: function(response){
                alert('Error loading content');
            }
        });
}
function getDailyTaskTimer() {
    const url = "/daily_task_timer/";
    let username = $('body').data('username');
    let csrfToken = $('body').data('csrftoken');

    $.ajax({
        url: url,
        method: "GET",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response){
            const timePattern = /^\d+:\d+:\d+(\.\d+)?$/;

            $('.timerSet').removeClass('timer2');
            $('.timerSet').removeClass('timer');

            if (timePattern.test(response.time_until_next_bonus)) {
                let timeParts = response.time_until_next_bonus.split(':');
                let hours = parseInt(timeParts[0], 10);
                let minutes = parseInt(timeParts[1], 10);
                let seconds = Math.floor(parseFloat(timeParts[2]));

                $('.timerSet').addClass('timer2');

                // Функция для обновления таймера
                function updateTimer() {
                    if (seconds < 0) {
                        // Если время истекло, остановить таймер и обновить текст
                        clearInterval(timerInterval);
                        $('.timer2').text('You can claim your bonus now!');
                    } else {
                        // Форматирование времени
                        let roundedTime = String(hours).padStart(2, '0') + ':' +
                            String(minutes).padStart(2, '0') + ':' +
                            String(seconds).padStart(2, '0');


                        $('.timer2').text(roundedTime);

                        // Уменьшаем секунды
                        seconds--;

                        // Если секунды становятся отрицательными, уменьшаем минуты и сбрасываем секунды
                        if (seconds < 0) {
                            seconds = 59;
                            minutes--;
                            if (minutes < 0) {
                                minutes = 59;
                                hours--;
                            }
                        }
                    }
                }

                // Обновляем таймер каждую секунду
                let timerInterval = setInterval(updateTimer, 1000);
                updateTimer(); // Сразу вызываем для отображения первого значения
            } else {
                $('.timerSet').addClass('timer');
                $('.timer').text('You can claim your bonus now!'); // Уведомляем о некорректных данных
            }
        },
        error: function(response){
            alert('Error loading content');
        }
    });
}
function bonusEligible() {
    const url = "/update_task_timer_status_bool/"
    let username = $('body').data('username');
    let csrfToken = $('body').data('csrftoken');
    const dailyTaskClaim = $('.dailyTaskClaim');
    const dailyContainer = $('.dailyContainer');
    $.ajax({
        url: url,
        method: "POST",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function (response) {
            if (response.bonus_eligible === false) {
                dailyTaskClaim.remove();
                dailyContainer.append(`<div class="doneButton">Done</div>`)
            }
        },
        error: function (response) {
            alert('Error loading content');
        }
    })
}

$('.dailyTaskClaim').click(function () {
    const url = "/update_task_timer_status/"
    let username = $('body').data('username');
    let csrfToken = $('body').data('csrftoken');
    const dailyTaskClaim = $('.dailyTaskClaim');
    const dailyContainer = $('.dailyContainer');
    $.ajax({
        url: url,
        method: "POST",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response){
            dailyTaskClaim.remove();
            dailyContainer.append(`<div class="doneButton">Done</div>`)
            getDailyTaskTimer()
        },
        error: function(response){
            alert('Daily bonus already received');
            dailyTaskClaim.remove();
            dailyContainer.append(`<div class="doneButton">Done</div>`)
        }
    });
})

$(document).ready(function() {
    const url = "/update_task_status/";

    $('#specialTasks').on('click', '.startButton, .claimButton', function() {
        let taskName = $(this).closest('.taskContainer').find('.taskName').text();
        let taskPk = $(this).closest('.taskContainer').data('taskpk');
        let username = $('body').data('username');
        let csrfToken = $('body').data('csrftoken');

        let button = $(this);

        $.ajax({
            url: url,
            method: "POST",
            data: {
                'username': username,
                'task_pk': taskPk,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response){
                if (button.hasClass('startButton')) {
                    button.removeClass('startButton').addClass('claimButton').text('Claim');
                    const redirectUrl = response.link;
                    Telegram.WebApp.ready();
                    Telegram.WebApp.expand();
                    Telegram.WebApp.openLink(redirectUrl);
                } else if (button.hasClass('claimButton')) {
                    button.removeClass('claimButton').addClass('doneButton').text('Done');
                }
            },
            error: function(response){
                alert('Error updating task status');
            }
        });
    });

});