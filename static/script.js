// Lotus Holiday Resort - JavaScript


// Format Price

function formatPrice(value) {

    return "₹" + Number(value).toLocaleString("en-IN");

}


// Prediction Form

const predictionForm = document.getElementById(
    "predictionForm"
);

const predictButton = document.getElementById(
    "predictButton"
);

const formError = document.getElementById(
    "formError"
);


predictionForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // Clear Error

        formError.textContent = "";


        // Get Values

        const roomType = document.getElementById(
            "roomType"
        ).value;

        const dayType = document.getElementById(
            "dayType"
        ).value;

        const season = document.getElementById(
            "season"
        ).value;

        const guests = document.getElementById(
            "guests"
        ).value;

        const extraGuests = document.getElementById(
            "extraGuests"
        ).value;


        // Basic Validation

        if (
            roomType === "" ||
            dayType === "" ||
            season === ""
        ) {

            formError.textContent =
                "Please select room type, day type and season.";

            return;

        }


        // Button Loading

        predictButton.disabled = true;

        predictButton.innerHTML =
            "⏳ Calculating Price...";


        try {


            // Send Data to Flask

            const response = await fetch(
                "/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        Room_Type: roomType,

                        Day_Type: dayType,

                        Season: season,

                        Guests: Number(
                            guests
                        ),

                        Extra_Guests: Number(
                            extraGuests
                        )

                    })
                }
            );


            // Read Response

            const result =
                await response.json();


            // Check Error

            if (
                !response.ok ||
                !result.success
            ) {

                throw new Error(
                    result.error ||
                    "Unable to calculate price."
                );

            }


            // Show Base Price

            document.getElementById(
                "basePrice"
            ).textContent =
                Number(
                    result.base_price
                ).toLocaleString("en-IN");


            document.getElementById(
                "basePriceDetail"
            ).textContent =
                formatPrice(
                    result.base_price
                );


            // Show Extra Guest Charge

            document.getElementById(
                "extraGuestCharge"
            ).textContent =
                formatPrice(
                    result.extra_guest_charge
                );


            // Show Total Price

            document.getElementById(
                "totalPrice"
            ).textContent =
                formatPrice(
                    result.total_price
                );


            // Show Room

            document.getElementById(
                "resultRoom"
            ).textContent =
                result.room_type;


            // Show Day

            document.getElementById(
                "resultDay"
            ).textContent =
                result.day_type;


            // Show Season

            document.getElementById(
                "resultSeason"
            ).textContent =
                result.season;


            // Show Guests

            document.getElementById(
                "resultGuests"
            ).textContent =
                result.guests +
                " Guest(s)";


            // Show Success Message

            document.getElementById(
                "resultMessage"
            ).textContent =
                "✨ Price calculated successfully for your selected stay.";


        }

        catch (error) {

            console.error(
                "Prediction Error:",
                error
            );

            formError.textContent =
                error.message ||
                "Something went wrong.";

        }


        finally {

            // Restore Button

            predictButton.disabled = false;

            predictButton.innerHTML =
                "<span>✨</span> Predict Room Price";

        }

    }
);


// Load ML Summary

async function loadMLSummary() {

    try {

        const response =
            await fetch(
                "/ml-summary"
            );

        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                data.error
            );

        }


        // Model Comparison

        const comparison =
            document.getElementById(
                "modelComparison"
            );


        let comparisonHTML =
            "<table>";

        comparisonHTML +=
            "<thead>";

        comparisonHTML +=
            "<tr>";

        comparisonHTML +=
            "<th>Model</th>";

        comparisonHTML +=
            "<th>MAE</th>";

        comparisonHTML +=
            "<th>RMSE</th>";

        comparisonHTML +=
            "<th>R² Score</th>";

        comparisonHTML +=
            "</tr>";

        comparisonHTML +=
            "</thead>";

        comparisonHTML +=
            "<tbody>";


        data.comparison.forEach(
            function (row) {

                comparisonHTML +=
                    "<tr>";

                comparisonHTML +=
                    "<td>" +
                    row.Model +
                    "</td>";

                comparisonHTML +=
                    "<td>" +
                    row.MAE +
                    "</td>";

                comparisonHTML +=
                    "<td>" +
                    row.RMSE +
                    "</td>";

                comparisonHTML +=
                    "<td>" +
                    row.R2 +
                    "</td>";

                comparisonHTML +=
                    "</tr>";

            }
        );


        comparisonHTML +=
            "</tbody>";

        comparisonHTML +=
            "</table>";


        comparison.innerHTML =
            comparisonHTML;


        // Cross Validation

        const crossValidation =
            document.getElementById(
                "crossValidation"
            );


        let cvHTML =
            "<table>";

        cvHTML +=
            "<thead>";

        cvHTML +=
            "<tr>";

        cvHTML +=
            "<th>Model</th>";

        cvHTML +=
            "<th>Mean R²</th>";

        cvHTML +=
            "<th>Standard Deviation</th>";

        cvHTML +=
            "</tr>";

        cvHTML +=
            "</thead>";

        cvHTML +=
            "<tbody>";


        data.cross_validation.forEach(
            function (row) {

                cvHTML +=
                    "<tr>";

                cvHTML +=
                    "<td>" +
                    row.Model +
                    "</td>";

                cvHTML +=
                    "<td>" +
                    row.Mean_R2 +
                    "</td>";

                cvHTML +=
                    "<td>" +
                    row.Standard_Deviation +
                    "</td>";

                cvHTML +=
                    "</tr>";

            }
        );


        cvHTML +=
            "</tbody>";

        cvHTML +=
            "</table>";


        crossValidation.innerHTML =
            cvHTML;


        // GridSearchCV

        const gridSearch =
            document.getElementById(
                "gridSearch"
            );


        if (
            data.gridsearch &&
            data.gridsearch.length > 0
        ) {

            const row =
                data.gridsearch[0];


            gridSearch.innerHTML =

                "<strong>Random Forest GridSearchCV</strong>" +

                "<br><br>" +

                "MAE: " +
                row.MAE +

                "<br>" +

                "RMSE: " +
                row.RMSE +

                "<br>" +

                "R² Score: " +
                row.R2;

        }

        else {

            gridSearch.textContent =
                "GridSearchCV results not available.";

        }


        // EDA Summary

        const edaSummary =
            document.getElementById(
                "edaSummary"
            );


        let edaHTML = "";


        data.eda.forEach(
            function (row) {

                edaHTML +=

                    '<div class="eda-item">' +

                    "<span>" +
                    row.Metric +
                    "</span>" +

                    "<strong>" +
                    row.Value +
                    "</strong>" +

                    "</div>";

            }
        );


        edaSummary.innerHTML =
            edaHTML;


    }

    catch (error) {

        console.error(
            "ML Summary Error:",
            error
        );


        document.getElementById(
            "modelComparison"
        ).textContent =
            "Unable to load model results.";


        document.getElementById(
            "crossValidation"
        ).textContent =
            "Unable to load validation results.";


        document.getElementById(
            "gridSearch"
        ).textContent =
            "Unable to load GridSearchCV results.";


        document.getElementById(
            "edaSummary"
        ).textContent =
            "Unable to load dataset summary.";

    }

}


// Load Dataset Information

async function loadDatasetInfo() {

    try {

        const response =
            await fetch(
                "/dataset-info"
            );

        const data =
            await response.json();


        if (!data.success) {

            return;

        }


        console.log(
            "Dataset Information:",
            data
        );


    }

    catch (error) {

        console.error(
            "Dataset Error:",
            error
        );

    }

}


// Start Page

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadMLSummary();

        loadDatasetInfo();

    }
);