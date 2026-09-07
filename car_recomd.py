#Car Recommendation System

"""
Car Recommendation CLI

This project is a Command-Line Interface (CLI) application that allows users 
to search for cars or get recommendations based on specifications and popularity.

Key Features:
1. Menu-driven interface:
    - Search by car make and model.
    - Get car suggestions with optional filters (budget, fuel type, etc.).
    - Exit the application.

2. API Integration:
    - Fetches car details from CarAPI.app (primarily US and major global brands).
    - Fetches additional non-US cars from free APIs like Back4App or API Ninjas.
    - Handles JSON responses and merges data from multiple sources.

3. Car Details Display:
    - Shows specifications including year, engine, transmission, fuel type, and price.
    - Displays results in a readable table format using rich library.

4. Recommendation Logic:
    - Calculates a popularity score for cars based on criteria like horsepower, price, and fuel efficiency.
    - Sorts cars by popularity to suggest the best options to the user.

5. Extensibility:
    - Can be expanded to include more APIs or additional car features.
    - Filters and recommendation algorithm can be refined for better user experience.

Purpose:
- To provide an interactive way for users to explore and compare cars.
- To showcase API integration, data handling, and CLI design skills.
- Suitable as a resume-worthy project for intermediate Python programmers.
"""

#Libraries we will be using in our project

"""
  - os: to work with files and folders 
       - os.listdir(folder) → gets all files in your data/ folder.
       - os.path.join(folder, file) → safely builds the full file path.
    - Without os, you have to hardcode file paths — messy.

  - re (regular expressions): To extract numeric values from strings (like "2.0L" → 2.0).
       - _num_re = re.compile(r"[-+]?\d*\.?\d+") → pattern for numbers.
       - _num_re.search("2.0L").group() → "2.0"
    - This is how we clean dirty columns (engineSize, mpg, etc.)

  - json: To save your final dictionary into a .json file so its portable.
       - json.dump(cars, f, indent=2) → saves your nested dictionary as a JSON file
    - JSON is universal: you can use it in Python, Node, Java, etc.

  - pandas (pd): To load and clean CSV data easily
       - pd.read_csv(path) → reads each CSV file
       - df.rename(columns=rename) → standardizes column names
       - df.apply(to_float) → applies cleaning functions column by column
    - Pandas makes it super simple to handle missing data, renaming, parsing, and cleaning

"""

"""
key points learned from this project:

 - os.path.splitext(file_name) -> This function splits a filename into two parts: (name, extension). this enabled me to take the name omitting the extension as the key
 - os.listdir(csv_folder) -> This function from the os module gives you a list of all files and folders inside the path you give it, i used this to iterate through the entire CSV
 - .endswith(".csv") -> checks whether in the folder there is any other files which aren't CSV
 - os.path.join(csv_folder, file_name) -> joins folder path and file name into a complete path, which means when you have the directory of the folder, your adding the file location to it inorder to access it
 - iterrows() -> lets you loop over each row of the DataFrame. For each row, it returns a tuple like (index, row) 
   - so in our code, we did like for _, row in df.iterrows():
       -  the reason for _ and row is that we dont care about index however we do need the row value 
 - enumerate(iterable, start=1) -> it loops two values each time (an index and actual value)

"""

import os
import pandas as pd

# Folder containing your CSV files
csv_folder = r"d:\Dhanush\Py_Project\Projects\practice\Cars_Dataset"

# Dictionary to store all cars
cars = {}

data_box = []


print("\033[1;34m")  # Set text to bold blue
print("=======================================")
print("         VIRTUAL CAR SHOWROOM         ")
print("=======================================")
print("\033[0m") 
 
print("\033[1;34m") 
print("Hi Sir/Ma'am, Welcome to our Virtual Car Showroom")
print('Loading Data...')
print("\033[0m")

def max_dataset(car_manu):
    hp_values = []
    mpg_values = []

    if car_manu not in cars:
        return {"max_hp": 0.0, "max_mpg": 0.0}

    for models in cars[car_manu].values():
        for years in models.values():
            for d in years:
                hp = HP(d["engineSize"])
                mpg = float(d["mpg"])

                hp_values.append(hp)
                mpg_values.append(mpg)

    if hp_values != []:
        max_hp = max(hp_values)
    else:
        max_hp = 0.0

    if mpg_values != []:
        max_mpg = max(mpg_values)
    else:
        max_mpg = 0.0
    
    return {"max_hp": max_hp, "max_mpg": max_mpg}

