"""
Task bank for the AI Product-Search experiment.

INDIVIDUALIZED tasks: parameters drawn stochastically per participant.
ANCHOR tasks: identical parameter sets across ALL participants — used for
              H7 (choice concentration and product overlap).

All tasks are constrained-product-search:
   Find one currently-for-sale product meeting every listed constraint.
"""
import random

# ---------------------------------------------------------------------
# TASK TEMPLATES (individualized). Each entry is a category with
# parameter ranges the platform samples from at task-assignment time.
# ---------------------------------------------------------------------
TEMPLATES = [
    dict(category="cordless vacuum",
         price=(50, 120), min_rating=(3.9, 4.3),
         min_reviews=(150, 400), difficulty="medium"),
    dict(category="wireless headphones",
         price=(30, 100), min_rating=(4.0, 4.4),
         min_reviews=(500, 2000), difficulty="easy"),
    dict(category="office chair",
         price=(100, 250), min_rating=(4.0, 4.4),
         min_reviews=(200, 800), difficulty="medium"),
    dict(category="electric kettle",
         price=(20, 60), min_rating=(4.1, 4.5),
         min_reviews=(300, 1500), difficulty="easy"),
    dict(category="running shoes (men's)",
         price=(60, 140), min_rating=(4.0, 4.4),
         min_reviews=(100, 500), difficulty="medium"),
    dict(category="mechanical keyboard",
         price=(70, 180), min_rating=(4.1, 4.5),
         min_reviews=(200, 1200), difficulty="hard"),
    dict(category="portable projector",
         price=(120, 400), min_rating=(3.8, 4.3),
         min_reviews=(100, 600), difficulty="hard"),
    dict(category="air fryer",
         price=(50, 130), min_rating=(4.2, 4.6),
         min_reviews=(1000, 5000), difficulty="easy"),
]

# ---------------------------------------------------------------------
# ANCHOR TASKS — identical across all participants.
# Selected to guarantee ≥ 5 feasible products at any given snapshot.
# ---------------------------------------------------------------------
ANCHORS = [
    dict(task_id="ANCHOR_1", category="wireless headphones",
         price_min=40, price_max=80, min_rating=4.0, min_reviews=1000,
         difficulty="easy"),
    dict(task_id="ANCHOR_2", category="cordless vacuum",
         price_min=60, price_max=100, min_rating=4.0, min_reviews=250,
         difficulty="medium"),
    dict(task_id="ANCHOR_3", category="mechanical keyboard",
         price_min=80, price_max=140, min_rating=4.2, min_reviews=500,
         difficulty="hard"),
]

N_INDIVIDUALIZED_PER_BATTERY = 7
N_ANCHOR_PER_BATTERY = 3
N_TASKS_PER_BATTERY = N_INDIVIDUALIZED_PER_BATTERY + N_ANCHOR_PER_BATTERY


def sample_individualized_task(seed=None):
    """Draw a single individualized task from the templates."""
    rng = random.Random(seed)
    t = rng.choice(TEMPLATES)
    price_min = rng.randint(*t["price"])
    price_max = price_min + rng.choice([20, 30, 40])
    return dict(
        task_id=f"IND_{rng.randint(10000, 99999)}",
        category=t["category"],
        price_min=price_min,
        price_max=price_max,
        min_rating=round(rng.uniform(*t["min_rating"]), 1),
        min_reviews=rng.randint(*t["min_reviews"]),
        difficulty=t["difficulty"],
    )


def build_battery(participant_seed):
    """
    Return an ordered list of task dicts for one participant.

    - Include all 3 anchor tasks
    - Sample 7 individualized tasks with balanced difficulty
    - Randomize the presentation order

    Anchor parameters never change across participants — that is the
    point of anchors.
    """
    rng = random.Random(participant_seed)
    individualized = [sample_individualized_task(seed=participant_seed * 100 + i)
                      for i in range(N_INDIVIDUALIZED_PER_BATTERY)]
    battery = list(ANCHORS) + individualized
    rng.shuffle(battery)
    return battery


def get_practice_task():
    """A fixed, easy task used only for the (unscored) practice round."""
    return dict(
        task_id="PRACTICE",
        category="electric kettle",
        price_min=20, price_max=45,
        min_rating=4.0, min_reviews=100,
        difficulty="easy",
    )
