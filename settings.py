from os import environ

# ------------------------------------------------------------------
# Session configurations
# ------------------------------------------------------------------
SESSION_CONFIGS = [
    dict(
        name='ai_search',
        display_name='AI Product-Search Study',
        num_demo_participants=8,
        app_sequence=['ai_search'],
    ),
]

# Real participants (Prolific)
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=8.00,       # base payment ($USD)
    doc="",
)

# ------------------------------------------------------------------
# Language / currency
# ------------------------------------------------------------------
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

# ------------------------------------------------------------------
# Admin / secrets
# ------------------------------------------------------------------
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'admin')
SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'change-me-in-production')

# ------------------------------------------------------------------
# Rooms (create at least one for Prolific hand-off)
# ------------------------------------------------------------------
ROOMS = [
    dict(
        name='prolific',
        display_name='Prolific — AI Search Study',
        participant_label_file='_rooms/prolific.txt',
    ),
]

INSTALLED_APPS = ['otree']