def HP(engine_size, turbo=False):
    # Estimated HP ≈ Engine Size (L) × 75
    base_hp = float(engine_size) * 75

    if turbo:
        base_hp *= 1.3

    return round(base_hp)

def score_rate_display():
    global data_box
    # Formula used to calculate the power, value, economany and balanced score
    """
    - Power Score (HP estimate from engine size) = (Horse-Power/Max HP in dataset) * 10
    - Economy Score (Fuel Efficency) = (MPG/Max MPG in data-set) * 10
    - Value Score (Affordability for Performance) = (Horse-Power/Price) * K, K is the scaling factor 1-10
    - Balanced Score (Overall performance/Efficiency/Value) = 0.4 * Power + 0.3 * Economy + 0.3 * Value

      k is not fixed — it depends on the dataset and level of detail available
    """
    scored_cars = []

    # Get information about each selected car
    for car in data_box:

        manufacturer = car["manufacturer"]
        model = car["model"]
        year = car["year"]

        variants = cars[manufacturer][model][year]

        prices = [float(v["price"]) for v in variants]
        mpgs = [float(v["mpg"]) for v in variants]
        engine_sizes = [float(v["engineSize"]) for v in variants]

        # Average variant values
        price = sum(prices) / len(prices)
        mpg = sum(mpgs) / len(mpgs)
        engine_size = sum(engine_sizes) / len(engine_sizes)

        horsepower = HP(engine_size)

        scored_cars.append({
            "manufacturer": manufacturer,
            "model": model,
            "year": year,
            "price": price,
            "mpg": mpg,
            "engine_size": engine_size,
            "hp": horsepower
        })

    # Find maximum values
    max_hp = max(car["hp"] for car in scored_cars)

    max_mpg = max(car["mpg"] for car in scored_cars)

    max_value = max(car["hp"] / car["price"] for car in scored_cars)

    # Calculate scores
    for car in scored_cars:

        power_score = (car["hp"] / max_hp) * 10
        economy_score = (car["mpg"] / max_mpg) * 10
        value_score = ((car["hp"] / car["price"])/ max_value) * 10

        balanced_score = (0.4 * power_score + 0.3 * economy_score + 0.3 * value_score)

        car["power_score"] = power_score
        car["economy_score"] = economy_score
        car["value_score"] = value_score
        car["balanced_score"] = balanced_score

    # Sort by score
    scored_cars.sort(key=lambda car: car["balanced_score"], reverse=True)

    # Display the comparison table

    print("\n")
    print("\033[1;34mCAR COMPARISON\033[0m")
    print("-" * 80)

    # Header
    print(f"{'Specification':<20}", end="")

    for car in scored_cars:
        name = f"{car['manufacturer']} {car['model']}"

        print(f"{name[:18]:<20}", end="")

    print()

    print("-" * 80)

    # Function to print each row
    def print_row(label, key, decimal=False):

        print(f"{label:<20}", end="")

        for car in scored_cars:

            value = car[key]

            if decimal:
                value = f"{value:.2f}"

            print(f"{str(value)[:18]:<20}", end="")

        print()

    # Car information
    print_row("Year", "year")
    print_row("Price (£)", "price", True)
    print_row("MPG", "mpg", True)
    print_row("Engine (L)", "engine_size", True)
    print_row("Horsepower", "hp")
    
    print("-" * 80)

    # Scores
    print_row("Power Score", "power_score", True)
    print_row("Economy Score", "economy_score", True)
    print_row("Value Score", "value_score", True)
    print_row("Overall Score", "balanced_score", True)

    print("-" * 80)

    # Recommendation
    best_car = scored_cars[0]

    print("\n\033[1;32mRECOMMENDATION\033[0m")

    print(
        f"{best_car['manufacturer']} "
        f"{best_car['model']} "
        f"({best_car['year']})"
    )

    print(
        f"Overall Score: "
        f"{best_car['balanced_score']:.2f}/10"
    )

    print("-" * 80)

