from data_validation import qform_varchar, qform_num, input_number, input_yes
from search import search_food_item, search_ingredient

#INGREDIENT: [food_id, recipe_id, amount_in_grams]

#checks if ingredient exists;if not, adds it, if so gives option to update ingredient
#cursor, recipe id, food id -> None
def add_ingredient(cursor, recipe_id, food_id):
    if food_id is None:
        food_item = search_food_item(cursor, None)
        food_id = food_item[0]
    # search_ingredient(cursor, food_id/None, recipe_id/None) -> [food_id, recipe_id, amount_in_grams]
    if search_ingredient(cursor, food_id, recipe_id) is not None:
        print("This ingredient is already a part of the recipe.")
        input("\n \n Press any key to continue.")
    else:
        amount = input_number("How many grams of this item does the recipe need?")
        cursor.callproc('add_ingredient', (food_id, recipe_id, amount))

#checks if ingredient exists;if not, does nothing, if so deletes it
#cursor, recipe id, food id/None -> None
def remove_ingredient(cursor, recipe_id, food_id):
    if food_id is None:
        food_item = search_food_item(cursor, None)
        food_id = food_item[0]
    # search_ingredient(cursor, food_id/None, recipe_id/None) -> [food_id, recipe_id, amount_in_grams]
    if (search_ingredient(cursor, food_id, recipe_id) is not None):
        cursor.callproc('remove_ingredient', (food_id, recipe_id))

#checks if ingerent exists; if so, alters the amount, if not gives option to add
#cursor, recipe id, food id/None -> None
def alter_ingredient(cursor, recipe_id, food_id):
    if food_id is None:
        food_item = search_food_item(cursor, None)
        food_id = food_item[0]
    # search_ingredient(cursor, food_id/None, recipe_id/None) -> [food_id, recipe_id, amount_in_grams]
    if (search_ingredient(cursor, food_id, recipe_id, ) is not None):
        new_amt = input_number('What would you like to change the amount to (in grams)?')
        query = "update ingredient set amount_in_grams =  " + qform_num(new_amt) + "where food_id = " + qform_varchar(food_id) + "and recipe_id = " + qform_num(recipe_id)
        cursor.execute(query)
    else:
        if(input_yes("Would you like to add this ingredient?")):
            add_ingredient(cursor, recipe_id, food_id)

