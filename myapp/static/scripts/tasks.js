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
            getNewData(); // Synchronize with server on friends page load
            getFriendsListData()
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
function threeFriendsTaskEligible(disabledElem) {
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
            if (!response.can_recieve_3fr_reward) {
                disabledElem.disabled = true;  // Properly disable the button
                disabledElem.style.opacity = '0.5';  // Visually indicate it's disabled
                if (response.recieved_threefriends_reward) {
                    disabledElem.textContent = "Done"
                }
            }
        },
        error: function(response){
            console.error('Error checking eligibility.');
        }
    });
}

(function () {
    let friendsTaskClaim = document.querySelector('.friendsTaskClaim');
    let friendsTaskClaimContainer = document.querySelector('.taskClaimContainer');

    // Call the function to check eligibility
    threeFriendsTaskEligible(friendsTaskClaim);

    friendsTaskClaim.addEventListener('click', function () {

        if (friendsTaskClaim.disabled) {
            event.preventDefault();  // Prevent the click event if button is disabled
            return;  // Stop further execution
        }

        const url = "/get_3fr_bonus_into_wallet/";
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
                friendsTaskClaimContainer.innerHTML = ''; // Clear the container
                friendsTaskClaimContainer.innerHTML = `
                    <div class="doneButton">Done</div>
                `;
            },
            error: function(response){
                console.error('Error processing reward.');
            }
        });
    });
})();

(function () {
    const url = "/hour12_task/";
    let username = $('body').data('username');
    let csrfToken = $('body').data('csrftoken');

    function attachStartButtonListener() {
        // Attach the event listener to the .startButton
        $('.startButton').on('click', function() {
            const claimUrl = "/get_hour12_bonus_into_wallet/";
            $.ajax({
                url: claimUrl,
                method: "POST",
                data: {
                    'username': username,
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function(response) {
                    // Handle successful reward claim here
                    console.log('Reward claimed successfully');
                    // After claiming the reward, start the cycle again
                    fetchTaskData();
                },
                error: function(response) {
                    console.error('Error processing reward.');
                }
            });
        });
    }

    function fetchTaskData() {
        $.ajax({
            url: url,
            method: "POST",
            data: {
                'username': username,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                let taskTimer = response.time_until_active;

                if (response.status === false) {
                    // Status is false: Set button to inactive
                    $('.12hTaskClaimContainer').css('opacity', '0.5');
                    $('.12hTaskClaimContainer').attr('disabled', true);
                    $('.12hTaskClaimContainer').html('<div class="startButton">Start</div>');

                    // Prevent actions if the button is inactive
                    $('.12hTaskClaimContainer').on('click', function(e) {
                        e.preventDefault();
                    });

                    if (taskTimer <= 0) {
                        $('.timerSet').text('Now!');
                    } else {
                        startCountdown(taskTimer);
                    }

                } else {
                    // Status is true: Set button to active
                    $('.12hTaskClaimContainer').css('opacity', '1');
                    $('.12hTaskClaimContainer').attr('disabled', false);
                    $('.12hTaskClaimContainer').html('<div class="startButton">Start</div>');

                    attachStartButtonListener();

                    if (taskTimer <= 0) {
                        $('.timerSet').text('Now!');
                    } else {
                        startCountdown(taskTimer);
                    }
                }
            },
            error: function(response) {
                console.error('Error processing task.');
            }
        });
    }

    function startCountdown(taskTimer) {
        let totalSeconds = Math.floor(taskTimer * 3600);

        let countdown = setInterval(function() {
            if (totalSeconds <= 0) {
                clearInterval(countdown);
                console.log('Timer finished');

                // Replace content in .12hTaskClaimContainer and set timer text to 'Now!'
                $('.12hTaskClaimContainer').empty();
                $('.12hTaskClaimContainer').html('<div class="startButton">Start</div>');
                $('.12hTaskClaimContainer').css('opacity', '1');
                $('.timerSet').text('Now!');

                // Re-attach event listener after timer finishes
                attachStartButtonListener();

            } else {
                totalSeconds--;
                let countdownHours = Math.floor(totalSeconds / 3600);
                let countdownMinutes = Math.floor((totalSeconds % 3600) / 60);
                let countdownSeconds = totalSeconds % 60;

                let countdownDisplay = `${countdownHours}h ${countdownMinutes}m`;
                let countdownDisplayForConsole = `${countdownHours}h ${countdownMinutes}m ${countdownSeconds}s`;
                console.log(`Countdown: ${countdownDisplayForConsole}`);

                // Update the interface inside .timerSet
                $('.timerSet').text(countdownDisplay);
            }
        }, 1000);
    }

    // Start the initial fetch of task data
    fetchTaskData();
})();

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
                    specialTasks.append('<div class="noFriends">No special tasks yet</div>');
                }
            },
            error: function(response){
                alert('Error loading content');
            }
        });
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