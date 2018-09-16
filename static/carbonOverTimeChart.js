
function createCarbonFootprintOvertimeChart(trips) {

    let date = [];
    let totalCarbon = 0;
    let totalCarbonPerPerson = 0;
    let totalCarbonArray = [];
    let totalCarbonPerPersonArray = [];
    let totalCarbonSaved = 0;
    let totalCarbonSavedArray = [];

   for (let trip in trips) {
        totalCarbon += (((trips[trip]['distanceMeters']/1609.34) * 404)/1000);
        totalCarbonPerPerson += ((((trips[trip]['distanceMeters']/1609.34) * 404)
                                        * (trips[trip]['numPassengers'] + 1))/1000);
        totalCarbonPerPersonArray.push(totalCarbonPerPerson);
        totalCarbonSaved = totalCarbonPerPerson - totalCarbon
        totalCarbonSavedArray.push(totalCarbonSaved);
        date.push(trip);     
    }

    let ctx = document.getElementById("carbonFootprintOverTimeChart").getContext("2d")

    data = {
        datasets: [{
            label: "Total CO2 Saved Each Trip",
            data: totalCarbonSavedArray,
            borderColor: "#FFB200",
            fill: false,
            steppedLine: true
        }],

        labels: date
    };

    let myDoughnutChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            legend: { display: true },
            title: {
                display: true,
                text: 'Liters of CO2 Saved Over Time'
            }
        }
    });
        roundedTotalCarbonReduced = Math.floor(totalCarbonSaved)
        document.getElementById("carbonReduced").innerHTML = roundedTotalCarbonReduced
}