def best_one_out():

    print("\n\033[1;34mBEST CAR BY BRAND\033[0m")
    print("-" * 55)
    print("Available manufacturers:")
    print("\033[1;32m" + ", ".join(cars.keys()) + "\033[0m")

    while True:
        manufacturer = input("\nEnter manufacturer: ").strip().title()
        if manufacturer in cars:
            break
        print(f"\033[1;31m'{manufacturer}' not found!\033[0m")

    all_cars = []

    for model, years in cars[manufacturer].items():
        for year, variants in years.items():
            price = sum(float(v["price"]) for v in variants) / len(variants)
            mpg = sum(float(v["mpg"]) for v in variants) / len(variants)
            engine = sum(float(v["engineSize"]) for v in variants) / len(variants)

            all_cars.append({
                "model": model, "year": year,
                "price": price, "mpg": mpg,
                "engine": engine, "hp": HP(engine)
            })

    if not all_cars:
        print("\033[1;31mNo cars found!\033[0m")
        return

    prices = [c["price"] for c in all_cars]
    minimum, maximum = min(prices), max(prices)
    budget_limit = minimum + (maximum - minimum) * 0.33
    mid_limit = minimum + (maximum - minimum) * 0.66

    budget = [c for c in all_cars if c["price"] <= budget_limit]
    mid = [c for c in all_cars if budget_limit < c["price"] <= mid_limit]
    top = [c for c in all_cars if c["price"] > mid_limit]

    max_hp = max(c["hp"] for c in all_cars)
    max_mpg = max(c["mpg"] for c in all_cars)
    max_value = max(c["hp"] / c["price"] for c in all_cars)

    for car in all_cars:
        power = car["hp"] / max_hp * 10
        economy = car["mpg"] / max_mpg * 10
        value = (car["hp"] / car["price"]) / max_value * 10
        car["score"] = 0.4 * power + 0.3 * economy + 0.3 * value

    best = [
        max(group, key=lambda c: c["score"]) if group else None
        for group in (budget, mid, top)
    ]

    print("\n\033[1;34m" + "=" * 70 + "\033[0m")
    print(f"\033[1;34m              BEST {manufacturer.upper()} CARS\033[0m")
    print("\033[1;34m" + "=" * 70 + "\033[0m")

    categories = [
        ("BUDGET", best[0], "\033[1;32m"),
        ("MID-RANGE", best[1], "\033[1;33m"),
        ("TOP", best[2], "\033[1;35m")
    ]

    for title, car, color in categories:
        print(f"\n{color}{title}\033[0m")
        if car:
            print(
                f"  \033[1;36m{manufacturer} {car['model']} ({car['year']})\033[0m"
                f" | £{car['price']:.0f}"
                f" | {car['mpg']:.1f} MPG"
                f" | {car['hp']} HP"
                f" | \033[1;32m{car['score']:.2f}/10\033[0m"
            )
        else:
            print("  No car available.")

    print("\n\033[1;34m" + "=" * 70 + "\033[0m")

def comparison_mech():
    global data_box

    if not data_box:
        print("\033[1;31m\nNo cars have been added to comparison yet.\033[0m")
        print("\033[1;33mPlease use the Search option to add cars first.\033[0m\n")
        return

    while True:
        print("\n\033[1;34m" + "=" * 55 + "\033[0m")
        print("\033[1;34m              CAR COMPARISON\033[0m")
        print("\033[1;34m" + "=" * 55 + "\033[0m")

        for i, car in enumerate(data_box, 1):
            print(
                f"\033[1;36m{i}.\033[0m "
                f"\033[1;32m{car['manufacturer']}\033[0m "
                f"{car['model']} "
                f"\033[1;33m({car['year']})\033[0m"
            )

        print("\033[1;34m" + "-" * 55 + "\033[0m")
        print("\033[1;32m1.\033[0m Compare Cars")
        print("\033[1;33m2.\033[0m Remove a Car")
        print("\033[1;35m3.\033[0m Clear Comparison")
        print("\033[1;31m4.\033[0m Back")

        choice = input("\n\033[1;36mChoose an option: \033[0m").strip()

        if choice == "1":
            if len(data_box) < 2:
                print(
                    "\033[1;31m"
                    "You need at least 2 cars to compare."
                    "\033[0m"
                )
            else:
                score_rate_display()

        elif choice == "2":
            try:
                index = int(
                    input(
                        "\033[1;36mEnter the car number to remove: \033[0m"
                    )
                )

                if 1 <= index <= len(data_box):
                    removed = data_box.pop(index - 1)
                    print(
                        f"\033[1;32m"
                        f"{removed['manufacturer']} {removed['model']} "
                        f"removed from comparison."
                        f"\033[0m"
                    )
                else:
                    print("\033[1;31mInvalid car number.\033[0m")

            except ValueError:
                print("\033[1;31mPlease enter a valid number.\033[0m")

        elif choice == "3":
            data_box.clear()
            print("\033[1;32mComparison list cleared.\033[0m")
            return

        elif choice == "4":
            return

        else:
            print("\033[1;31mInvalid option. Please try again.\033[0m")

