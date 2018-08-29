
function createCarbonFootprintOvertimeChart(trips) {

    let date = [];
    let totalCarbon = 0;
    let totalCarbonPerPerson = 0;
    let totalCarbonArray = [];
    let totalCarbonPerPersonArray = [];
    let totalCarbonSaved = 0;
    let totalCarbonSavedArray = [];

   for (let trip in trips) {
        totalCarbon += ((trips[trip]['distanceMeters']/1609.34) * 404);
        totalCarbonPerPerson += (((trips[trip]['distanceMeters']/1609.34) * 404)
                                        * (trips[trip]['numPassengers'] + 1));
        totalCarbonSaved = totalCarbonPerPerson - totalCarbon
        totalCarbonSavedArray.push(totalCarbonSaved)
        date.push(trip);     
    }

    let ctx = document.getElementById("carbonFootprintOverTimeChart").getContext("2d")

    data = {
        datasets: [{
            label: "Total Carbon Saved",
            data: totalCarbonSavedArray,
            borderColor: "#8e5ea2",
            fill: false
        },
        // {
        //     label: "Carbon Dioxide if Each Individual Drove",
        //     data: totalCarbonPerPersonArray,
        //     borderColor: "#3e95cd",
        //     fill: false
        // }
        ],

        labels: date
    };

    let myDoughnutChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            legend: { display: true },
            title: {
                display: true,
                text: 'CO2 Saved Over Time'
            }
        }
    });
}