from data_validation import input_form, qform_varchar, qform_num
from search import search_recipe, search_meal, q_get_tuple, q_get_list_of_tuples
from recipe import print_recipe

#MEAL [recipe_id, plan_id, num_servings]

def recipe_id_meal(meal):
    return meal[0]
def plan_id_meal(meal):
    return meal[1]
def num_servings_meal(meal):
    return meal[2]


#add meal if doesn't exists, if not, give option to update
#add_meal(cursor, plan_id, recipe_id/None)-> None
def add_meal(cursor, plan_id, recipe_id):
    if recipe_id is None:
        recipe = search_recipe(cursor, None)
        print_recipe(recipe)
        recipe_id = recipe[0]
    if (search_meal(cursor, plan_id, recipe_id) is None):
        amount = input("How many servings of this item would you like to add?")
        if(input_form(amount)==1):
            query = ("insert into meal (recipe_id, plan_id, num_servings) values ("
                     + qform_num(recipe_id) + ","
                     + qform_num(plan_id) + ","
                     + qform_num(amount) + ")")
            cursor.execute(query)
        else:
            print("Please enter a numeric input:")
            add_meal(cursor, plan_id, recipe_id)
    else:
        print("This recipe is already a part of this plan")

#remove meal if exists, if not do nothing
#remove_meal(cursor, plan_id, recipe_id/None)-> None
def remove_meal(cursor, plan_id, recipe_id):
    if recipe_id is None:
        recipe_item = search_recipe(cursor, None)
        recipe_id = recipe_item[0]
    if not (search_meal(cursor, plan_id, recipe_id) is None):
        query = ("delete from meal where recipe_id =" + qform_num(recipe_id) + " and plan_id = " + qform_num(plan_id))
        cursor.execute(query)

#alter meal if exists, if not give option to add
#alter_meal(cursor, plan_id, recipe_id/None)-> None
def alter_meal(cursor, plan_id):
    recipe = search_recipe(cursor, None)
    recipe_id = recipe[0]
    if (search_meal(cursor, plan_id, recipe_id) is None):
        ans = input("Would you like to add this recipe to the plan? [Y/N]")
        if (ans == "Y"):
            add_meal(cursor, plan_id, recipe_id)
    else:
        new_amt = input('What would you like to change the number of servings to?')
        query = "update meal set num_servings =  " + qform_num(new_amt) + "where recipe_id = " + qform_num(recipe_id) + "and plan_id = " + qform_num(plan_id)
        cursor.execute(query)