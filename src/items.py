import random
from prices import PRICES

supermarket_items = {
    "GeneralMerchandise": [
        "batteries", "light bulbs", "extension cord", "umbrella", "notebook", "pens", "pencils", "scissors", "adhesive tape",
        "super glue", "gift wrap", "birthday cards", "envelopes", "paper clips", "duct tape", "storage boxes", "plastic bags", 
        "ziplock bags", "travel mug", "water bottle", "reusable grocery bag", "flashlight", "candles", "matches", "lighters",
        "AA batteries", "AAA batteries", "laundry basket", "broom", "dustpan", "mop", "bucket", "sponge", "trash bags",
    ],
    "Food": [
        "apples", "bananas", "oranges", "lemons", "grapes", "strawberries", "blueberries", "watermelon", "pineapple", "mango",
        "lettuce", "spinach", "kale", "tomatoes", "onions", "garlic", "carrots", "potatoes", "broccoli", "cauliflower",
        "bell peppers", "cucumbers", "avocados", "ginger", "lemongrass", "rice", "pasta", "flour", "sugar", "salt", "pepper",
        "olive oil", "vegetable oil", "soy sauce", "vinegar", "baking powder", "baking soda", "yeast", "honey","peanut butter",
        "jam", "chocolate spread", "cereal", "instant noodles", "macaroni and cheese", "canned beans", "canned corn",
        "canned soup", "tomato sauce", "pasta sauce", "chicken broth", "beef broth", "tea bags", "coffee", "hot chocolate",
        "granola bars", "chips", "popcorn", "crackers", "cookies", "biscuits", "trail mix", "nuts", "pretzels",
        # --- Food: Refrigerated & Frozen ---
        "milk", "butter", "cheese", "yogurt", "cream", "eggs", "orange juice", "apple juice", "frozen pizza", "frozen fries",
        "ice cream", "frozen peas", "frozen corn", "frozen berries", "frozen chicken", "frozen fish", "frozen vegetables",
        "frozen waffles", "frozen dinners",
        # --- Food: Meat & Seafood ---
        "chicken breast", "chicken thighs", "ground beef", "steak", "bacon", "sausages", "pork chops", "salmon", "shrimp",
        "tilapia", "tuna", "deli ham", "roast beef slices", "turkey slices",
    ],
    "Home": [
        # --- Home & Cleaning ---
        "laundry detergent", "fabric softener", "dish soap", "sponges", "paper towels", "toilet paper", "napkins",
        "all-purpose cleaner", "glass cleaner", "bathroom cleaner", "bleach", "air freshener", "mop refills",
        "vacuum bags", "aluminum foil", "plastic wrap", "food storage containers",
    ],
    "Toiletries": [
        # --- Toiletries ---
        "toothpaste", "toothbrush", "mouthwash", "dental floss", "soap", "body wash", "shampoo", "conditioner", "razor",
        "shaving cream", "deodorant", "toilet wipes", "cotton swabs", "cotton balls", "tissues", "hand sanitizer", "feminine pads",
        "tampons", "baby wipes", "diapers",
    ],
    "Health": [
        "vitamins", "pain reliever", "cough syrup", "antacid tablets", "band-aids", "first aid cream", "sunscreen", "lip balm",
        "moisturizer", "face wash", "makeup remover", "foundation", "mascara", "eyeliner", "nail polish", "hairbrush", "hair ties",
        "body lotion", "perfume", "aftershave", "cotton rounds",
    ],
}

generated_items = {}
flags = {
    "GeneralMerchandise": "GMFlag",
    "Food": "FFlag",
    "Home": "HFlag",
    "Toiletries": "TFlag",
    "Health": "HBFlag",
}


def does_item_code_exist(code):
    for _, item_code in generated_items.items():
        if item_code == code:
            return True
    return False


def get_flag(department):
    return flags[department]


def get_random_item():
    itemDepartment = random.choice(list(supermarket_items.keys()))
    item = random.choice(supermarket_items[itemDepartment])
    item_code = 0
    if not item in generated_items:
        item_code = random.randint(1000, 5000)
        while does_item_code_exist(item_code):  ## prevents same code from existing
            item_code = random.randint(1000, 5000)

        generated_items[item] = item_code

    return {
        "item_name": item,
        "item_code": generated_items[item],
        "flag": get_flag(itemDepartment),
        "price": PRICES.get(item, 5.00),  # Default price if not found
    }
