from multiprocessing import Pool
import pyautogui
import re
from selenium import webdriver
import sys
import time

ai_delay = 0.75
max_confidence = 0.95
min_confidence = 0.75
customer_delay = 2.5
ingredient_regex = re.compile(r'Assets/Ingredients/(.*).png')
max_level = 5
order_regex = re.compile(r'Assets/Pizzas/(.*)_pizza.png')
potential_orders = ['Assets/Pizzas/margherita_pizza.png', 'Assets/Pizzas/marinara_pizza.png', 'Assets/Pizzas/ham_artichoke_pizza.png',
                    'Assets/Pizzas/ham_mushroom_pizza.png', 'Assets/Pizzas/pepperoni_mushroom_pizza.png', 'Assets/Pizzas/pepperoni_pizza.png']

def click_button(button_name, required=False, check_interval=1):
    button = None
    looking_for_button = True
    temp_confidence = max_confidence

    while looking_for_button:
        button = pyautogui.locateCenterOnScreen(button_name, confidence=temp_confidence)

        if button is None and required:
            if temp_confidence <= min_confidence:
                print("My confidence can't get any lower...")
                temp_confidence = min_confidence
            else:
                print("Lowering confidence...")
                temp_confidence -= 0.05
            time.sleep(check_interval)
        elif button is None and not required:
            return False
        else:
            print("Restoring confidence...")
            temp_confidence = max_confidence
            looking_for_button = False

    pyautogui.moveTo(button.x, button.y)
    pyautogui.click(button.x, button.y)

def description():
    click_button('Assets/Buttons/description_button.png', required=True)

def find_order_on_screen(order_name):
    order = pyautogui.locateCenterOnScreen(order_name, confidence=max_confidence)
    purged_order_name = order_regex.findall(order_name)

    if order is not None:
        return purged_order_name[0]
    else:
        return None

def get_ingredient_location(ingredient):
    purged_ingredient_name = ingredient_regex.findall(ingredient)

    if purged_ingredient_name[0] is not None:
        print('Added coordinates for %s to dictionary...' % purged_ingredient_name[0])

    location = pyautogui.locateCenterOnScreen(ingredient, confidence=max_confidence)

    if location is not None:
        return location

def start():
    click_button('Assets/Buttons/start_button.png', required=True)


class PizzaPartyBot:
    browser = None
    currentLevel = 1
    ingredientLocations = {}
    isNextLevel = False
    pool = None

    # Startup & Destruction
    def open_browser_and_start_game(self):
        print('\nInitializing bot...\n')
        self.browser = webdriver.Firefox()
        self.browser.get('https://www.minigames.com/games/pizza-party')

        start()
        description()
        self.continue_to_first_level()

    def self_destruct(self):
        print('\nI have won, mortal...\n')
        time.sleep(ai_delay)
        print('\nSelf destruct in 5...')
        for i in range(4, 0, -1):
            time.sleep(ai_delay)
            print('\n%s...' % i)
        time.sleep(ai_delay * 2)
        print('\nGoodnight...\n')
        time.sleep(ai_delay * 2)
        self.browser.close()
        sys.exit(1)
  
    # Navigation
    def continue_to_first_level(self):
        self.isNextLevel = True
        click_button('Assets/Buttons/continue_button.png', required=True)

    def continue_to_next_level_or_self_destruct(self):
        self.currentLevel += 1
        self.isNextLevel = True

        if self.currentLevel <= max_level:
            looking = click_button('Assets/Buttons/next_level_button.png', required=True)
        else:
            self.self_destruct()

        print('\nStarting level %s...\n' % self.currentLevel)
        time.sleep(customer_delay)  # Wait for first customer of upcoming level (halved because no exit animation)

    # Order creation
    def get_new_order(self):
        print('Getting new order...')

        if self.pool is None:
            self.pool = Pool()

        results = self.pool.map(find_order_on_screen, potential_orders)

        for result in results:
            if result is not None:
                return result
            else:
                continue

        print('\nNo new order...\n')

    def prepare_new_order(self, order):
        print('Starting the %s pizza...' % order)
        ingredients = self.get_ingredients_for_order(order)

        for ingredient in ingredients:
            pyautogui.click(ingredient.x, ingredient.y)

        print('Finished the %s pizza...\n' % order)
        time.sleep(customer_delay)  # Wait for next customer

    # Ingredient management
    def get_ingredients_for_order(self, order):
        if self.isNextLevel:
            self.get_ingredient_locations()
            self.isNextLevel = False

        ingredients = []

        if order == 'margherita':
            ingredients.append(self.ingredientLocations['tomato'])
            ingredients.append(self.ingredientLocations['mozzarella'])
            ingredients.append(self.ingredientLocations['basil'])
        elif order == 'marinara':
            ingredients.append(self.ingredientLocations['tomato'])
            ingredients.append(self.ingredientLocations['oregano'])
        elif order == 'ham_artichoke':
            ingredients.append(self.ingredientLocations['tomato'])
            ingredients.append(self.ingredientLocations['mozzarella'])
            ingredients.append(self.ingredientLocations['ham'])
            ingredients.append(self.ingredientLocations['artichoke'])
        elif order == 'ham_mushroom':
            ingredients.append(self.ingredientLocations['mozzarella'])
            ingredients.append(self.ingredientLocations['ham'])
            ingredients.append(self.ingredientLocations['mushrooms'])
        elif order == 'pepperoni':
            ingredients.append(self.ingredientLocations['tomato'])
            ingredients.append(self.ingredientLocations['mozzarella'])
            ingredients.append(self.ingredientLocations['basil'])
            ingredients.append(self.ingredientLocations['pepperoni'])
        elif order == 'pepperoni_mushroom':
            ingredients.append(self.ingredientLocations['tomato'])
            ingredients.append(self.ingredientLocations['mozzarella'])
            ingredients.append(self.ingredientLocations['pepperoni'])
            ingredients.append(self.ingredientLocations['mushrooms'])

        ingredients.append(self.ingredientLocations['oven'])
        return ingredients

    def get_ingredient_locations(self):
        print('Updating ingredient location coordinates...')
        locations = self.ingredientLocations

        if self.currentLevel == 1:
            locations['oven'] = get_ingredient_location('Assets/Ingredients/oven_button.png')
            locations['tomato'] = get_ingredient_location('Assets/Ingredients/tomato.png')
            locations['mozzarella'] = get_ingredient_location('Assets/Ingredients/mozzarella.png')
            locations['basil'] = get_ingredient_location('Assets/Ingredients/basil.png')
            locations['oregano'] = get_ingredient_location('Assets/Ingredients/oregano.png')

        if self.currentLevel == 2:
            locations['ham'] = get_ingredient_location('Assets/Ingredients/ham.png')
            locations['artichoke'] = get_ingredient_location('Assets/Ingredients/artichoke.png')

        if self.currentLevel == 3:
            locations['mushrooms'] = get_ingredient_location('Assets/Ingredients/mushrooms.png')

        if self.currentLevel == 4:
            locations['pepperoni'] = get_ingredient_location('Assets/Ingredients/pepperoni.png')

        self.ingredientLocations = locations

def main():
    bot = PizzaPartyBot()
    bot.open_browser_and_start_game()

    time.sleep(customer_delay)  # Wait for first customer of first level

    while True:
        order = bot.get_new_order()

        if order is not None:
            bot.prepare_new_order(order)
        else:
            bot.continue_to_next_level_or_self_destruct()

if __name__ == '__main__':
    main()
