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
            $('.userName').text(response.user);
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
            // Update the content on the page with the received HTML
            $('#dynamicContent').html(response);
            getNewData();
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

function bonusEligible() {
    const url = "/bonus_eligibility/"
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
    const url = "/daily_task/"
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
            alert('You have successfully received your reward!');
            dailyTaskClaim.remove();
            dailyContainer.append(`<div class="doneButton">Done</div>`)
        },
        error: function(response){
            alert('Daily bonus already received');
            dailyTaskClaim.remove();
            dailyContainer.append(`<div class="doneButton">Done</div>`)
        }
    });
})
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
                        taskCost = Math.round(taskCost);
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
                                    <div>
                                        <img src="../static/images/userAvatar.png" alt="" width="30px" height="30px">
                                    </div>
                                    <div style="gap: 3px; display: flex; flex-direction: column">
                                        <div style="display: flex; flex-direction: row; gap: 5px; font: 500 12px var(--second-family); letter-spacing: -0.03em; color: #fff;">
                                            <div>${taskName}</div>
                                        </div>
                                        <div style="font: 600 11px var(--second-family); letter-spacing: -0.04em; color: #fff; display: flex; flex-direction: row; align-items: center">
                                            <img src="../static/images/airdrop.png" alt="" width="24px">
                                            <div id="rewardCost">+${taskCost}</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="doneButton start${i}">${taskStatus}</div>
                            </div>
                        `);
                        } else if (taskStatus === "Claim") {
                            specialTasks.append(`
                            <div class="taskContainer container${i}" data-taskPk="${taskPk}">
                                <div class="dailyCount task${i}">
                                    <div>
                                        <img src="../static/images/userAvatar.png" alt="" width="30px" height="30px">
                                    </div>
                                    <div style="gap: 3px; display: flex; flex-direction: column">
                                        <div style="display: flex; flex-direction: row; gap: 5px; font: 500 12px var(--second-family); letter-spacing: -0.03em; color: #fff;">
                                            <div>${taskName}</div>
                                        </div>
                                        <div style="font: 600 11px var(--second-family); letter-spacing: -0.04em; color: #fff; display: flex; flex-direction: row; align-items: center">
                                            <img src="../static/images/airdrop.png" alt="" width="24px">
                                            <div id="rewardCost">+${taskCost}</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="claimButton start${i}">${taskStatus}</div>
                            </div>
                        `);
                        } else {
                            specialTasks.append(`
                            <div class="taskContainer container${i}" data-taskPk="${taskPk}">
                                <div class="dailyCount task${i}">
                                    <div>
                                        <img src="../static/images/userAvatar.png" alt="" width="30px" height="30px">
                                    </div>
                                    <div style="gap: 3px; display: flex; flex-direction: column">
                                        <div style="display: flex; flex-direction: row; gap: 5px; font: 500 12px var(--second-family); letter-spacing: -0.03em; color: #fff;">
                                            <div>${taskName}</div>
                                        </div>
                                        <div style="font: 600 11px var(--second-family); letter-spacing: -0.04em; color: #fff; display: flex; flex-direction: row; align-items: center">
                                            <img src="../static/images/airdrop.png" alt="" width="24px">
                                            <div id="rewardCost">+${taskCost}</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="startButton start${i}">${taskStatus}</div>
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