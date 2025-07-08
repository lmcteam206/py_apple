def load_recipes(filename):
    recipes = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:
                continue
            left, result = line.split('=')
            ingredients = [x.strip() for x in left.split('+')]
            result = result.strip()
            recipes[frozenset(ingredients)] = result
    return recipes
