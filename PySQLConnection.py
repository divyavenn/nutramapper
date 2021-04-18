
import pymysql


# --------------------------------------------------CURSOR FUNCTIONS
def get_only_result(cursor, query):
    cursor.execute(query)
    x = None
    for i in cursor:
        return i;


# --------------------------------------------------SEARCH BY NAME FUNCTIONS-------------------------------------------------
def search(cursor, dialogue, allCols, table, onCol):
    x = input(dialogue + "\n")
    query = "select " + allCols + " from " + table + " where " + onCol + " like '" + x + "%'"
    while not (cursor.execute(query) == 1):
        print("Not an exact match. Did you mean one of these?")
        for i in cursor:
            print(i)
        x = input(dialogue + "\n")
        query = "select " + allCols + " from " + table + " where " + onCol + " like '" + x + "%'"
    for i in cursor:
        return i


# Searches for ingredient by name or by specific nid, returns nutritional info
def search_nutrient(cursor, nid):
    x = []
    if (nid == None):
        x = search(cursor, "Enter a nutrient", "nutrient_id, nutrient_name, units", "nutrient", "nutrient_name")
    else:
        cursor.execute("select nutrient_id, nutrient_name, units from nutrient where nutrient_id = " + nid)
        for i in cursor:
            x = i
    return x;


# Searches for ingredient by name or through specific (inp)food-id
# returns [food_id, food_name, cost_per_100]
def search_food_item(cursor, food_id):
    x = []
    if (food_id is None):
        x = search(cursor, "Enter a food item", "food_id, food_name, cost_per_100g", "food_item", "food_name")
    else:
        cursor.execute("select food_id, food_name, cost_per_100g from food_item where food_id = " + food_id)
        for i in cursor:
            x = i
    return x;


# Searches for recipe by name or through specific recipe-id
def search_recipe(cursor, recipe_id):
    x = []
    output_fields = "recipe_id, recipe_name"
    table = "recipe"
    if (recipe_id is None):
        x = search(cursor, "Enter a recipe", output_fields, table, "recipe_name")
    else:
        cursor.execute("select " + output_fields + " from " + table + " where recipe_id = " + str(recipe_id))
        for i in cursor:
            x = i
    return x


# Searches for recipe by name or through specific recipe-id
def search_plan(cursor, plan_id):
    x = []
    output_fields = "plan_id, plan_name"
    table = "plan"
    if (plan_id is None):
        x = search(cursor, "Enter a plan", output_fields, table, "plan_name")
    else:
        cursor.execute("select " + output_fields + " from " + table + " where plan_id = " + (plan_id))
        for i in cursor:
            x = i
    return x;


# -----------------------------------------------------NUTRIENT FUNCTIONS-----------------------------------------------

# gets amount of (inp)nutrient in (inp)food item
# returns integer: amount
def get_nutrient_amount(cursor, food_id, nutrient_id):
    cursor.execute \
        ("select nutrient_id, amt, food_id from nutrient_data where food_id = )" + str(food_id) + " and nutrient_id = " + str(nutrient_id))
    for i in cursor:
        x = i
    if (len(x) == 0):
        return 0
    else:
        return x[1]

def print_nutrient_info(nutrientList):
    for n in nutrientList:
        print(n)

def get_nutrients_to_track(cursor):
    nutr_to_track = []
    cursor.execute ('select n.nutrient_id, n.nutrient_name, d.requ, n.units from daily_nut_requ as d natural join nutrient as n')
    for i in cursor:
        nutr_to_track.append(i)
    return nutr_to_track

def is_part_of_nutrients_to_track(cursor, nutrient):
    nttList = get_nutrients_to_track(cursor)
    return (nutrient[0] in (i[0] for i in nttList))

