document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("predictionForm");

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        const room_type = document.getElementById("room_type").value;
        const day_type = document.getElementById("day_type").value;
        const season = document.getElementById("season").value;
        const guests = parseInt(document.getElementById("guests").value);
        const extra_guests = parseInt(document.getElementById("extra_guests").value);

        try {

            const response = await fetch("/predict", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    room_type,
                    day_type,
                    season,
                    guests,
                    extra_guests

                })

            });

            const data = await response.json();

            if (!response.ok) {

                alert(data.error);

                return;

            }

            document.querySelector(".result-card").style.display = "block";

            document.getElementById("result").innerHTML = `

                <h1>₹ ${data.final_price}</h1>

                <p>AI Recommended Price</p>

            `;

            document.getElementById("demand").textContent = data.demand;

            document.getElementById("occupancy").textContent = data.occupancy + "%";

            document.getElementById("trend").textContent = data.trend;

            document.getElementById("confidence").textContent = data.confidence + "%";

            document.getElementById("summary").innerHTML = `

                <table class="summary-table">

                    <tr>

                        <td>Room Type</td>

                        <td>${room_type}</td>

                    </tr>

                    <tr>

                        <td>Day Type</td>

                        <td>${day_type}</td>

                    </tr>

                    <tr>

                        <td>Season</td>

                        <td>${season}</td>

                    </tr>

                    <tr>

                        <td>Guests</td>

                        <td>${guests}</td>

                    </tr>

                    <tr>

                        <td>Extra Guests</td>

                        <td>${extra_guests}</td>

                    </tr>

                    <tr>

                        <td>Base Price</td>

                        <td>₹${data.base_price}</td>

                    </tr>

                    <tr>

                        <td>Extra Charge</td>

                        <td>₹${data.extra_charge}</td>

                    </tr>

                    <tr>

                        <td><strong>Final Price</strong></td>

                        <td><strong>₹${data.final_price}</strong></td>

                    </tr>

                </table>

            `;

            document.getElementById("recommendation").innerHTML = `

                <p>${data.recommendation}</p>

            `;

            // Refresh generated graphs

            const timestamp = new Date().getTime();

            document.getElementById("priceGraph").src =
                data.price_graph + "?t=" + timestamp;

            document.getElementById("guestGraph").src =
                data.guest_graph + "?t=" + timestamp;

            document.getElementById("occupancyGraph").src =
                data.occupancy_graph + "?t=" + timestamp;

            document.querySelector(".graph-section").style.display = "block";

            document.querySelector(".result-card").scrollIntoView({

                behavior: "smooth"

            });

        }

        catch (error) {

            console.error(error);

            alert("Server Error");

        }

    });

});