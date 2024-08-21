function getFriendData(name, callback) {
    const url = "/get_user_bonus/";
    let username = name;
    let csrfToken = $('body').data('csrftoken');
    $.ajax({
        url: url,
        method: "POST",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            // Calculate the correct friend count by summing the lengths of all non-empty lists
            let depthLists = response.depth_lists;
            let friendCount = depthLists.reduce((count, list) => count + list.length, 0);

            // Call the callback function with the bonus value and corrected friendCount
            if (callback && typeof callback === "function") {
                callback(response.bonus, friendCount);
            }
        },
        error: function(response) {
            alert('Error loading content');
        }
    });
}

function getFriendsListData() {
    const url = "/get_user_bonus/";
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
            const friendList = $('.friendList');
            friendList.empty(); // Clear the friends list before adding new names

            // Retrieve friends only from the first element of depth_lists
            const firstList = response.depth_lists[0];

            if (firstList && firstList.length > 0) {
                let friendCount = firstList.length; // Number of friends in the first list

                for (let j = 0; j < firstList.length; j++) {
                    let friendName = firstList[j];

                    // Call getFriendData with the friend's name and a callback function
                    getFriendData(friendName, function(bonus, friendCount) {
                        friendList.append(`
                            <div class="profitClaim">
                                <div class="friendName">
                                    <img src="../static/images/userAvatar.png" alt="" height="36px">
                                    <div class="friendsCount">${friendCount}</div>Friends
                                    <img src="../static/images/ellipse.png" alt="" height="24px">
                                    <div class="earnedContainer">${bonus} Earned</div>
                                </div>
                            </div>`);
                    });
                }
            } else {
                friendList.append('<div class="noFriends">You haven\'t invited anyone yet</div>');
            }
        },
        error: function(response) {
            alert('Error loading content');
        }
    });
}

$('#applyBonus').click(function () {
    const url = "/get_user_bonus_into_wallet/"
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
            $('#counter').text('0');
        },
        error: function(response){
            alert('Error loading content');
        }
    });
})


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
            getFriendsData()
            getFriendsListData()
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

$('#copyButton').click(function () {
    let username = $('body').data('username');
    navigator.clipboard.writeText(`https://t.me/lionkombatgame_bot?start=startapp=${username}

Play with me, grow your financial empire and get tokens on TON after Airdrop

💸 +5k coins as your first gift
🔥 +A lot of extra bonuses for Early Adopters`).then(function() {
        alert('Link copied successfully!');
    })
});

$('#generate-referral-link').click(function () {
    let username = $('body').data('username');
    let url = `https://t.me/lionkombatgame_bot?start=startapp=${username}`
    let text = `
Play with me, grow your financial empire and get tokens on TON after Airdrop

💸 +5k coins as your first gift
🔥 +A lot of extra bonuses for Early Adopters`
    const shareUrl = 'https://t.me/share/url?url=' + encodeURIComponent(url) + '&text=' + encodeURIComponent(text);

    window.location.href = shareUrl
});