def search_mech():
    global data_box
    while True:  # <-- main loop for multiple searches
        question = input("Do you know the car you are looking for? (y/n): ").strip().lower()
        if question != 'y':
            print("\033[1;32m" +"No problem! You can browse our showroom later."+ "\033[0m")
            print("\033[1;32m" + "If you remember something, feel free to comeback else Press 4"+ "\033[0m\n")
            return  # exit function if they don’t know

        # Show all manufacturers
        print("\nAvailable manufacturers:")
        print("\033[1;32m" + ", ".join(cars.keys()) + "\033[0m\n")

        # Manufacturer selection
        while True:
            user_manu = input("Enter the manufacturer: ").strip().title()
            if user_manu in cars:
                break
            print(f"\033[1;31mManufacturer '{user_manu}' not found! Please try again.\033[0m")

        # Show models
        print(f"\nModels available for {user_manu}:")
        print("\033[1;32m" + ", ".join(cars[user_manu].keys()) + "\033[0m\n")

        # Model selection
        while True:
            user_model = input("Enter the model: ").strip().title()
            if user_model in cars[user_manu]:
                break
            print(f"\033[1;31mModel '{user_model}' not found under {user_manu}! Please try again.\033[0m")

        # Show available years
        years = sorted(cars[user_manu][user_model].keys())
        print(f"\nAvailable years for {user_model}:")
        print("\033[1;32m" + ", ".join(str(y) for y in years) + "\033[0m\n")

        # Year selection
        while True:
            user_year = int(input("Enter the year: ").strip())
            if user_year not in cars[user_manu][user_model]:
                print(f"Year {user_year} not found for {user_model}!")
            else:
                break

        # Count the number of variants for that year
        variants_list = cars[user_manu][user_model][user_year]
        num_variants = len(variants_list)

        if num_variants == 1:
            detail = variants_list[0]
            print("\n" + "="*50)
            print(f"{user_manu} {user_model} ({user_year}) Details")
            print("-"*50)
            print(f"Transmission : {detail['transmission']}")
            print(f"Fuel Type    : {detail['fuelType']}")
            print(f"MPG          : {detail['mpg']}")
            print(f"Engine Size  : {detail['engineSize']} L")
            print(f"Price        : {detail['price']} £")
            print(f"Horse Power  : {HP(detail['engineSize'])} HP")
            print("="*50 + "\n")
        else:
            print("\n" + "="*50)
            print(f" {user_manu} {user_model} ({user_year}) Summary ({num_variants} variants)")
            print("-"*50)
            
            detail = variants_list[0]
            print(f"Transmission : {detail['transmission']}")
            print(f"Fuel Type    : {detail['fuelType']}")

            mpgs = [float(v['mpg']) for v in variants_list]
            print(f"MPG          : {min(mpgs)} - {max(mpgs)}")

            prices = [float(v['price']) for v in variants_list]
            print(f"Average Price : {sum(prices)/len(prices):.2f} £")
            print(f"Engine Size  : {detail['engineSize']} L")
            print(f"Horse Power  : {HP(detail['engineSize'])} HP")
            print("="*50 + "\n")

        # ---------------- Add to Comparison ----------------
        add_choice = input(f"Do you want to add {user_manu} {user_model} {user_year} to comparison? (y/n): ").strip().lower()
        if add_choice == "y":
            already_exists = any(car["manufacturer"] == user_manu and car["model"] == user_model and car["year"] == user_year for car in data_box)

            if already_exists:
                print(f"\033[1;31m{user_manu} {user_model} {user_year} is already in your comparison list!\033[0m")
            else:
                if len(data_box) < 3:
                    car_entry = {
                        "manufacturer": user_manu,
                        "model": user_model,
                        "year": user_year
                    }
                    data_box.append(car_entry)
                    print()
                    print(f"\033[1;33m{user_manu} {user_model} {user_year} added to comparison!\033[0m")
                    print("\n\033[1;33m","Current comparison list:", data_box, "\033[0m")
                    print(len(data_box))
        
                    # ---------------- Continue or Stop ----------------
                    print()
                    cont = input("Do you want to search another car? (y/n): ").strip().lower()
                    if cont != "y":
                        print()
                        break
                else:
                    while True:
                        print("Sorry, The Comparison Database is full!")
                        try:
                            data_removal = int(input("Do you want to remove a particular data or clear all or no? (1 or 2 or 3): "))
                        except ValueError:
                            print("Please enter a valid number (1, 2, or 3)!")
                            continue

                        if data_removal == 1:
                            print("\n\033[1;33mCurrent comparison list:\033[0m")
                            for i, car in enumerate(data_box, start=1):
                                print(f"  {i}. {car['manufacturer']} {car['model']} {car['year']}")

                            while True:
                                try:
                                    user_remove = int(input("Which one do you want to remove (enter index): ").strip())
                                except ValueError:
                                    print("Invalid input! Please enter a number.")
                                    continue

                                if 1 <= user_remove <= len(data_box):
                                    removed_car = data_box.pop(user_remove - 1)
                                    print(f"{removed_car['manufacturer']} {removed_car['model']} {removed_car['year']} removed from comparison!")
                                    break
                                else:
                                    print("Invalid number! Please enter a number from the list.")

                        elif data_removal == 2:
                            data_box.clear()
                            print('Comparison Database is Empty!')
                            break

                        elif data_removal == 3:
                            break

                        else:
                            continue
        else:
            return



