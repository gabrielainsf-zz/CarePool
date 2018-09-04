
function createChartByMonth(trips) {

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
            label: "Total Carbon Saved",
            data: totalCarbonSavedArray,
            borderColor: "#8e5ea2",
            fill: false,
            steppedLine: true,
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

        document.getElementById("carbonReduced").innerHTML = totalCarbonSaved
}

