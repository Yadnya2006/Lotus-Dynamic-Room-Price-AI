# Graph Generator

import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


# Graph folder

GRAPH_FOLDER = os.path.join(
    "static",
    "graphs"
)

os.makedirs(
    GRAPH_FOLDER,
    exist_ok=True
)


# Generate graphs

def generate_graphs():

    try:

        df = pd.read_csv(
            "dataset.csv"
        )

        # Price Graph

        plt.figure(figsize=(8, 5))

        price_data = (
            df.groupby("Room_Type")["Base_Price"]
            .mean()
            .sort_values()
        )

        price_data.plot(
            kind="bar"
        )

        plt.title(
            "Average Room Price"
        )

        plt.xlabel(
            "Room Type"
        )

        plt.ylabel(
            "Average Price"
        )

        plt.xticks(
            rotation=25,
            ha="right"
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GRAPH_FOLDER,
                "price_graph.png"
            )
        )

        plt.close()


        # Guest Graph

        plt.figure(figsize=(8, 5))

        df["Guests"].value_counts().sort_index().plot(
            kind="bar"
        )

        plt.title(
            "Guest Distribution"
        )

        plt.xlabel(
            "Number of Guests"
        )

        plt.ylabel(
            "Number of Bookings"
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GRAPH_FOLDER,
                "guest_graph.png"
            )
        )

        plt.close()


        # Occupancy Graph

        plt.figure(figsize=(8, 5))

        occupancy = (
            df.groupby("Room_Type")["Guests"]
            .mean()
        )

        occupancy.plot(
            kind="bar"
        )

        plt.title(
            "Average Guests by Room"
        )

        plt.xlabel(
            "Room Type"
        )

        plt.ylabel(
            "Average Guests"
        )

        plt.xticks(
            rotation=25,
            ha="right"
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GRAPH_FOLDER,
                "occupancy_graph.png"
            )
        )

        plt.close()


        # Extra Guest Graph

        plt.figure(figsize=(8, 5))

        df["Extra_Guests"].value_counts().sort_index().plot(
            kind="bar"
        )

        plt.title(
            "Extra Guest Distribution"
        )

        plt.xlabel(
            "Extra Guests"
        )

        plt.ylabel(
            "Bookings"
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GRAPH_FOLDER,
                "extra_guest_graph.png"
            )
        )

        plt.close()


        # Day Price Graph

        plt.figure(figsize=(7, 5))

        day_price = (
            df.groupby("Day_Type")["Base_Price"]
            .mean()
        )

        day_price.plot(
            kind="bar"
        )

        plt.title(
            "Average Price by Day Type"
        )

        plt.xlabel(
            "Day Type"
        )

        plt.ylabel(
            "Average Price"
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GRAPH_FOLDER,
                "day_price_graph.png"
            )
        )

        plt.close()


        # Season Graph

        plt.figure(figsize=(8, 5))

        season_price = (
            df.groupby("Season")["Base_Price"]
            .mean()
        )

        season_price.plot(
            kind="bar"
        )

        plt.title(
            "Average Price by Season"
        )

        plt.xlabel(
            "Season"
        )

        plt.ylabel(
            "Average Price"
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GRAPH_FOLDER,
                "season_graph.png"
            )
        )

        plt.close()


        print(
            "Graphs generated successfully."
        )

        print(
            "Graph directory:",
            os.path.abspath(
                GRAPH_FOLDER
            )
        )


    except Exception as error:

        print(
            "Graph Error:",
            error
        )


# Run directly

if __name__ == "__main__":

    generate_graphs()