from os import environ

SESSION_CONFIGS = [
    dict(
        name='ai_search',
        display_name='AI Product-Search Study (classroom)',
        num_demo_participants=4,
        app_sequence=['ai_search'],
        task_seconds=240,        # 4 minutes per scored task
        practice_seconds=180,    # 3 minutes for the practice task
        ai_url='https://chatgpt.com/',
    ),
]

# Payment shown on the completion page (planning amounts from the proposal).
# Bonus is paid later, after reviewers verify answers; oTree does not compute it.
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=5.00,
    bonus_per_correct=0.50,
    max_total_pay=8.00,
    doc="",
)

PARTICIPANT_FIELDS = ['seed', 'battery', 'arm', 'consented', 'excluded']
SESSION_FIELDS = ['blocks', 'block_counts']

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
