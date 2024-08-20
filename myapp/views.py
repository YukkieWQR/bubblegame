from .models import *
from django.shortcuts import render
from .models import UserProfile
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

            'next_energy_level': min(user.multitap_level, 20),

            'tasks': task_data,
            'user_tasks': list(user_tasks.values('task__name', 'status')),
            'users_invited': users_invited,
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

