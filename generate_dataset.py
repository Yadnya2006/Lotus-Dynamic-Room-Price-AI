import random
import pandas as pd

random.seed(42)

ROOMS = {
    "AC Cottage": {
        "capacity": 2,
        "prices": {
            "Weekday": (3500, 4000),
            "Weekend": (4500, 5000),
            "Festival": (5000, 6000),
            "Summer": (4200, 4700),
            "Monsoon": (3200, 3800),
            "New Year": (6500, 7500)
        }
    },

    "AC Suite Room With Jacuzzi": {
        "capacity": 6,
        "prices": {
            "Weekday": (6000, 7000),
            "Weekend": (8000, 9000),
            "Festival": (10000, 12000),
            "Summer": (8500, 9500),
            "Monsoon": (5500, 6500),
            "New Year": (13000, 15000)
        }
    },

    "AC Executive Suite Room": {
        "capacity": 8,
        "prices": {
            "Weekday": (7500, 8000),
            "Weekend": (11000, 12000),
            "Festival": (13000, 14000),
            "Summer": (12000, 13000),
            "Monsoon": (7000, 8000),
            "New Year": (15000, 17000)
        }
    },

    "AC Deluxe Cottage": {
        "capacity": 2,
        "prices": {
            "Weekday": (4000, 4500),
            "Weekend": (4500, 5000),
            "Festival": (7000, 7500),
            "Summer": (5000, 5500),
            "Monsoon": (3800, 4300),
            "New Year": (8500, 9500)
        }
    },

    "AC Executive Rooms": {
        "capacity": 2,
        "prices": {
            "Weekday": (4000, 4500),
            "Weekend": (4500, 5000),
            "Festival": (7000, 7500),
            "Summer": (5000, 5500),
            "Monsoon": (3800, 4300),
            "New Year": (8500, 9500)
        }
    }
}

DAY_TYPES = ["Weekday", "Weekend"]
SEASONS = ["Normal", "Summer", "Monsoon", "Festival", "New Year"]

rows = []

for _ in range(1000):

    room = random.choice(list(ROOMS.keys()))

    day = random.choice(DAY_TYPES)

    season = random.choice(SEASONS)

    capacity = ROOMS[room]["capacity"]

    guests = random.randint(1, capacity)

    extra_guests = random.randint(0, 3)

    if season == "Normal":
        low, high = ROOMS[room]["prices"][day]
    else:
        low, high = ROOMS[room]["prices"][season]

    base_price = random.randint(low, high)

    rows.append([
        room,
        day,
        season,
        guests,
        extra_guests,
        base_price
    ])

df = pd.DataFrame(
    rows,
    columns=[
        "Room_Type",
        "Day_Type",
        "Season",
        "Guests",
        "Extra_Guests",
        "Base_Price"
    ]
)

df.to_csv("dataset.csv", index=False)

print(df.head())

print()

print("Dataset Generated Successfully")
print("Rows :", len(df))