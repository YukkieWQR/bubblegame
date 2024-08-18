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
function getMiningCardsListData() {
    const url = "/mining_card/";
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
            const mineMenu = $('.mineMenu');
            mineMenu.empty();

            // Создаём мапу для user_mining по mining ID
            let userMiningMap = {};
            if (response.user_mining) {
                response.user_mining.forEach(item => {
                    let matchingMining = response.mining.find(mine => mine.name === item["mining__name"]);
                    if (matchingMining) {
                        userMiningMap[matchingMining.id] = item;
                    }
                });
            }

            if (response.mining.length > 0) {
                for (let i = 0; i < response.mining.length; i++) {
                    let mineCardId = response.mining[i].id;
                    let mineCardName = response.mining[i].name;
                    let mineCardImg = response.mining[i].picture.replace('myapp/', '../');
                    let mineCardProfit = parseFloat(response.mining[i].income_per_hour).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
                    let mineCardLevel = userMiningMap[mineCardId] ? userMiningMap[mineCardId].level || 0 : 0;
                    let mineCardCost = userMiningMap[mineCardId] ? parseFloat(userMiningMap[mineCardId].cost).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " ") :
                        parseFloat(response.mining[i].cost).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, " ");

                    mineMenu.append(`
                        <div id="mineContainer${i}" class="mineContainer">
                            <div style="display: flex;flex-direction: column;align-items: center;justify-content: space-between;width: -webkit-fill-available;">
                                <div class="mineImg">
                                    <img src="${mineCardImg}" alt="" class="mineImg" height="48px" width="48px"/>
                                </div>
                                <div class="containerInfo">
                                    <div class="containerName">${mineCardName}</div>
                                    <div class="profitInfo">
                                        Profit per hour
                                        <div class="profitDigits">
                                            <div class="coinImg"><img src="../static/images/coinTask.png" alt="" height="14px" width="14px"></div>
                                            <div class="profit">
                                                +${mineCardProfit}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="upgradeInfo">
                                <svg width="100%" height="2" viewBox="0 0 169 2" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path opacity="0.3" d="M1 1L168 0.999985" stroke="white" stroke-linecap="round" stroke-linejoin="round" />
                                </svg>
                                <div style="display: flex;flex-direction: row;width: -webkit-fill-available;align-items: center;justify-content: space-evenly;padding-bottom: 3px;">
                                    <div class="miningLevel">lvl ${mineCardLevel}</div>
                                    <svg width="2" height="28" viewBox="0 0 2 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path opacity="0.3" d="M1 1L0.999999 27" stroke="white" stroke-linecap="round" stroke-linejoin="round" />
                                    </svg>
                                    <div class="upgradePrice">
                                        <img src="../static/images/coinTask.png" alt="" width="24px" height="22px">
                                        <div class="price">
                                            ${mineCardCost}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `);

                    // Создаем скрытую карточку меню
                    mineMenu.append(`
                        <div id="menu" class="hidden menu${i} menu" data-mining="${mineCardId}">
                            <div id="closeButton" class="closeButton${i}">
                                <img src="../static/images/close.png" alt="" width="21px">
                            </div>
                            <div class="menuMain menuMainMine">
                                <img src="${mineCardImg}" alt="" style="height: 100px" width="auto"/>
                                <h2>${mineCardName}</h2>
                                <div class="menuDescription">
                                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Alias dicta inventore itaque iusto nemo quam quos recusandae sunt tenetur voluptatem? Aperiam deserunt facilis minima perspiciatis rerum tempore voluptatibus! Dicta, ipsam?
                            </div>
                            </div>
                            <div class="profitPerHour">
                                <div>Profit per hour</div>
                                <div class="profitCount">
                                    <img src="../static/images/coinTask.png" alt="" height="16px" width="auto">
                                    <div class="decimal">+ ${mineCardProfit}</div>
                                </div>
                            </div>
                            <div style="font: 700 26px var(--second-family); letter-spacing: -0.01em; text-align: center; color: #fff; height: 100%; display: flex; align-items: center; justify-content: center">
                                <img src="../static/images/airdrop.png" alt="" height="40px" width="auto">
                                <div id="mineCard_cost">${mineCardCost}</div>
                            </div>
                            <div id="button" class="button button${i}">
                                Purchase
                            </div>
                        </div>
                    `);

                    // Добавляем обработчики событий для кнопок
                    $('#mineContainer' + i).on('click', function() {
                        $('.menu' + i).toggleClass('hidden');
                    });
                    $('.closeButton' + i).on('click', function() {
                        $('.menu' + i).addClass('hidden');
                    });
                }
            } else {
                mineMenu.append('<div class="noFriends">Mining activities will appear here very soon!</div>');
            }
        },
        error: function(response) {
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





