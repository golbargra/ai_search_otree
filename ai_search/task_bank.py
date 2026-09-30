"""
Task bank for the AI product-search experiment (proposal Section 5).

Each participant gets 6 scored tasks: one per category, so 2 easy,
2 medium and 2 hard. Individualization comes from a FINITE, PRECHECKED
list of parameter variants per category (no free random numbers).
Task order is shuffled. The seed is saved so everything is reproducible.

>>> BEFORE CLASS: check every variant below on the live web and delete
>>> any variant that does not have several qualifying offers.
"""
import random

# Each variant: (price_min, price_max, min_rating, min_ratings_count)
CATEGORIES = [
    dict(template_id='mouse', category='Wireless mouse', difficulty='easy',
         attribute=None,
         variants=[(15, 35, 4.0, 100), (20, 40, 4.0, 150), (15, 30, 4.1, 100)]),
    dict(template_id='kettle', category='Electric kettle', difficulty='easy',
         attribute=None,
         variants=[(25, 55, 4.0, 200), (30, 60, 4.1, 200), (25, 50, 4.0, 300)]),
    dict(template_id='headphones', category='Wireless headphones', difficulty='medium',
         attribute='Has a built-in microphone',
         variants=[(40, 80, 4.2, 200), (45, 85, 4.2, 250), (40, 75, 4.3, 200)]),
    dict(template_id='backpack', category='Laptop backpack', difficulty='medium',
         attribute='Fits a 15.6-inch laptop',
         variants=[(30, 60, 4.2, 150), (35, 65, 4.2, 200), (30, 55, 4.3, 150)]),
    dict(template_id='vacuum', category='Cordless vacuum', difficulty='hard',
         attribute='Stated weight under 6 lb',
         variants=[(70, 120, 4.3, 300), (75, 125, 4.3, 350), (70, 115, 4.4, 300)]),
    dict(template_id='speaker', category='Portable speaker', difficulty='hard',
         attribute='Stated IPX7 water-resistance rating',
         variants=[(35, 65, 4.3, 300), (40, 70, 4.3, 350), (35, 60, 4.4, 300)]),
]

PRACTICE_TASK = dict(
    task_id='PRACTICE', template_id='practice', category='USB-C phone charger',
    difficulty='practice', price_min=10, price_max=25, min_rating=4.0,
    min_ratings_count=100, attribute='At least 20W output',
)

N_SCORED_TASKS = len(CATEGORIES)  # 6


def make_task(cat, variant_index):
    pmin, pmax, rating, count = cat['variants'][variant_index]
    return dict(
        task_id=f"{cat['template_id']}_v{variant_index + 1}",
        template_id=cat['template_id'],
        category=cat['category'],
        difficulty=cat['difficulty'],
        price_min=pmin, price_max=pmax,
        min_rating=rating, min_ratings_count=count,
        attribute=cat['attribute'],
    )


def build_battery(seed):
    """One task per category (variant picked at random), shuffled order."""
    rng = random.Random(seed)
    tasks = [make_task(c, rng.randrange(len(c['variants']))) for c in CATEGORIES]
    rng.shuffle(tasks)
    return tasks


def requirements_list(task):
    """Human-readable requirement lines shown to participants (and exported)."""
    reqs = [
        f"Category: {task['category']} (new, not used or refurbished)",
        f"Price: ${task['price_min']} to ${task['price_max']} (item price before shipping and tax)",
        f"Rating: at least {task['min_rating']} out of 5 stars",
        f"At least {task['min_ratings_count']} customer ratings",
        "In stock (can be ordered now; not preorder or backorder)",
    ]
    if task.get('attribute'):
        reqs.append(task['attribute'])
    return reqs
