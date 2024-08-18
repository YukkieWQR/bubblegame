from django.db import models
from django.utils import timezone
import uuid


class UserProfile(models.Model):
    LEVELS = [
        (1, 'Bronze'),
        (2, 'Silver'),
        (3, 'Gold'),
        (4, 'Platinum'),
        (5, 'Diamond'),
        (6, 'Master'),
        (7, 'Grandmaster'),
        (8, 'Elite'),
        (9, 'Legendary'),
        (10, 'The King'),
    ]

    username = models.CharField(max_length=20, unique=True)
    wallet = models.DecimalField(max_digits=20, decimal_places=2, default=1)
    level = models.IntegerField(default=1)
    energy = models.IntegerField(default=1000)

    energy_limit = models.IntegerField(default=1000)
    multitap_level = models.IntegerField(default=1)
    tap_efficiency = models.IntegerField(default=1)
    energy_limit_level = models.IntegerField(default=1)
    last_energy_update = models.DateTimeField(default=timezone.now)
    invited_by = models.TextField(null=True, blank=True)
    users_invited = models.TextField(default="", null=True, blank=True)
    highest_invited_wallets_sum = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    last_daily_bonus = models.DateTimeField(null=True, blank=True)
    daily_energy_last_daily_bonus = models.DateTimeField(null=True, blank=True)
    daily_turbo_last_daily_bonus = models.DateTimeField(null=True, blank=True)
    last_mining_bonus = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.username

    def check_level_up(self):
        level_requirements = {
            2: 50000,
            3: 100000,
            4: 500000,
            5: 1000000,
            6: 5000000,
            7: 10000000,
            8: 50000000,
            9: 100000000,
            10: 1000000000,
        }

        next_level = self.level + 1

        if next_level in level_requirements and self.wallet >= level_requirements[next_level]:
            self.level = next_level
            self.tap_efficiency += 1
            self.energy += 500
            self.save()
            return True
        return False

    def multitap_upgrade_cost(self):
        return 1000 * (2 ** (self.multitap_level - 1))

    def purchase_multitap(self):
        cost = self.multitap_upgrade_cost()
        if self.wallet >= cost and self.multitap_level < 20:
            self.wallet -= cost
            self.multitap_level += 1
            self.tap_efficiency += 1
            self.save()
            return True
        return False

    def energy_upgrade_cost(self):
        return 1000 * (2 ** (self.energy_limit_level - 1))

    def purchase_energy_limit(self):
        cost = self.energy_upgrade_cost()
        if self.wallet >= cost and self.energy_limit_level < 20:
            self.wallet -= cost
            self.energy_limit_level += 1
            self.energy += 500
            self.energy_limit = min(10500, 1000 + (self.energy_limit_level - 1) * 500)
            self.save()
            return True
        return False

    def regenerate_energy(self):
        now = timezone.now()
        elapsed_seconds = (now - self.last_energy_update).total_seconds()
        new_energy = self.energy + int(elapsed_seconds)

        # Calculate energy limit based on energy_limit_level
        self.energy_limit = (1000 + (self.energy_limit_level - 1) * 500 + (self.level * 500))

        if new_energy > self.energy_limit:
            new_energy = self.energy_limit

        self.energy = new_energy
        self.last_energy_update = now
        self.save()






    def set_energy_to_limit(self):
        """Sets the energy value to the energy_limit value."""
        self.energy = self.energy_limit
        self.save()

    @property
    def next_multitap_upgrade_cost(self):
        if self.multitap_level < 20:
            return self.multitap_upgrade_cost()
        return None  # or some indication that the level cap has been reached

    @property
    def next_energy_upgrade_cost(self):
        if self.energy_limit_level < 20:
            return self.energy_upgrade_cost()
        return None  # or some indication that the level cap has been reached

    @property
    def max_multitap_level_reached(self):
        return self.multitap_level >= 20

    @property
    def max_energy_level_reached(self):
        return self.energy_limit_level >= 20

    @property
    def next_energy_level(self):
        return min(self.energy_limit_level, 20)

    def calculate_bonus(self):
        if not self.users_invited:
            return 0

        invited_usernames = self.users_invited.split(', ')
        invited_users = UserProfile.objects.filter(username__in=invited_usernames)
        total_wallets_sum = sum(user.wallet for user in invited_users)

        if total_wallets_sum > self.highest_invited_wallets_sum:
            bonus = (total_wallets_sum - self.highest_invited_wallets_sum) * 0.02
            self.highest_invited_wallets_sum = total_wallets_sum
            self.save()
            return bonus
        return 0

    def apply_bonus(self):
        bonus = self.calculate_bonus()
        if bonus > 0:
            self.wallet += bonus
            self.save()
        return bonus

from decimal import Decimal




class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Mining(models.Model):
    name = models.CharField(max_length=50)
    name_rus = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='myapp/static/mining_pictures')
    income_per_hour = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_2 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_3 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_4 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_5 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_6 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_7 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_8 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_9 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_10 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_11 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_12 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_13 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_14 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_15 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_16 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_17 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_18 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_19 = models.DecimalField(max_digits=100, decimal_places=2)
    income_per_hour_20 = models.DecimalField(max_digits=100, decimal_places=2)


    cost = models.DecimalField(max_digits=100, decimal_places=2)
    cost_2 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_3 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_4 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_5 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_6 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_7 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_8 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_9 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_10 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_11 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_12 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_13 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_14 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_15 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_16 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_17 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_18 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_19 = models.DecimalField(max_digits=100, decimal_places=2)
    cost_20 = models.DecimalField(max_digits=100, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    about = models.TextField(max_length=50)
    about_rus = models.TextField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.category.name}"

class MiningCard(models.Model):


    mining = models.ForeignKey(Mining, on_delete=models.CASCADE)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)





    def calculate_cost(self):
        if 1 <= self.level <= 20:
            cost_field = f'cost_{self.level + 1}'
            return getattr(self.mining, cost_field)
        else:
            return self.mining.cost

    def calculate_income_actual_lvl(self):
        if 1 <= self.level <= 20:
            income_per_hour_field = f'income_per_hour_{self.level}'
            return getattr(self.mining, income_per_hour_field, self.mining.income_per_hour)
        else:
            return self.mining.income_per_hour

    def calculate_income_next_lvl(self):
        if 1 <= self.level < 20:
            income_per_hour_field = f'income_per_hour_{self.level + 1}'
            return getattr(self.mining, income_per_hour_field, self.mining.income_per_hour)
        else:
            return self.mining.income_per_hour


    def calculate_total_income(self):
        total_income = Decimal('0.0')
        for lvl in range(1, self.level + 1):
            self.level = lvl
            total_income += self.calculate_additional_income()
        self.level -= self.level
        return total_income

    def upgrade(self):
        if self.level < 20:
            self.level += 1
            self.save()

    def __str__(self):
        return f"{self.mining.name} - Level {self.level}"

class Task(models.Model):
    name = models.CharField(max_length=50, unique=True)
    picture = models.ImageField(upload_to='myapp/static/task_pictures/')
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.name

class TaskUser(models.Model):
    STATUSES = [
        (1, 'Start'),
        (2, 'Claim'),
        (3, 'Done'),
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUSES, default=1)

    def __str__(self):
        return f"{self.user.username} - {self.task.name}"

    def status_change(self):
        self.status = (self.status % 3) + 1
        self.save()

class Referral(models.Model):
    referrer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    invited = models.CharField(max_length=20, null=True, blank=True)
