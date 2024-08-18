from .models import *
from django.shortcuts import render
from .models import UserProfile, Referral
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseBadRequest
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile


def index(request):
    username = request.GET.get('username')

    context = {}

    level_names = {
        1: 'Bronze',
        2: 'Silver',
        3: 'Gold',
        4: 'Platinum',
        5: 'Diamond',
        6: 'Master',
        7: 'Grandmaster',
        8: 'Elite',
        9: 'Legendary',
        10: 'The King'
    }

    energy_limit_level_digits = {
        1: 1000,
        2: 1500,
        3: 2000,
        4: 2500,
        5: 3000,
        6: 3500,
        7: 4000,
        8: 4500,
        9: 5000,
        10: 5500,
        11: 6000,
        12: 6500,
        13: 7000,
        14: 7500,
        15: 8000,
        16: 8500,
        17: 9000,
        18: 9500,
        19: 10000,
        20: 10500,
    }

    if username:
        user, created = UserProfile.objects.get_or_create(username=username)
        user.regenerate_energy()

        # If the user was created now, check for referral
        if created:
            referral = Referral.objects.filter(invited=username).first()
            if referral:
                invitor = UserProfile.objects.filter(username=referral.referrer.username).first()
                if invitor:
                    # Update wallets
                    user.wallet += 5000
                    invitor.wallet += 5000

                    user.invited_by = invitor.username
                    existing_usernames = invitor.users_invited.split(',')

                    formatted_usernames = [f'"{name.strip()}"' for name in existing_usernames if name.strip()]

                    formatted_usernames.append(f'"{username}"')

                    invitor.users_invited = ', '.join(formatted_usernames)

                    user.save()
                    invitor.save()

        # Update energy limit based on the user's energy_limit_level
        user.energy_limit = energy_limit_level_digits.get(user.energy_limit_level, 1000)
        user.save()

        level = user.level
        userlevelname = level_names.get(level, 'Unknown')
        energy_limit = energy_limit_level_digits.get(user.energy_limit_level, 'Unknown')
        energy_bonus_for_level = 500 * int(level)
        energy_limit = energy_limit + energy_bonus_for_level

        efficiencypertap = f'+{user.tap_efficiency}'

        context['efficiencypertap'] = efficiencypertap
        context['user'] = user
        context['userlevelname'] = userlevelname
        context['energy_limit_level_digits'] = energy_limit
        context['energy_limit'] = user.energy_limit  # Add this line
        context['referral_link'] = None

        if request.method == 'POST':
            if 'generate_referral_link' in request.POST:
                referral = Referral.objects.create(referrer=user)
                context['referral_link'] = f'https://yukkie.pythonanywhere.com/register/?token={referral.token}'

    return render(request, 'index.html', context)



def index_referral(request):
    username = request.GET.get('username')

    invitor_username = request.GET.get('invitor')
    context = {}

    level_names = {
        1: 'Bronze',
        2: 'Silver',
        3: 'Gold',
        4: 'Platinum',
        5: 'Diamond',
        6: 'Master',
        7: 'Grandmaster',
        8: 'Elite',
        9: 'Legendary',
        10: 'The King'
    }

    energy_limit_level_digits = {
        1: 1000,
        2: 1500,
        3: 2000,
        4: 2500,
        5: 3000,
        6: 3500,
        7: 4000,
        8: 4500,
        9: 5000,
        10: 5500,
        11: 6000,
        12: 6500,
        13: 7000,
        14: 7500,
        15: 8000,
        16: 8500,
        17: 9000,
        18: 9500,
        19: 10000,
        20: 10500,
    }


    if username and invitor_username:
        user, created = UserProfile.objects.get_or_create(username=username)
        invitor, invitor_created = UserProfile.objects.get_or_create(username=invitor_username)
        user.regenerate_energy()

        if not user.invited_by:
            user.wallet += 5000
            invitor.wallet += 5000

            user.invited_by = invitor.username
            invitor.users_invited += f"{username},"
            user.save()
            invitor.save()

        # If the user was created now, check for referral
        if created:
            referral = Referral.objects.filter(invited=username).first()
            if referral:
                invitor = UserProfile.objects.filter(username=referral.referrer.username).first()
                if invitor:
                    # Update wallets
                    user.wallet += 5000
                    invitor.wallet += 5000

                    user.invited_by = invitor.username
                    existing_usernames = invitor.users_invited.split(',')

                    formatted_usernames = [f'"{name.strip()}"' for name in existing_usernames if name.strip()]

                    formatted_usernames.append(f'"{username}"')

                    invitor.users_invited = ', '.join(formatted_usernames)

                    user.save()
                    invitor.save()

        # Update energy limit based on the user's energy_limit_level
        user.energy_limit = energy_limit_level_digits.get(user.energy_limit_level, 1000)
        user.save()

        level = user.level
        userlevelname = level_names.get(level, 'Unknown')
        energy_limit = energy_limit_level_digits.get(user.energy_limit_level, 'Unknown')
        energy_bonus_for_level = 500 * int(level)
        energy_limit = energy_limit + energy_bonus_for_level

        efficiencypertap = f'+{user.tap_efficiency}'

        context['efficiencypertap'] = efficiencypertap
        context['user'] = user
        context['userlevelname'] = userlevelname
        context['energy_limit_level_digits'] = energy_limit
        context['energy_limit'] = user.energy_limit  # Add this line
        context['referral_link'] = None

        if request.method == 'POST':
            if 'generate_referral_link' in request.POST:
                referral = Referral.objects.create(referrer=user)
                context['referral_link'] = f'https://yukkie.pythonanywhere.com/register/?token={referral.token}'

    return render(request, 'index.html', context)

