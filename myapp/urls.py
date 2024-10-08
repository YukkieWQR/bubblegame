from django.urls import path
from .views import *




urlpatterns = [
    path('', index, name='index'),
    path('referral/', index_referral, name='index_referral'),

    path('load_boost_html/', load_boost_html, name='load_boost_html'),
    path('get_data_about_user/', get_data_about_user, name='get_data_about_user'),
    path('load_main_page/', load_main_page, name='load_main_page'),
    path('load_mine_page/', load_mine_page, name='load_mine_page'),
    path('load_tasks_page/', load_tasks_page, name='load_tasks_page'),
    path('load_airdrop_page/', load_airdrop_page, name='load_airdrop_page'),
    path('load_friends_page/', load_friends_page, name='load_friends_page'),
    path('load_prey_page/', load_prey_page, name='load_prey_page'),
    path('load_wheel_page/', load_wheel_page, name='load_wheel_page'),
    path('get_data_about_user/', get_data_about_user, name='get_data_about_user'),
    path('update_task_status/', update_task_status, name='update_task_status'),
    path('statistics/', statistics_view, name='statistics'),
    path('bonus_eligibility/', bonus_eligibility, name='bonus_eligibility'),
    path('get_user_bonus/', get_user_bonus, name='get_user_bonus'),
    path('three_friends_task/', three_friends_task, name='three_friends_task'),

    path('update_task_status/', update_task_status, name='update_task_status'),
    path('update_task_timer_status/', update_task_timer_status, name='update_task_timer_status'),
    path('update_task_timer_status_bool/', update_task_timer_status_bool, name='update_task_timer_status_bool'),

    path('get_bonus/', get_bonus, name='get_bonus'),
    path('get_daily_bonus_into_wallet/', get_daily_bonus_into_wallet, name='get_daily_bonus_into_wallet'),
    path('hour_task/', hour_task, name='hour_task'),
    path('hour2_task/', hour2_task, name='hour_task_2'),
    path('get_hour12_bonus_into_wallet_1/', get_hour12_bonus_into_wallet_1, name='get_hour12_bonus_into_wallet_1'),
    path('get_hour12_bonus_into_wallet_2/', get_hour12_bonus_into_wallet_2, name='get_hour12_bonus_into_wallet_2'),
    path('get_3fr_bonus_into_wallet/', get_3fr_bonus_into_wallet, name='get_3fr_bonus_into_wallet'),

    path('reward_for_subscription/', reward_for_subscription, name='reward_for_subscription'),
    path('add_to_bonus/', add_to_bonus, name='add_to_bonus'),

    path('json_bot_1/', json_bot_1, name='json_bot_1'),
    path('json_bot_2/', json_bot_2, name='json_bot_2'),
    path('get_domen/', get_domen, name='get_domen'),
    path('get_bot_url/', get_bot_url, name='get_bot_url'),

    path('json_bot_stats/', json_bot_stats, name='json_bot_stats'),
]



