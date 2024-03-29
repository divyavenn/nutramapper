
from data_validation import *
from search import *
from meal import add_meal
from nutrient import get_nutrients_to_track
from recipe import nutritional_total_recipe
import decimal

#PLAN = [plan_id, plan_name, num_days]
def plan_id_plan(plan):
    return plan[0]
def plan_name_plan(plan):
    return plan[1]
def num_days_plan(plan):
    return plan[2]

#adds a new plan
#cursor -> None
def add_plan(cursor):
    name = input_name("What is the name of this plan?")
    days = input_number_not_zero("How many days does this meal plan cover?")
    plan_id = 0
    plan_id = cp_get_value(cursor, 'insert_plan', (name, days, plan_id), 0)
    while (input_yes("Would you like to add a recipe?")):
        add_meal(cursor, plan_id, None)

#adds a new plan
#cursor -> None
def remove_plan(cursor, plan_id):
    cursor.callproc('remove_plan', (plan_id,))

#adds a new plan
#cursor -> None
def change_plan_days(cursor, plan_id):
    days = input_number_not_zero("What number of days should this plan cover?")
    query = "update plan set num_days = " + qform_num(days) + "where plan_id = " + qform_num(plan_id)
    cursor.execute(query)

#adds a new plan
#cursor -> None
def rename_plan(cursor, plan_id):
    new_name = input_name("Enter a new name for the plan")
    print(qform_num(plan_id))
    query = "update plan set plan_name = " + qform_varchar(new_name) + "where plan_id = " + qform_num(plan_id)
    cursor.execute(query)

def fulfills_nutritional_requs(cursor, plan_id):
    from meal import recipe_id_meal
    # cursor, recipe_id/None, plan_id/None -> [recipe_id, plan_id, num_servings]/None
    meals = search_meal(cursor, None, plan_id)
    plan = search_plan(cursor, plan_id)
    if (meals is not None and plan is not None):
        daily_reqs = []
        #cursor -> [nutrient_id, nutrient name, daily requirement, units]
        nutrients = get_nutrients_to_track(cursor)
        if (nutrients is not None):
            for n in nutrients:
                daily_reqs.append(n[2])
            #for each recipe, holds info for each nutrient total
            recipe_totals = []
            num_days = num_days_plan(plan)
            num_nutr_reqr = len(daily_reqs)
            planwide_avg = [0 for i in range(num_nutr_reqr)]
            for m in meals:
                recipe_id = recipe_id_meal(m)
                num_servings = m[2]
                # nutritional_total_recipe(cursor, recipe_id) -> [nutrient_id, name, total_in_recipe, units]
                totals = nutritional_total_recipe(cursor, recipe_id)
                for t in totals:
                    t[2] = t[2]*decimal.Decimal(num_servings)
                recipe_totals.append(totals)
            for i in range(0,num_nutr_reqr):
                sum = 0
                for r in recipe_totals:
                    sum = sum + r[i][2]
                planwide_avg[i] = decimal.Decimal(sum)/decimal.Decimal(num_days)
                if planwide_avg[i] < daily_reqs[i]:
                    diff = round(daily_reqs[i] - planwide_avg[i],1)
                    print("You miss your goal for " + str(nutrients[i][1]) + " by an average of: " + str(diff) + " " + str(nutrients[i][3]) + " per day.")
                elif planwide_avg[i] > daily_reqs[i]:
                    surplus = round(planwide_avg[i] - daily_reqs[i],1)
                    print("You exceed your goal for " + str(nutrients[i][1]) + " by an average of: " + str(surplus) + " " + str(nutrients[i][3]) + " per day.")
        else:
            print("There are no nutrient requirements set yet.")