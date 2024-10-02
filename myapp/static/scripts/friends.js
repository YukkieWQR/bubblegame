function getFriendData(name, callback) {
    const url = "/get_user_bonus/";
    const url2 = "/add_to_bonus/";
    let username = name;
    let csrfToken = $('body').data('csrftoken');
    let totalBonus = 0;

    function getBonusData(callback) {
        $.ajax({
            url: url2,
            method: "POST",
            data: {
                'username': username,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                totalBonus += parseFloat(response.addtobonus);
                console.log(totalBonus);
                // Call the callback here; only after bonus data has been fetched
                callback();
            },
            error: function(response) {
                alert('Error loading content');
            }
        });
    }

    $.ajax({
        url: url,
        method: "POST",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            let friendLevel = response.depth_lists.filter(array => Array.isArray(array) && array.length > 0).length;
            let firstList = response.depth_lists[0];
            let friendCount = firstList ? firstList.length : 0; // Handle case where firstList might be undefined

            // Calculate `friendCountTwoCount` dynamically if needed
            let friendCountTwoCount = response.depth_lists.flat().length;

            // Now call getBonusData and pass in a callback
            getBonusData(function() {
                // Now we can safely call the final callback with the updated totalBonus
                if (callback && typeof callback === "function") {
                    callback((totalBonus += parseFloat(response.bonus)), friendCount, friendLevel, friendCountTwoCount);
                }
            });
        },
        error: function(response) {
            alert('Error loading content');
        }
    });
}

function getFriendData(name, callback) {
    const url = "/get_user_bonus/";
    const url2 = "/add_to_bonus/";
    let username = name;
    let csrfToken = $('body').data('csrftoken');
    let totalBonus = 0;

    function getBonusData(callback) {
        $.ajax({
            url: url2,
            method: "POST",
            data: {
                'username': username,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                totalBonus += parseFloat(response.addtobonus);
                console.log(totalBonus);
                // Call the callback here; only after bonus data has been fetched
                callback();
            },
            error: function(response) {
                alert('Error loading content');
            }
        });
    }

    $.ajax({
        url: url,
        method: "POST",
        data: {
            'username': username,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            let friendLevel = response.depth_lists.filter(array => Array.isArray(array) && array.length > 0).length;
            let firstList = response.depth_lists[0];
            let friendCount = firstList ? firstList.length : 0; // Handle case where firstList might be undefined

            // Calculate `friendCountTwoCount` dynamically if needed
            let friendCountTwoCount = response.depth_lists.flat().length;

            // Now call getBonusData and pass in a callback
            getBonusData(function() {
                // Now we can safely call the final callback with the updated totalBonus
                if (callback && typeof callback === "function") {
                    callback((totalBonus += parseFloat(response.bonus)), friendCount, friendLevel, friendCountTwoCount);
                }
            });
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

            // Retrieve friends from all depth levels
            const allFriends = response.depth_lists.flat(); // Flatten the array of arrays

            if (allFriends.length > 0) {
                for (let j = 0; j < response.depth_lists[0].length; j++) {
                    let friendName = response.depth_lists[0][j];

                    // Calculate dynamic friend count for this specific friend
                    let friendCountTwoCount = allFriends.length; // Adjust this based on specific criteria if needed

                    // Call getFriendData with the friend's name and a callback function
                    getFriendData(friendName, function(bonus, friendCount, friendLevel, dynamicCount) {
                        friendList.append(`
                            <div class="profitClaim">
                                <div class="friendName">
                                    <div class="friendLevel">${(friendLevel === 0) ? 1 : (friendLevel + 1)} lvl</div>
                                    <img src="../static/images/userAvatar.png" alt="" height="36px">
                                    <div class="friendsCount">${dynamicCount}</div>Friends
                                    <img src="../static/images/ellipse.png" alt="" height="24px">
                                    <div class="earnedContainer">${Math.round(bonus)} Earned</div>
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

$('#copyButton').click(function (event) {
    // Check if the button is disabled
    if ($('#copyButton').prop('disabled')) {
        event.preventDefault(); // Prevent button action if already disabled
        return; // Exit the function early
    }

    // Disable the button
    $('#copyButton').prop('disabled', true);

    let username = $('body').data('username');
    navigator.clipboard.writeText(`https://t.me/BubblesNice_bot?start=invitor_${username}

Play with me, grow your financial empire and get tokens on TON after Airdrop`)
        .then(function() {
            // Append success message
            $('#copyButton').append(`<div class="successText">Referral link copied successfully!</div>`);
            $('.copyLinkButton').css('height', '99px'); // Use jQuery's css method

            // Remove success message after 3 seconds
            setTimeout(function () {
                $('.successText').remove(); // This will remove the success message when it's no longer needed
                $('.copyLinkButton').css('height', '54px'); // Use jQuery's css method

                // Re-enable the button
                $('#copyButton').prop('disabled', false);
            }, 3000);
        })
        .catch(function(error) {
            console.error('Could not copy text: ', error);

            // Re-enable the button in case of error
            $('#copyButton').prop('disabled', false);
        });
});

$('#generate-referral-link').click(function () {
    let username = $('body').data('username');
    let url = `https://t.me/BubblesNice_bot?start=invitor_${username}`
    let text = `
Play with me, grow your financial empire and get tokens on TON after Airdrop`
    const shareUrl = 'https://t.me/share/url?url=' + encodeURIComponent(url) + '&text=' + encodeURIComponent(text);

    window.location.href = shareUrl
});