def menu_sys():
    print("\033[1;33m+----------------------------+")
    print("|        Menu System         |")
    print("+----------------------------+")
    print("| 1. Search                  |")
    print("| 2. Car Comparison          |")
    print("| 3. Best Car in Manufacturer|")
    print("| 4. Exit                    |")
    print("+----------------------------+\033[0m")

    
    try:
        pressed_button = int(input("Please choose: "))
    except ValueError:
        print("\033[1;31mPlease enter a number from 1-4.\033[0m")
        return
    
    if pressed_button == 1:
        search_mech()
    
    elif pressed_button == 2:
        comparison_mech()
    
    elif pressed_button == 3:
        best_one_out()
    
    elif pressed_button == 4:
        print("\033[1;33m"+ 'Thank you for your time!'+ "\033[0m")
        return True

# Loop over all CSV files in the folder
for file_name in os.listdir(csv_folder):
    if not file_name.endswith(".csv"):
        continue

    manufacturer = os.path.splitext(file_name)[0].strip().title()

    # Read CSV and select relevant columns
    df = pd.read_csv(os.path.join(csv_folder, file_name))
    df = df[["model", "year", "price", "transmission", "fuelType", "mpg", "engineSize"]]

    for _, row in df.iterrows():
        year = int(row["year"])
        model = row["model"].strip().title()  # Clean model name

        details = {
            "price": row["price"],
            "transmission": row["transmission"],
            "fuelType": row["fuelType"],
            "mpg": row["mpg"],
            "engineSize": row["engineSize"]
        }

        # Build dictionary: Manufacturer -> Model -> Year -> List of Details
        cars.setdefault(manufacturer, {})
        cars[manufacturer].setdefault(model, {})
        cars[manufacturer][model].setdefault(year, [])
        cars[manufacturer][model][year].append(details)

print(f"\n\033[1;31mTotal manufacturers loaded: {len(cars)}\033[0m\n")


while True:
    a = menu_sys()
    if a == True:
        break
    else:
        continue