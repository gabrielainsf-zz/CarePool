
function createCarbonFootprintOvertimeChart(trips) {


    let date = [];
    let totalCarbon = 0;
    let totalCarbonPerPerson = 0;
    let totalCarbonArray = [];
    let totalCarbonPerPersonArray = [];


    for (let i = 0; i < trips.length; i++) {

        totalCarbon += ((trips[i]['distance_meters']/1609.34) * 404);
        totalCarbonArray.push(totalCarbon);
        totalCarbonPerPerson += (((trips[i]['distance_meters']/1609.34) * 404)
                                        * (trips[i]['numPassengers'] + 1));
        totalCarbonPerPersonArray.push(totalCarbonPerPerson);
        date.push(trips[i]['dateOfTrip']);
    }


    let ctx = document.getElementById("carbonFootprintOverTimeChart").getContext("2d")

    data = {
        datasets: [{
            label: "Carbon Dioxide per Rideshare",
            data: totalCarbonArray,
            borderColor: "#8e5ea2",
            fill: false
        },{
            label: "Carbon Dioxide if Each Individual Drove",
            data: totalCarbonPerPersonArray,
            borderColor: "#3e95cd",
            fill: false
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
                text: 'Carbon Dioxide Emitted Comparison Over Time'
            }
        }
    });
}