def update_nutrients_to_track(cursor, nid):
    x = search_nutrient(cursor, nid)
    is_part = is_part_of_nutrients_to_track(cursor, x)
    # Nutrient is indeed part of list; can update
    if (is_part):
        r = input("How many " + x[2] + " would you like to consume daily, on average?")
        query = "update daily_nut_requ set requ = 13.5 where nutrient_id = '" + r + "'"
        cursor.execute(query)
    else:
        print("That nutrient is not part of the daily requirements.\n")
        print(x)
        choice = input("Would you like to add it? [Y/N] \n")
        if (choice == 'Y'):
            add_nutrients_to_track(cursor, x[0])
        # Nutrient is not part of list; must add


def add_nutrients_to_track(cursor, nid):
    x = search_nutrient(cursor, nid)
    is_part = is_part_of_nutrients_to_track(cursor, x)
    if (is_part):
        print("That nutrient is already part of the daily requirements.\n")
        print(x)
        choice = input("Would you like to update it? [Y/N] \n")
        if (choice == 'Y'):
            update_nutrients_to_track(cursor, x[0])
    else:
        r = input("How many " + x[2] + " would you like to consume daily, on average?")
        cursor.execute("insert into daily_nut_requ (nutrient_id, requ) values (" + str(x[0]) + "," + str(r) + ")")
def remove_nutrients_to_track(cursor):
    nutr_to_track = get_nutrients_to_track(cursor)
    print_nutrient_info(nutr_to_track)
    x = search_nutrient(cursor, None)
    is_part = is_part_of_nutrients_to_track(cursor, x)
    if (is_part):
        cursor.execute("delete from daily_nut_requ where nutrient_id = " + str(x[0]) + "")
    else:
        print("Nutrient is already not part of tracked requirements. \n")

#--------------------------------------------------------------INGREDIENT FUNCTIONS--------------------------------------------------
def part_of_recipe(cursor, food_id, recipe_id):
    
def add_ingredient(cursor, recipe_id):
    food_item = search_food_item(cursor, None)
    food_id = food_item[0]
    amount = input("How many grams(whole numbers only) of this item would you like to add?")
    query = ("insert into ingredient (food_id, recipe_id, amount_in_grams) values ("
             + str(food_id) + ","
             + str(recipe_id) + ","
             + str(amount) + ")")
    cursor.execute(query)

def remove_ingredient(cursor, recipe_id):
    food_item = search_food_item(cursor, None)
    food_id = food_item[0]
def alter_ingredient(cursor, recipe_id):
# ---------------------------------------------------------------RECIPE FUNCTIONS--------------------------------------------------------
def get_recipe_ingredients(cursor, recipe_id):
    ingredients = []
    cursor.execute("select food_id, amount_in_grams, recipe_id from ingredient where recipe_id = " + str(recipe_id))
    for i in cursor:
        ingredients.append(i)
    return ingredients

def nutritional_total_recipe(cursor, recipe_id):
    nutr_reqs = get_nutrients_to_track(cursor)
    food_items_in_recipe = get_recipe_ingredients(cursor, recipe_id)
    nutr_totals = []
    for nutrient in nutr_reqs:
        total = 0
        for food_info in food_items_in_recipe:
            amount = (get_nutrient_amount(cursor, food_info[0], nutrient[0]))
            total = total + amount
        # [nutrient id, nutrient name, total in recipe, units]
        nutr_totals.append([nutrient[0], nutrient[1], total, nutrient[3]])
    return nutr_totals

def add_recipe(cursor):
    name = input("What is the name of this recipe?")
    cursor.execute('insert into recipe (recipe_name) values ( "' + name + ' ")')
    recipe_id = None
    # find recipe_id of new recipe
    cursor.execute("select recipe_id from recipe where (recipe_name = '" + name + "')")
    for i in cursor:
        recipe_id = i[0]
    while (input("Would you like to add an ingredient [Y/N]") == "Y"):
        add_ingredient(cursor, recipe_id)

def view_recipe(cursor, recipe_id):
    recipe = search_recipe(cursor, recipe_id)
    recipe_id = recipe[0]
    ingredients = get_recipe_ingredients(cursor, recipe_id)
    name = recipe[1]
    print(name)
    for i in ingredients:
        food_item = search_food_item(cursor, i[0])
        food_name = food_item[1]
        amount_in_grams = i[1]
        print("\t " + food_name + ": \n \t \t" + str(amount_in_grams) + " grams")

