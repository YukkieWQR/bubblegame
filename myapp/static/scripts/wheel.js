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
(function () {
    const wheel = document.getElementById('wheel');
    const spinButton = document.getElementById('spinButton');

    // Призы и соответствующие им углы с увеличенной частотой для меньших значений
    const prizes = [
        { name: '10', angle: 0 }, { name: '10', angle: 0 }, { name: '10', angle: 0 }, // 3 раза
        { name: '500', angle: 22.5 }, { name: '500', angle: 22.5 }, // 2 раза
        { name: '90', angle: 45 }, { name: '90', angle: 45 }, // 2 раза
        { name: '250', angle: 67.5 },
        { name: '80', angle: 90 }, { name: '80', angle: 90 }, // 2 раза
        { name: '10000', angle: 112.5 },
        { name: '70', angle: 135 }, { name: '70', angle: 135 }, // 2 раза
        { name: '2500', angle: 157.5 },
        { name: '50', angle: 180 }, { name: '50', angle: 180 }, { name: '50', angle: 180 }, // 3 раза
        { name: '150', angle: 202.5 },
        { name: '100', angle: 225 }, { name: '100', angle: 225 }, // 2 раза
        { name: '350', angle: 247.5 },
        { name: '5', angle: 270 }, { name: '5', angle: 270 }, { name: '5', angle: 270 }, // 3 раза
        { name: '1000', angle: 292.5 },
        { name: '20', angle: 315 }, { name: '20', angle: 315 }, // 2 раза
        { name: '5000', angle: 337.5 }
    ];

    const spinDuration = 3000; // Продолжительность вращения в миллисекундах
    let currentRotation = 0; // Текущее количество градусов вращения

    function animateButton() {
        spinButton.style.transition = 'all 0.1s';
        spinButton.style.transform = 'scale(0.9)'; // Уменьшает кнопку и сдвигает её в центр

        setTimeout(() => {
            spinButton.style.transform = 'scale(1)'; // Возвращает кнопку к исходному размеру
        }, 100);
    }

    spinButton.addEventListener('click', () => {

        spinButton.disabled = true

        animateButton()

        const randomIndex = Math.floor(Math.random() * prizes.length);
        const targetPrize = prizes[randomIndex];

        const targetAngle = targetPrize.angle;

        // Сброс предыдущего вращения и добавление нового угла
        const extraRotation = 3600; // 10 оборотов для эффекта
        const finalRotation = extraRotation + targetAngle - (currentRotation % 360);

        // Обновляем текущее количество градусов вращения
        currentRotation += finalRotation;

        wheel.style.transition = `transform ${spinDuration}ms ease-out`;
        wheel.style.transform = `rotate(${currentRotation}deg)`;

        setTimeout(() => {
            $.ajax({
                url: "/get_wheel_spin_result/",
                method: "POST",
                data: {
                    'username': $('body').data('username'),
                    'result': targetPrize.name,
                    'csrfmiddlewaretoken': $('body').data('csrftoken')
                },
                success: function (response) {
                    getNewData();
                    spinButton.disabled = false
                },
                error: function () {
                    alert('Error');
                }
            });
        }, spinDuration);
    });
})();






