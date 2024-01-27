import json

f = open("recipes_exmple.txt", "r")
x = f.read()

# parse x:
y = json.loads(x)


# find a recipe
search_string = "RECIPE LIST"


def find_recipe(recipes, find_parameter, str_=""):
    if find_parameter == "find_recipe_from_name":
        for rec in recipes:
            if rec["recipe"] == str_:
                return rec
    elif find_parameter == "all_recipe_names":
        lst = []
        for rec in recipes:
            lst.append(rec["recipe"])
        return lst

    return None


print(find_recipe(y["RECIPE LIST"], "find_recipe_from_name", "khichdi"))

print(find_recipe(y["RECIPE LIST"], "all_recipe_names"))