def view_recipe_list(cursor):
    print("RECIPE INDEX")
    query = "select recipe_name from recipe"
    all_recipes = cursor.execute(query)
    for r in all_recipes:
        print(r)
def rename_recipe(cursor, recipe_id):
    new_name = input("Enter a new name for the recipe:")
    query = "update recipe set recipe_name = " + "'new_name'" + "where recipe_id = " + str(recipe_id)


# --------------------------------------------------------------MENU FUNCTIONS--------------------------------------------------------------------
def print_menu(options):
    print(30 * "-" + "MENU" + 30 * "-" + "")
    i = 1
    for opt in options:
        opt_stmt = str(i) + ":" + opt + ""
        print(opt_stmt)
        i = i + 1
    print(67 * "-" + "")
    print("**Type 0 to end program.")
def make_menu(opt):
    loop = True
    while loop:
        print_menu(opt)
        x = input("Enter your choice " + str(1) + " to " + str(len(opt)))
        for i in range(1, len(opt ) +1):
            if x == str(i):
                return i
        if x == str(0):
            loop = False  # This will make the while loop to end as not value of loop is set to False
        else:
            # Any integer inputs other than values 1-5 we print an error message
            print("Invalid option selection. \n")

def nutrient_menu(cursor):
    options = ['View Nutrient Requirements',
              'Add Nutrient Requirement to Track',
              'Update Nutrient Requirement',
              'Remove Nutrient Requirement Tracked',
              'Return to Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        nutr_to_track = get_nutrients_to_track(cursor)
        print("Nutrients that are currently being tracked: \n")
        print_nutrient_info(nutr_to_track)
        nutrient_menu(cursor)
    elif (choice == 2):
        add_nutrients_to_track(cursor, None)
        nutrient_menu(cursor)
    elif (choice == 3):
        update_nutrients_to_track(cursor, None)
        nutrient_menu(cursor)
    elif (choice == 4):
        remove_nutrients_to_track(cursor)
        nutrient_menu(cursor)
    elif (choice == 5):
        main_menu(cursor)

def food_item_menu(cursor):
    options = ['View Information For a Food Item',
              'Update Cost Of Food Item',
              'Return to Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        print("View food item information")
        food_item_menu(cursor)
    elif (choice == 2):
        print('Update cost of food item')
        food_item_menu(cursor)
    elif (choice == 3):
        main_menu(cursor)

def recipe_menu(cursor):
    options = ['View/Update Recipes',
              'Create New Recipe',
               'Return To Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        print("View/update recipe")
        view_recipe_list(cursor)
        recipe = search_recipe(cursor ,None)
        view_recipe(cursor, recipe[0])
        recipe_menu(cursor)
    elif (choice == 2):
        print('create new recipe')
        add_recipe(cursor)
        recipe_menu(cursor)
    elif (choice == 3):
        main_menu(cursor)
def plan_menu(cursor):
    options = ['View/Update Meal Plan',
              'Create New Meal Plan',
               'Return To Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        print("View/update meal plan")
        recipe_menu(cursor)
    elif (choice == 2):
        print('create new meal plan')
        recipe_menu(cursor)
    elif (choice == 3):
        main_menu(cursor)

def main_menu(cursor):
    options = ['View/Edit Tracked Nutrients',
               'View/Edit Ingredients',
               'View/Edit Recipes',
               'View/Edit Plans']
    choice = make_menu(options)
    if (choice == 1):
        nutrient_menu(cursor)
    elif (choice == 2):
        food_item_menu(cursor)
    elif (choice == 3):
        recipe_menu(cursor)
    elif (choice == 4):
        plan_menu(cursor)


# -----------------------------------------------------------------MAIN--------------------------------------------------------------------
print('Hi!')
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='0926',
                             db='meal_plan',
                             charset='utf8mb4')


cursor = connection.cursor()
main_menu(cursor)
connection.commit()
print("Closing connection to database...\n")
cursor.close()
connection.close()
print("Goodbye!\n")




