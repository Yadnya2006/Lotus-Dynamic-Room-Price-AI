import os
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


GRAPH_FOLDER = "static/graphs"

os.makedirs(GRAPH_FOLDER, exist_ok=True)


def generate_price_graph(base_price, extra_charge, final_price):

    plt.figure(figsize=(8, 5))

    labels = [
        "Base Price",
        "Extra Charge",
        "Final Price"
    ]

    values = [
        base_price,
        extra_charge,
        final_price
    ]

    colors = [
        "#3498db",
        "#f39c12",
        "#27ae60"
    ]

    bars = plt.bar(labels, values, color=colors)

    plt.title(
        "AI Dynamic Price Recommendation",
        fontsize=16,
        fontweight="bold"
    )

    plt.ylabel("Price (₹)")

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width()/2,
            height + 100,
            f"₹{int(height)}",
            ha="center",
            fontsize=11,
            fontweight="bold"
        )

    graph_path = os.path.join(
        GRAPH_FOLDER,
        "price_graph.png"
    )

    plt.tight_layout()

    plt.savefig(
        graph_path,
        dpi=180
    )

    plt.close()

    return graph_path


def generate_guest_graph(guests, extra_guests):

    plt.figure(figsize=(5, 5))

    labels = [
        "Guests",
        "Extra Guests"
    ]

    values = [
        guests,
        extra_guests
    ]

    colors = [
        "#3498db",
        "#e74c3c"
    ]

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90
    )

    plt.title(
        "Guest Distribution",
        fontsize=15,
        fontweight="bold"
    )

    graph_path = os.path.join(
        GRAPH_FOLDER,
        "guest_graph.png"
    )

    plt.savefig(
        graph_path,
        dpi=180
    )

    plt.close()

    return graph_path


def generate_occupancy_graph():

    plt.figure(figsize=(5, 5))

    labels = [
        "Occupied",
        "Available"
    ]

    values = [
        95,
        5
    ]

    colors = [
        "#2ecc71",
        "#ecf0f1"
    ]

    plt.pie(
        values,
        labels=labels,
        autopct="%1.0f%%",
        colors=colors,
        startangle=90
    )

    plt.title(
        "Expected Occupancy",
        fontsize=15,
        fontweight="bold"
    )

    graph_path = os.path.join(
        GRAPH_FOLDER,
        "occupancy_graph.png"
    )

    plt.savefig(
        graph_path,
        dpi=180
    )

    plt.close()

    return graph_path


def generate_all_graphs(
    base_price,
    extra_charge,
    final_price,
    guests,
    extra_guests
):

    generate_price_graph(
        base_price,
        extra_charge,
        final_price
    )

    generate_guest_graph(
        guests,
        extra_guests
    )

    generate_occupancy_graph()