def increment_wallet(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = UserProfile.objects.get(username=username)
        user.regenerate_energy()
        now = timezone.now()
        if user.daily_turbo_last_daily_bonus and (now - user.daily_turbo_last_daily_bonus) <= timedelta(seconds=30):
            increment_amount = user.tap_efficiency * 5
        else:
            increment_amount = user.tap_efficiency

        user.wallet += increment_amount
        user.energy -= user.tap_efficiency
        user.check_level_up()
        user.save()
        return JsonResponse({
            'new_wallet': user.wallet,
            'new_level': user.level,
            'coins_per_tap': user.tap_efficiency,
            'energy': user.energy,
            'efficiencypertap': user.tap_efficiency,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def purchase_multitap(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = UserProfile.objects.get(username=username)
        user.regenerate_energy()
        if user.purchase_multitap():
            return JsonResponse({
                'new_wallet': user.wallet,
                'new_multitap_level': user.multitap_level,
                'new_tap_efficiency': user.tap_efficiency,
            })
        else:
            return JsonResponse({'error': 'Not enough funds or max level reached'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def update_energy(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = UserProfile.objects.get(username=username)
        user.regenerate_energy()
        return JsonResponse({
            'energy': user.energy
        })

def purchase_energy_limit(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = UserProfile.objects.get(username=username)
        user.regenerate_energy()
        if user.purchase_energy_limit():
            return JsonResponse({
                'new_wallet': user.wallet,
                'new_energy_limit_level': user.energy_limit_level,
                'new_energy': user.energy,
            })
        else:
            return JsonResponse({'error': 'Not enough funds or max level reached'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def daily_energy(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = UserProfile.objects.get(username=username)
            user.set_energy_to_limit()
            now = timezone.now()
            user.daily_energy_last_daily_bonus = now  # Update the timestamp
            user.save()  # Save the changes to the database
            return JsonResponse({'status': 'success'}, status=200)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def daily_energy_bonus_eligibility(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = UserProfile.objects.get(username=username)
            now = timezone.now()
            last_bonus = user.daily_energy_last_daily_bonus
            bonus_eligible = False
            if user.daily_turbo_last_daily_bonus and (now - user.daily_turbo_last_daily_bonus) <= timedelta(seconds=30):
                bonus_eligible = True
            if last_bonus is None or now - last_bonus >= timedelta(hours=24):
                bonus_eligible = True

            return JsonResponse({'bonus_eligible': bonus_eligible})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def daily_energy_bonus_eligibility(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = UserProfile.objects.get(username=username)
            now = timezone.now()
            last_bonus = user.daily_energy_last_daily_bonus
            bonus_eligible = False
            if user.daily_turbo_last_daily_bonus and (now - user.daily_turbo_last_daily_bonus) <= timedelta(seconds=30):
                bonus_eligible = True
            if last_bonus is None or now - last_bonus >= timedelta(hours=24):
                bonus_eligible = True

            return JsonResponse({'bonus_eligible': bonus_eligible})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def daily_energy_bonus_eligibilit_for_button(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = UserProfile.objects.get(username=username)
            now = timezone.now()

            bonus_eligible = False
            if user.daily_turbo_last_daily_bonus and (now - user.daily_turbo_last_daily_bonus) <= timedelta(seconds=30):
                bonus_eligible = True


            return JsonResponse({'bonus_eligible': bonus_eligible})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def daily_turbo(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = UserProfile.objects.get(username=username)
            now = timezone.now()
            user.daily_turbo_last_daily_bonus = now  # Update the timestamp
            user.save()  # Save the changes to the database

            return JsonResponse({'success': 'Turbo activated!'}, status=200)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def daily_turbo_bonus_eligibility(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = UserProfile.objects.get(username=username)
            now = timezone.now()
            last_bonus = user.daily_turbo_last_daily_bonus
            bonus_eligible = False

            if last_bonus is None or now - last_bonus >= timedelta(hours=24):
                bonus_eligible = True

            return JsonResponse({'bonus_eligible': bonus_eligible})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def load_boost_html(request):
    return render(request, 'boost.html')

def load_main_page(request):
    return render(request, 'index.html')

def load_mine_page(request):
    return render(request, 'mine.html')

def load_friends_page(request):
    return render(request, 'friends.html')

def load_wheel_page(request):
    return render(request, 'wheel.html')

def load_tasks_page(request):
    return render(request, 'tasks.html')

def load_airdrop_page(request):
    return render(request, 'airdrop.html')

def load_prey_page(request):
    return render(request, 'prey.html')
def get_data_about_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(UserProfile, username=username)

        level_names = {
            1: 'Bronze',
            2: 'Silver',
            3: 'Gold',
            4: 'Platinum',
            5: 'Diamond',
            6: 'Master',
            7: 'Grandmaster',
            8: 'Elite',
            9: 'Legendary',
            10: 'The King'
        }

        energy_limit_level_digits = {
            1: 1000,
            2: 1500,
            3: 2000,
            4: 2500,
            5: 3000,
            6: 3500,
            7: 4000,
            8: 4500,
            9: 5000,
            10: 5500,
            11: 6000,
            12: 6500,
            13: 7000,
            14: 7500,
            15: 8000,
            16: 8500,
            17: 9000,
            18: 9500,
            19: 10000,
            20: 10500,
        }

        user.regenerate_energy()

        # Convert users_invited to a list if it's stored as JSON string
        if isinstance(user.users_invited, str):
            # Remove any leading or trailing commas and split the string by commas
            users_invited = user.users_invited.strip().split(',')

            # Remove any leading/trailing whitespace from each item and enclose in double quotes
            users_invited = [f'{item.strip()}' for item in users_invited]

        user_tasks = TaskUser.objects.filter(user=user).select_related('task')
        task_data = list(Task.objects.all().values('id', 'name', 'cost', 'picture'))

        level = user.level
        userlevelname = level_names.get(level, 'Unknown')
        energy_limit = energy_limit_level_digits.get(user.energy_limit_level, 'Unknown')
        energy_bonus_for_level = 500 * int(level)
        energy_limit = energy_limit + energy_bonus_for_level
        print(energy_limit)
        now = timezone.now()
        if user.daily_turbo_last_daily_bonus and (now - user.daily_turbo_last_daily_bonus) <= timedelta(seconds=30):
            increment_amount = user.tap_efficiency * 5
        else:
            increment_amount = user.tap_efficiency


        response_data = {
            'efficiencypertap': increment_amount,
            'user': user.username,
            'userlevelname': userlevelname,
            'energy_limit_level_digits': energy_limit,
            'new_wallet': user.wallet,
            'new_energy_limit_level': user.energy_limit_level,
            'new_energy': user.energy,
            'energy': user.energy,
            'new_level': user.level,
            'next_multitap_upgrade_cost': user.next_multitap_upgrade_cost,
            'next_energy_upgrade_cost': user.next_energy_upgrade_cost,
            #по неизвестной причине переменные перепутались на каком-то моменте, для упрощения переменные здесь меняются местами обратно

            'next_multitap_level': user.next_energy_level,
            'next_energy_level': min(user.multitap_level, 20),
            #
            'max_multitap_level_reached': user.max_multitap_level_reached,
            'max_energy_level_reached': user.max_energy_level_reached,
            'tasks': task_data,
            'user_tasks': list(user_tasks.values('task__name', 'status')),
            'users_invited': users_invited,  # Include users_invited as a list of usernames
        }

        return JsonResponse(response_data)


def update_task_status(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        task_pk = request.POST.get('task_pk')

        user = get_object_or_404(UserProfile, username=username)
        task = get_object_or_404(Task, pk=task_pk)

        task_user, created = TaskUser.objects.get_or_create(user=user, task=task)

        if created:
            task_user.status = 2  # Status 'Start'
        else:
            task_user.status_change()
            if task_user.status == 3:  # Status 'Done'
                user.wallet += task.cost
                user.save()

        task_user.save()

        return JsonResponse({
            'username': user.username,
            'wallet': user.wallet,
            'task': task.name,
            'link': task.link,  # Include the task link in the response
            'status': task_user.get_status_display(),
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def daily_task(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        user = get_object_or_404(UserProfile, username=username)

        now = timezone.now()
        if user.last_daily_bonus:
            time_since_last_bonus = now - user.last_daily_bonus
            if time_since_last_bonus < timedelta(days=1):
                return JsonResponse({'error': 'Daily bonus already received'}, status=400)

        user.wallet += 5000  # Add bonus
        user.last_daily_bonus = now  # Update the timestamp

        user.save()

        return JsonResponse({
            'username': user.username,
            'wallet': user.wallet,
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def daily_task_timer(request):
    if request.method == 'GET':
        username = request.GET.get('username')

        user = get_object_or_404(UserProfile, username=username)

        now = timezone.now()
        if user.last_daily_bonus:
            time_since_last_bonus = now - user.last_daily_bonus
            if time_since_last_bonus < timedelta(days=1):
                time_remaining = timedelta(days=1) - time_since_last_bonus
                return JsonResponse({
                    'username': user.username,
                    'time_until_next_bonus': str(time_remaining)
                })

        return JsonResponse({
            'username': user.username,
            'time_until_next_bonus': 'You can claim your bonus now'
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def apply_bonus_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = UserProfile.objects.get(username=username)
        bonus = user.apply_bonus()
        return JsonResponse({
            'username': user.username,
            'new_wallet': user.wallet,
            'bonus_applied': bonus
        })




def statistics_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        # Check if the username parameter is provided
        if not username:
            return JsonResponse({'error': 'Username is required.'}, status=400)

        # Fetch the user if exists
        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User does not exist.'}, status=404)

        # Aggregate the total wallet sum and user count
        total_wallet_sum = UserProfile.objects.aggregate(Sum('wallet'))['wallet__sum'] or 0
        total_user_count = UserProfile.objects.count()

        return JsonResponse({
            'total_wallet_sum': total_wallet_sum,
            'total_user_count': total_user_count,
        })
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def bonus_eligibility(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        now = timezone.now()
        last_bonus = user.last_daily_bonus
        bonus_eligible = False

        if last_bonus is None or now - last_bonus >= timedelta(hours=24):
            bonus_eligible = True

        return JsonResponse({
            'bonus_eligible': bonus_eligible
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def get_user_bonus(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    username = request.POST.get('username')
    if not username:
        return HttpResponseBadRequest("Username is required.")

    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)

    if not user.users_invited:
        return JsonResponse({'username': user.username, 'invited_users_wallets_sum': 0, 'bonus': 0})

    # Split the users_invited field to get individual usernames, and strip any surrounding whitespace
    invited_usernames = [u.strip() for u in user.users_invited.split(',')]
    invited_users = UserProfile.objects.filter(username__in=invited_usernames)

    # Calculate the sum of the wallets of invited users
    total_wallets_sum = sum(Decimal(invited_user.wallet) for invited_user in invited_users)

    # Calculate the bonus based on the highest invited wallets sum
    bonus = Decimal(0)
    if total_wallets_sum > user.highest_invited_wallets_sum:
        bonus = (total_wallets_sum - user.highest_invited_wallets_sum) * Decimal('0.02')
#        user.highest_invited_wallets_sum = total_wallets_sum
        user.save()

    # Prepare the response data
    response_data = {
        'username': user.username,
        'invited_users_wallets_sum': float(total_wallets_sum),
        'bonus': float(bonus)
    }

    return JsonResponse(response_data)
def get_user_bonus_into_wallet(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    username = request.POST.get('username')
    if not username:
        return HttpResponseBadRequest("Username is required.")

    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)

    if not user.users_invited:
        return JsonResponse({'username': user.username, 'invited_users_wallets_sum': 0, 'bonus': 0})

    # Split the users_invited field to get individual usernames, and strip any surrounding whitespace
    invited_usernames = [u.strip() for u in user.users_invited.split(',')]
    invited_users = UserProfile.objects.filter(username__in=invited_usernames)

    # Calculate the sum of the wallets of invited users
    total_wallets_sum = sum(Decimal(invited_user.wallet) for invited_user in invited_users)

    # Calculate the bonus based on the highest invited wallets sum
    bonus = Decimal(0)
    if total_wallets_sum > user.highest_invited_wallets_sum:
        bonus = (total_wallets_sum - user.highest_invited_wallets_sum) * Decimal('0.02')
        user.highest_invited_wallets_sum = total_wallets_sum
        user.wallet += bonus
        user.save()

    # Prepare the response data
    response_data = {
        'username': user.username,
        'invited_users_wallets_sum': float(total_wallets_sum),
        'bonus': float(bonus)
    }

    return JsonResponse(response_data)

def get_mining_bonus(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    username = request.POST.get('username')

    user = UserProfile.objects.select_for_update().get(username=username)


    now = timezone.now()
    last_bonus_time = user.last_mining_bonus

    if last_bonus_time is None:
        # Initialize last_bonus_time to now if it's None
        last_bonus_time = now
        user.last_mining_bonus = now  # Set the last bonus time to now
        user.save()

    hours_passed = Decimal((now - last_bonus_time).total_seconds() / 3600)
    if hours_passed >= 3:
        hours_passed = 3

    # Fetch all mining cards for the user
    mining_cards = MiningCard.objects.filter(user=user)

    # Calculate total income from all mining cards
    income = Decimal('0.0')
    income_per_hour_count = Decimal('0.0')
    for card in mining_cards:
        income_per_hour = card.calculate_income_actual_lvl()
        card_income = income_per_hour * hours_passed
        income += card_income
        income_per_hour_count += income_per_hour

    income_per_hour_count_final = income_per_hour_count

    total_income = income

    # Prepare the response data
    response_data = {
        'bonus': total_income,
        'income_per_hour': income_per_hour_count_final,
    }

    return JsonResponse(response_data)


def get_mining_bonus_into_wallet(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    username = request.POST.get('username')

    user = UserProfile.objects.select_for_update().get(username=username)

    now = timezone.now()
    last_bonus_time = user.last_mining_bonus

    if last_bonus_time is None:
        # Initialize last_bonus_time to now if it's None
        last_bonus_time = now
        user.last_mining_bonus = now  # Set the last bonus time to now
        user.save()

    hours_passed = Decimal((now - last_bonus_time).total_seconds() / 3600)
    if hours_passed >= 3:
        hours_passed = 3

    # Fetch all mining cards for the user
    mining_cards = MiningCard.objects.filter(user=user)

    # Calculate total income from all mining cards
    income = Decimal('0.0')

    for card in mining_cards:
        income_per_hour = card.calculate_income_actual_lvl()

        card_income = income_per_hour * hours_passed
        income += card_income




    total_income = income

    user.wallet += total_income
    user.last_mining_bonus = now
    user.save()
    # Prepare the response data
    response_data = {
        'bonus': total_income,

    }

    return JsonResponse(response_data)



def buy_mining_card(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    username = request.POST.get('username')
    mining_id = request.POST.get('mining_id')

    if not username or not mining_id:
        return HttpResponseBadRequest("Username and mining ID are required.")

    # Get the user profile and mining object
    user = get_object_or_404(UserProfile, username=username)
    mining = get_object_or_404(Mining, id=mining_id)



    try:
        # Try to get the existing MiningCard
        card = MiningCard.objects.get(user=user, mining=mining)
        if card:
            bonus_response = get_mining_bonus_into_wallet(request)
            if bonus_response.status_code != 200:
                return bonus_response

        if card.level < 20:
            # Calculate the cost to upgrade
            current_level = card.level
            upgrade_cost = card.calculate_cost()

            # Check if the user has enough funds
            if user.wallet >= upgrade_cost:
                user.wallet -= upgrade_cost
                user.save()
                card.upgrade()
                response = {
                    'status': 'success',
                    'message': f'Card upgraded to level {card.level}',
                    'wallet': float(user.wallet)
                }
            else:
                response = {
                    'status': 'error',
                    'message': 'Insufficient balance to upgrade the card.'
                }
        else:
            response = {
                'status': 'error',
                'message': 'Card is already at maximum level.'
            }
    except MiningCard.DoesNotExist:
        # No existing card; Create a new one
        if user.wallet >= mining.cost:
            user.wallet -= mining.cost
            user.save()
            MiningCard.objects.create(user=user, mining=mining, level=1)
            response = {
                'status': 'success',
                'message': 'Card purchased and upgraded to level 1',
                'wallet': float(user.wallet)
            }
        else:
            response = {
                'status': 'error',
                'message': 'Insufficient balance to buy the mining card.'
            }

    return JsonResponse(response)



def check_mining_card_status(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    username = request.POST.get('username')
    mining_id = request.POST.get('mining_id')

    if not username or not mining_id:
        return HttpResponseBadRequest("Username and mining ID are required.")

    # Get the user profile and mining object
    user = get_object_or_404(UserProfile, username=username)
    mining = get_object_or_404(Mining, id=mining_id)

    try:
        # Try to get the existing MiningCard
        card = MiningCard.objects.get(user=user, mining=mining)
        current_level = card.level

        # Calculate the cost to upgrade to the next level
        if current_level < 20:
            upgrade_cost = card.calculate_cost()
        else:
            upgrade_cost = Decimal('0.0')  # No upgrade cost if already at maximum level

        response = {

            'current_level': current_level,
            'upgrade_cost': float(upgrade_cost)  # Convert Decimal to float for JSON serialization
        }
    except MiningCard.DoesNotExist:
        # No existing card; Provide the initial cost to purchase the card
        initial_cost = mining.cost

        response = {

            'current_level': 0,
            'upgrade_cost': float(initial_cost)  # Convert Decimal to float for JSON serialization
        }

    return JsonResponse(response)

def mining_card_1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(UserProfile, username=username)
        user_mining = MiningCard.objects.filter(user=user).select_related('mining')

        # Fetch all Mining objects
        mining_data = list(
            Mining.objects.filter(category__name='Crypto').values(
                'id', 'name','name_rus', 'picture', 'income_per_hour', 'cost', 'category', 'about', 'about_rus'
            )
        )

        user_mining_data = []
        for mining_card in user_mining:
            mining = mining_card.mining

            income_per_hour_actual = Decimal(mining_card.calculate_income_actual_lvl())
            income_per_hour_next = Decimal(mining_card.calculate_income_next_lvl())


            income_for_card_inside = income_per_hour_next - income_per_hour_actual
            print(income_per_hour_actual,"::::::", income_per_hour_next,"::::::", income_for_card_inside)
            user_mining_data.append({
                'mining__name_eng': mining.name,
                'mining__name_rus': mining.name_rus,
                'level': mining_card.level,
                'cost': float(mining_card.calculate_cost()),  # Convert to float for JSON serialization
                'income_for_card': float(income_per_hour_actual),
                'income_inside_card': float(income_for_card_inside),
            })
        response = {
            'mining': mining_data,
            'user_mining': user_mining_data
        }
        return JsonResponse(response)

def mining_card_2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(UserProfile, username=username)
        user_mining = MiningCard.objects.filter(user=user).select_related('mining')

        # Fetch all Mining objects
        mining_data = list(
            Mining.objects.filter(category__name='Investment').values(
                'id', 'name','name_rus', 'picture', 'income_per_hour', 'cost', 'category', 'about', 'about_rus'
            )
        )

        user_mining_data = []
        for mining_card in user_mining:
            mining = mining_card.mining

            income_per_hour_actual = Decimal(mining_card.calculate_income_actual_lvl())
            income_per_hour_next = Decimal(mining_card.calculate_income_next_lvl())


            income_for_card_inside = income_per_hour_next - income_per_hour_actual
            print(income_per_hour_actual,"::::::", income_per_hour_next,"::::::", income_for_card_inside)
            user_mining_data.append({
                'mining__name_eng': mining.name,
                'mining__name_rus': mining.name_rus,
                'level': mining_card.level,
                'cost': float(mining_card.calculate_cost()),  # Convert to float for JSON serialization
                'income_for_card': float(income_per_hour_actual),
                'income_inside_card': float(income_for_card_inside),
            })

        response = {
            'mining': mining_data,
            'user_mining': user_mining_data
        }
        return JsonResponse(response)

def mining_card_3(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(UserProfile, username=username)
        user_mining = MiningCard.objects.filter(user=user).select_related('mining')

        # Fetch all Mining objects
        mining_data = list(
            Mining.objects.filter(category__name='Business').values(
                'id', 'name','name_rus', 'picture', 'income_per_hour', 'cost', 'category', 'about', 'about_rus'
            )
        )

        user_mining_data = []
        for mining_card in user_mining:
            mining = mining_card.mining

            income_per_hour_actual = Decimal(mining_card.calculate_income_actual_lvl())
            income_per_hour_next = Decimal(mining_card.calculate_income_next_lvl())


            income_for_card_inside = income_per_hour_next - income_per_hour_actual
            print(income_per_hour_actual,"::::::", income_per_hour_next,"::::::", income_for_card_inside)
            user_mining_data.append({
                'mining__name_eng': mining.name,
                'mining__name_rus': mining.name_rus,
                'level': mining_card.level,
                'cost': float(mining_card.calculate_cost()),  # Convert to float for JSON serialization
                'income_for_card': float(income_per_hour_actual),
                'income_inside_card': float(income_for_card_inside),
            })

        response = {
            'mining': mining_data,
            'user_mining': user_mining_data
        }
        return JsonResponse(response)

def mining_card_4(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(UserProfile, username=username)
        user_mining = MiningCard.objects.filter(user=user).select_related('mining')

        # Fetch all Mining objects
        mining_data = list(
            Mining.objects.filter(category__name='Special').values(
                'id', 'name','name_rus', 'picture', 'income_per_hour', 'cost', 'category', 'about', 'about_rus'
            )
        )

        user_mining_data = []
        for mining_card in user_mining:
            mining = mining_card.mining

            income_per_hour_actual = Decimal(mining_card.calculate_income_actual_lvl())
            income_per_hour_next = Decimal(mining_card.calculate_income_next_lvl())


            income_for_card_inside = income_per_hour_next - income_per_hour_actual
            print(income_per_hour_actual,"::::::", income_per_hour_next,"::::::", income_for_card_inside)
            user_mining_data.append({
                'mining__name_eng': mining.name,
                'mining__name_rus': mining.name_rus,
                'level': mining_card.level,
                'cost': float(mining_card.calculate_cost()),  # Convert to float for JSON serialization
                'income_for_card': float(income_per_hour_actual),
                'income_inside_card': float(income_for_card_inside),
            })

        response = {
            'mining': mining_data,
            'user_mining': user_mining_data
        }
        return JsonResponse(response)


def langs(request):

    langButton = {
        'EN': 'EN',
        'RU': 'RU'
    }

    profitPerTap = {
        'EN': 'Profit per tap',
        'RU': 'Доход за тап'
    }
    profitPerHour = {
            'EN': 'Profit per hour',
            'RU': 'Доход в час'
    }
    profit = {
             'EN': 'Profit per hour',
             'RU': 'Доход в час'
    }
    profitPerHourTwo = {
            'EN': 'Profit per hour',
            'RU': 'Доход в час'
    }
    level = {
            'EN': 'Level',
            'RU': 'Уровень'
    }
    miningClaim = {
            'EN': 'Mining',
            'RU': 'Майнинг'
    }
    claimButton = {
            'EN': 'Claim',
            'RU': 'Получить'
    }
    doneButton = {
             'EN': 'Done',
             'RU': 'Готово'
    }
    startButton = {
             'EN': 'Start',
             'RU': 'Начать'
    }
    game = {
            'EN': 'Game',
            'RU': 'Главная'
    }
    mine = {
            'EN': 'Mine',
            'RU': 'Майнинг'
    }
    tasks = {
            'EN': 'Tasks',
            'RU': 'Задания'
    }
    friends = {
            'EN': 'Friends',
            'RU': 'Друзья'
    }
    crypto = {
            'EN': 'Crypto',
            'RU': 'Крипта'
    }
    investment = {
            'EN': 'Investment',
            'RU': 'Инвестиции'
    }
    business = {
            'EN': 'Business',
            'RU': 'Бизнес'
    }
    special = {
            'EN': 'Special',
            'RU': 'Особое'
    }
    earnMoreCoins = {
            'EN': 'Earn more coins',
            'RU': 'Заработай больше монет'
    }
    dailyTasks = {
            'EN': 'Daily tasks',
            'RU': 'Ежедневные задания'
    }
    specialTasks = {
            'EN': 'Special tasks',
            'RU': 'Особые задания'
    }
    dailyReward = {
            'EN': 'Daily reward',
            'RU': 'Награда дня'
    }
    inviteFriends = {
            'EN': 'Invite friends',
            'RU': 'Приглашай друзей'
    }
    inviteFriendsButton = {
            'EN': 'Invite friends',
            'RU': 'Приглашай друзей'
    }
    invitePoster = {
            'EN': 'Invite a friend',
            'RU': 'Пригласи друга'
    }
    invitePosterDesc = {
            'EN': 'for you and your friend',
            'RU': 'для тебя и твоего друга'
    }
    extraProfit = {
            'EN': 'Extra profit from friends',
            'RU': 'Дополнительный доход от друзей'
    }
    extraProfitDesc = {
            'EN': 'Score 2% coins from your friend',
            'RU': 'Получайте 2% монет от друга'
    }
    profitFromFriends = {
            'EN': 'Profit from your friends',
            'RU': 'Доход с ваших друзей'
    }
    friendsContainerHeader = {
            'EN': 'List of your friends',
            'RU': 'Список ваших друзей'
    }
    boostButton = {
            'EN': 'Boost',
            'RU': 'Буст'
    }
    turbo = {
            'EN': 'Turbo',
            'RU': 'Турбо'
    }
    fullEnergy = {
            'EN': 'Full energy',
            'RU': 'Пополнение энергии'
    }
    multitap = {
            'EN': 'Multitap',
            'RU': 'Мультитап'
    }
    energyLimit = {
            'EN': 'Energy Limit',
            'RU': 'Лимит энергии'
    }
    turboDesc = {
            'EN': 'Increase the amount of coins you get per tap (per 30 sec. x5 per your tap level)',
            'RU': 'Увеличьте количество монет, которые вы получаете за нажатие (на 30 сек. x5 за каждый уровень нажатия).'
    }
    fullEnergyDesc = {
            'EN': 'Recharge your energy to the maximum and do extra taps',
            'RU': 'Зарядитесь энергией до максимума и делайте дополнительные нажатия'
    }
    multitapDesc = {
            'EN': 'Increase the amount of coins you ger per tap (+1 per tap for each level)',
            'RU': 'Увеличьте количество монет, которые вы получаете за нажатие (+1 за нажатие за каждый уровень).'
    }
    energyLimitDesc = {
            'EN': 'Increase the limit of energy storage (+500 energy for each level)',
            'RU': 'Увеличить лимит хранения энергии (+500 энергии за каждый уровень)'
    }
    miningwayp = {
            'EN': 'Mining',
            'RU': 'Майнинг'
    }
    taskswayp = {
            'EN': 'Tasks',
            'RU': 'Задания'
    }
    nftwayp = {
            'EN': 'NFT Launch',
            'RU': 'Запуск NFT'
    }
    tokenwayp = {
            'EN': 'Token Presale',
            'RU': 'Предпродажа токенов'
    }
    listingwayp = {
            'EN': 'Listing',
            'RU': 'Листинг'
    }
    gameswayp = {
            'EN': 'Jungle Games and Development',
            'RU': 'Jungle Games и Разработка'
    }
    connectTON = {
            'EN': 'Connect your TON wallet',
            'RU': 'Подключите свой TON-кошелек'
    }
    connectExchange = {
            'EN': 'Connect the exchange',
            'RU': 'Подключитесь к бирже'
    }
    soonButton = {
            'EN': 'Soon',
            'RU': 'Скоро'
    }
    totalTouchers = {
            'EN': 'Total touchers',
            'RU': 'Всего активных игроков'
    }
    totalPPH = {
            'EN': 'Total Profit per Hour',
            'RU': 'Общая прибыль в час'
    }
    totalPlayers = {
            'EN': 'Total players',
            'RU': 'Всего игроков'
    }
    soonContainer = {
            'EN': 'Coming soon',
            'RU': 'Скоро'
    }
    preyOfThePride = {
            'EN': 'Prey of the pride',
            'RU': 'Добыча прайда'
    }
    totalHeader = {
            'EN': 'Total Share Balance',
            'RU': 'Общий баланc'
    }
    tasksList = {
            'EN': 'Tasks list',
            'RU': 'Список заданий'
    }
    timer = {
            'EN': 'You can claim your bonus now!',
            'RU': 'Вы можете получить бонус прямо сейчас!'
    }
    combined_data = {
        'langButton': langButton,
        'profitPerHour': profitPerHour,
        'profit': profit,
        'profitPerHourTwo': profitPerHourTwo,
        'profitPerTap': profitPerTap,
        'level': level,
        'miningClaim': miningClaim,
        'claimButton': claimButton,
        'doneButton': doneButton,
        'game': game,
        'mine': mine,
        'tasks': tasks,
        'friends': friends,
        'crypto': crypto,
        'investment': investment,
        'business': business,
        'special': special,
        'startButton': startButton,
        'earnMoreCoins': earnMoreCoins,
        'dailyTasks': dailyTasks,
        'specialTasks': specialTasks,
        'dailyReward': dailyReward,
        'inviteFriends': inviteFriends,
        'inviteFriendsButton': inviteFriendsButton,
        'invitePoster': invitePoster,
        'invitePosterDesc': invitePosterDesc,
        'extraProfit': extraProfit,
        'extraProfitDesc': extraProfitDesc,
        'profitFromFriends': profitFromFriends,
        'friendsContainerHeader': friendsContainerHeader,
        'boostButton': boostButton,
        'turbo': turbo,
        'fullEnergy': fullEnergy,
        'multitap': multitap,
        'energyLimit': energyLimit,
        'turboDesc': turboDesc,
        'fullEnergyDesc': fullEnergyDesc,
        'multitapDesc': multitapDesc,
        'energyLimitDesc': energyLimitDesc,
        'miningwayp': miningwayp,
        'taskswayp': taskswayp,
        'nftwayp': nftwayp,
        'tokenwayp': tokenwayp,
        'listingwayp': listingwayp,
        'gameswayp': gameswayp,
        'connectTON': connectTON,
        'connectExchange': connectExchange,
        'soonButton': soonButton,
        'soonContainer': soonContainer,
        'preyOfThePride': preyOfThePride,
        'totalTouchers': totalTouchers,
        'totalPPH': totalPPH,
        'totalPlayers': totalPlayers,
        'totalHeader': totalHeader,
        'tasksList': tasksList,
        'timer': timer
    }


    return JsonResponse(combined_data)


def get_slot_spin_result(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        result_1 = request.POST.get('result_1')
        result_2 = request.POST.get('result_2')
        result_3 = request.POST.get('result_3')
        user = get_object_or_404(UserProfile, username=username)



        score = 0

        if result_1 == result_2 == result_3 == 'seven':
            score = 1000
        elif result_1 == result_2 == result_3 == 'melon':
            score = 100
        elif result_1 == result_2 == result_3 == 'berry':
            score = 50

        elif (result_1 == 'seven' and result_2 == 'seven') or (result_1 == 'seven' and result_3 == 'seven') or (
                result_2 == 'seven' and result_3 == 'seven'):
            score = 50
        elif (result_1 == 'melon' and result_2 == 'melon') or (result_1 == 'melon' and result_3 == 'melon') or (
                result_2 == 'melon' and result_3 == 'melon'):
            score = 20
        elif (result_1 == 'berry' and result_2 == 'berry') or (result_1 == 'berry' and result_3 == 'berry') or (
                result_2 == 'berry' and result_3 == 'berry'):
            score = 10
        print(score)
        user.wallet += score

        user.save()

        response = {

        }


        return JsonResponse(response)


    return JsonResponse({})

    return JsonResponse(response)

def get_wheel_spin_result(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(UserProfile, username=username)

        # Get the result from POST and convert it to an integer
        result = request.POST.get('result')
        try:
            result = int(result)  # Or float(result) if it's a decimal
        except ValueError:
            return JsonResponse({'error': 'Invalid result value'}, status=400)

        # Add the result to the user's wallet
        user.wallet += result

        # Save the updated user profile
        user.save()

        response = {
            'username': username,
            'wallet': user.wallet
        }

        return JsonResponse(response)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



