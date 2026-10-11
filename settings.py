from os import environ

SESSION_CONFIGS = [
    dict(
        name='ai_search',
        display_name='AI Product-Search Study (equal arms: use 69 or 72)',
        num_demo_participants=3,
        app_sequence=['ai_search'],
        require_equal_arms=True,
        task_seconds=240,        # 4 minutes per scored task
        practice_seconds=180,    # 3 minutes for the practice task
        ai_url='https://chatgpt.com/',
    ),
]

# Explicit option for a class of exactly 70; counts differ by at most one.
SESSION_CONFIGS.append(dict(SESSION_CONFIGS[0], name='ai_search_70',
    display_name='AI Product-Search Study (70 students: 24/23/23)',
    num_demo_participants=70, require_equal_arms=False))

# Payment shown on the completion page (planning amounts from the proposal).
# Bonus is paid later, after reviewers verify answers; oTree does not compute it.
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=5.00,
    bonus_per_correct=0.50,
    max_total_pay=6.50,
    doc="",
)

PARTICIPANT_FIELDS = ['seed', 'battery', 'arm', 'consented', 'excluded']
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'change-me-before-class')

ROOMS = [
    dict(name='classroom', display_name='AI Search Study - Classroom'),
]

INSTALLED_APPS = ['otree']
