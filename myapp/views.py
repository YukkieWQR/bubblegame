from .models import *
from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile


def index(request):
    username = request.GET.get('username')

    context = {}



    if username:
        user, created = UserProfile.objects.get_or_create(username=username)

        # Update energy limit based on the user's energy_limit_level



        context['user'] = user


        context['referral_link'] = None


    return render(request, 'index.html', context)



def index_referral(request):
    username = request.GET.get('username')

    invitor_username = request.GET.get('invitor')
    context = {}


    if username and invitor_username:
        user, created = UserProfile.objects.get_or_create(username=username)
        invitor, invitor_created = UserProfile.objects.get_or_create(username=invitor_username)
        user.regenerate_energy()

        if not user.invited_by:

            user.invited_by = invitor.username
            invitor.users_invited += f"{username},"
            user.save()
            invitor.save()

        # Update energy limit based on the user's energy_limit_level

        user.save()


        context['user'] = user


        context['referral_link'] = None


    return render(request, 'index.html', context)


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


        # Convert users_invited to a list if it's stored as JSON string
        if isinstance(user.users_invited, str):
            # Remove any leading or trailing commas and split the string by commas
            users_invited = user.users_invited.strip().split(',')

            # Remove any leading/trailing whitespace from each item and enclose in double quotes

        user_tasks = TaskUser.objects.filter(user=user).select_related('task')
        task_data = list(Task.objects.all().values('id', 'name', 'cost', 'picture'))
        task_timer_data = list(Task_Timer.objects.all().values('id', 'name', 'cost', 'picture'))

        level = user.level
        userlevelname = level_names.get(level, 'Unknown')
        users_invited = user.users_invited
        users_invited = users_invited.split(',')
        users_invited = [invited_user for invited_user in users_invited if invited_user]

        if len(users_invited) > 3 and user.recieved_threefriends_reward == False:
            can_recieve_3fr_reward = True
        else:
            can_recieve_3fr_reward = False
        if user.recieved_threefriends_reward == True:
            recieved_threefriends_reward = True
        else:
            recieved_threefriends_reward = False
        response_data = {

            'user': user.username,
            'userlevelname': userlevelname,

            'new_wallet': user.wallet,
            'new_energy_limit_level': user.energy_limit_level,
            'new_energy': user.energy,
            'energy': user.energy,
            'new_level': user.level,

            'tasks': task_data,
            'task_timer': task_timer_data,

            'user_tasks': list(user_tasks.values('task__name', 'status')),
            'users_invited': users_invited,
            'recieved_threefriends_reward' : user.recieved_threefriends_reward,
            'can_recieve_3fr_reward': user.can_recieve_3fr_reward,
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


def update_task_timer_status(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        task_pk = request.POST.get('task_pk')

        user = get_object_or_404(UserProfile, username=username)
        task = get_object_or_404(Task_Timer, pk=task_pk)

        task_user, created = TaskUser_Timer.objects.get_or_create(user=user, task=task)

        if created:
            now = timezone.now()
            task_user.timer = now
            task_user.timer.save()
            task_user.status_change()
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


def update_task_timer_status_bool(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        task_pk = request.POST.get('task_pk')

        # Get or create the user
        user = get_object_or_404(UserProfile, username=username)

        # Get or create the task
        task, created = Task_Timer.objects.get_or_create(pk=task_pk)

        # Get or create the task-user relationship
        task_user, created_task_user = TaskUser_Timer.objects.get_or_create(user=user, task=task)
        last_called = task_user.timer

        # If the task-user relationship was just created, return active as True
        if created_task_user:
            return JsonResponse({'active': True})

        # Update task_user status
        task_user.status_change()
        if task_user.status == 3:  # Status 'Done'
            user.wallet += task.cost
            user.save()

        task_user.save()

        # Calculate the hours passed since the last timer call
        now = timezone.now()
        hours_passed = Decimal((now - last_called).total_seconds() / 3600)

        # Check if 12 hours have passed
        if hours_passed >= 12:
            return JsonResponse({'active': True})
        else:
            return JsonResponse({'active': False})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

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
    username = request.POST.get('username')

    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if not user.users_invited:
        return JsonResponse({'username': user.username, 'invited_users_wallets_sum': 0, 'bonus': 0, 'depth_lists': []})

    # Get depth lists
    depth_lists = user.get_depth_lists()

    # Debugging output

    if not all(isinstance(level, list) for level in depth_lists):
        return JsonResponse({'error': 'Invalid format for depth_lists'}, status=500)

    # Calculate the sum of the wallets of invited users
    invited_usernames = [u.strip() for u in user.users_invited.split(',')]

    # Define bonus multipliers by depth level
    bonus_multipliers = {
        0: Decimal('0.40'),  # Index 0 corresponds to level 1
        1: Decimal('0.20'),  # Index 1 corresponds to level 2
        2: Decimal('0.10'),  # Index 2 corresponds to level 3
        3: Decimal('0.05'),  # Index 3 corresponds to level 4
        4: Decimal('0.02'),  # Index 4 corresponds to level 5
        5: Decimal('0.01'),  # Index 5 corresponds to level 6
    }

    # Calculate the bonus
    bonus = Decimal('0.00')
    for level_index, usernames in enumerate(depth_lists):
        multiplier = bonus_multipliers.get(level_index, Decimal('0.00'))
        for username in usernames:
            # Assuming the wallet of each user in the depth list is considered for bonus calculation
            user_wallet = UserProfile.objects.filter(username=username).values_list('wallet', flat=True).first()
            if user_wallet:
                bonus += multiplier * Decimal(user_wallet)

    # Prepare the response data
    response_data = {
        'username': user.username,
        'bonus': float(bonus),
        'depth_lists': depth_lists,
    }

    return JsonResponse(response_data)


def get_user_bonus_into_wallet(request):
    username = request.POST.get('username')

    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if not user.users_invited:
        return JsonResponse({'username': user.username, 'invited_users_wallets_sum': 0, 'bonus': 0, 'depth_lists': []})

    # Get depth lists
    depth_lists = user.get_depth_lists()

    # Debugging output

    if not all(isinstance(level, list) for level in depth_lists):
        return JsonResponse({'error': 'Invalid format for depth_lists'}, status=500)

    # Calculate the sum of the wallets of invited users
    invited_usernames = [u.strip() for u in user.users_invited.split(',')]
    invited_users = UserProfile.objects.filter(username__in=invited_usernames)

    # Define bonus multipliers by depth level
    bonus_multipliers = {
        0: Decimal('0.40'),  # Index 0 corresponds to level 1
        1: Decimal('0.20'),  # Index 1 corresponds to level 2
        2: Decimal('0.10'),  # Index 2 corresponds to level 3
        3: Decimal('0.05'),  # Index 3 corresponds to level 4
        4: Decimal('0.02'),  # Index 4 corresponds to level 5
        5: Decimal('0.01'),  # Index 5 corresponds to level 6
    }

    # Calculate the bonus
    bonus = Decimal('0.00')
    for level_index, usernames in enumerate(depth_lists):
        multiplier = bonus_multipliers.get(level_index, Decimal('0.00'))
        for username in usernames:
            # Assuming the wallet of each user in the depth list is considered for bonus calculation
            user_wallet = UserProfile.objects.filter(username=username).values_list('wallet', flat=True).first()
            if user_wallet:
                bonus += multiplier * Decimal(user_wallet)


    # user.highest_invited_wallets_sum = bonus
    user.wallet += bonus
    user.save()

    response_data = {
        'username': user.username,
        'bonus': float(bonus),
        'depth_lists': depth_lists,
    }

    return JsonResponse(response_data)


# def get_user_bonus_into_wallet(request):
#     if request.method != 'POST':
#         return HttpResponseBadRequest("Invalid request method.")
#
#     username = request.POST.get('username')
#     if not username:
#         return HttpResponseBadRequest("Username is required.")
#
#     try:
#         user = UserProfile.objects.get(username=username)
#     except UserProfile.DoesNotExist:
#         return JsonResponse({'error': 'User not found.'}, status=404)
#
#     if not user.users_invited:
#         return JsonResponse({'username': user.username, 'invited_users_wallets_sum': 0, 'bonus': 0})
#
#     # Split the users_invited field to get individual usernames, and strip any surrounding whitespace
#     invited_usernames = [u.strip() for u in user.users_invited.split(',')]
#     invited_users = UserProfile.objects.filter(username__in=invited_usernames)
#
#     # Calculate the sum of the wallets of invited users
#     total_wallets_sum = sum(Decimal(invited_user.wallet) for invited_user in invited_users)
#
#     # Calculate the bonus based on the highest invited wallets sum
#     bonus = Decimal(0)
#     if total_wallets_sum > user.highest_invited_wallets_sum:
#         bonus = (total_wallets_sum - user.highest_invited_wallets_sum) * Decimal('0.02')
#         user.highest_invited_wallets_sum = total_wallets_sum
#         user.wallet += bonus
#         user.save()
#
#     # Prepare the response data
#     response_data = {
#         'username': user.username,
#         'invited_users_wallets_sum': float(total_wallets_sum),
#         'bonus': float(bonus)
#     }
#
#     return JsonResponse(response_data)


def three_friends_task(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if not username:
            return JsonResponse({'error': 'Username not provided'}, status=400)

        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        users_invited = user.users_invited
        users_invited = users_invited.split(',')
        users_invited = [invited_user for invited_user in users_invited if invited_user]

        if len(users_invited) > 3:
            user.wallet + 3333

            status = True
        else:
            status = False

        return JsonResponse({
            'status': status
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)








def get_bonus(request):
    username = request.POST.get('username')

    user = UserProfile.objects.select_for_update().get(username=username)

    now = timezone.now()
    last_daily_bonus = user.last_daily_bonus

    if last_daily_bonus is None:
        last_bonus_time = now
        user.last_daily_bonus = now
        user.save()
    else:
        last_bonus_time = last_daily_bonus

    hours_passed = Decimal((now - last_bonus_time).total_seconds() / 3600)

    # Bonus calculation logic
    total_bonus = Decimal(333)  # Total bonus for 12 hours
    income_per_hour = total_bonus / 12  # Calculate bonus per hour
    accumulated_bonus = income_per_hour * hours_passed  # Calculate accumulated bonus

    if hours_passed >= 12:
        status = True
        time_until_next_bonus = 0
        accumulated_bonus = total_bonus  # Cap the bonus at the total if 12 or more hours have passed
    else:
        status = False
        time_until_next_bonus = 12 - hours_passed

    # Prepare the response data
    response_data = {
        'status': status,
        'income_per_hour': float(accumulated_bonus),  # Accumulated bonus
        'time_until_active': float(time_until_next_bonus),  # Convert to float for JSON serialization
    }

    return JsonResponse(response_data)



def get_daily_bonus_into_wallet(request):
    username = request.POST.get('username')

    try:
        user = UserProfile.objects.select_for_update().get(username=username)
        user.wallet += 333  # Add 333 to the user's wallet
        now = timezone.now()
        user.last_daily_bonus = now
        user.save()

        response_data = {
            'now': now,
        }

        return JsonResponse(response_data)

    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_3fr_bonus_into_wallet(request):
    username = request.POST.get('username')

    try:
        user = UserProfile.objects.select_for_update().get(username=username)
        user.wallet + 3333
        user.recieved_threefriends_reward = True

        user.save

        response_data = {
            'username': username,
        }

        return JsonResponse(response_data)

    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def hour_task(request):
    username = request.POST.get('username')

    try:
        user = UserProfile.objects.select_for_update().get(username=username)
        link = "https://www.youtube.com/"

        now = timezone.now()
        last_12h_task = user.last_12h_task

        if last_12h_task is None:
            last_bonus_time = now
            user.last_12h_task = now
            user.save()
        else:
            last_bonus_time = last_12h_task

        hours_passed = Decimal((now - last_bonus_time).total_seconds() / 3600)

        if hours_passed >= 12:
            status = True
            bonus = 300
            user.wallet += bonus  # Add bonus to the wallet
            user.last_12h_task = now
            time_until_next_bonus = 0
            user.save()
        else:
            status = False
            bonus = 0
            time_until_next_bonus = 12 - hours_passed

        response_data = {
            'status': status,
            'bonus': bonus,
            'time_until_next_bonus': time_until_next_bonus,
            'link': link
        }

        return JsonResponse(response_data)

    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

