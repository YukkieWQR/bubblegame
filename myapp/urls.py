from django.urls import path
from .views import *



urlpatterns = [
    path('', index, name='index'),
    path('referral/', index_referral, name='index_referral'),
    path('increment_wallet/', increment_wallet, name='increment_wallet'),
    path('purchase_multitap/', purchase_multitap, name='purchase_multitap'),
    path('purchase_energy_limit/', purchase_energy_limit, name='purchase_energy_limit'),
    path('update_energy/', update_energy, name='update_energy'),
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
    path('apply_bonus/', apply_bonus_view, name='apply_bonus'),  # Updated to use username as a path parameter
    path('statistics/', statistics_view, name='statistics'),
    path('daily_task/', daily_task, name='daily_task'),
    path('bonus_eligibility/', bonus_eligibility, name='bonus_eligibility'),
    path('get_user_bonus/', get_user_bonus, name='get_user_bonus'),
    path('daily_energy/', daily_energy, name='daily_energy'),
    path('daily_energy_bonus_eligibility/', daily_energy_bonus_eligibility, name='daily_energy_bonus_eligibility'),
    path('daily_turbo_bonus_eligibility/', daily_turbo_bonus_eligibility, name='daily_turbo_bonus_eligibility'),
    path('daily_turbo/', daily_turbo, name='daily_turbo'),

    path('daily_energy_bonus_eligibilit_for_button/', daily_energy_bonus_eligibilit_for_button, name='daily_energy_bonus_eligibilit_for_button'),

    path('daily_task_timer/', daily_task_timer, name='daily_task_timer'),

    path('daily_energy_bonus_eligibilit_for_button/', daily_energy_bonus_eligibilit_for_button, name='daily_energy_bonus_eligibilit_for_button'),

    ]
