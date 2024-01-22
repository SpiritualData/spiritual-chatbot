def find_missing_categories():
    # Read categories from all_categories.txt
    with open("all_categories.txt", "r") as f:
        all_categories = set(line.strip() for line in f.readlines())

    # Read categories from category_definitions.txt and only take the part before the colon
    with open("category_definitions.txt", "r") as f:
        defined_categories = set(line.strip().split(":")[0].strip() for line in f.readlines())

    # Find and print missing categories
    missing_categories = all_categories - defined_categories
    print("Missing categories:")
    for category in missing_categories:
        print(category)

from fire import Fire
Fire(find_missing_categories)