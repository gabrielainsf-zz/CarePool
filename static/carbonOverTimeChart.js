
function createCarbonFootprintOvertimeChart(trips, tripsAsPass) {


    let date = [];
    let totalCarbon = 0;
    let totalCarbonPerPerson = 0;
    let totalCarbonArray = [];
    let totalCarbonPerPersonArray = [];

    console.log(trips);
    function populateArrays(listOfTrips) {
        console.log(listOfTrips);
       for (let i = 0; i < listOfTrips.length; i++) {

            totalCarbon += ((listOfTrips[i]['distanceMeters']/1609.34) * 404);
            totalCarbonArray.push(totalCarbon);
            totalCarbonPerPerson += (((listOfTrips[i]['distanceMeters']/1609.34) * 404)
                                            * (listOfTrips[i]['numPassengers'] + 1));
            totalCarbonPerPersonArray.push(totalCarbonPerPerson);
            date.push(listOfTrips[i]['dateOfTrip']);
        } 
    }

    populateArrays(trips);
    populateArrays(tripsAsPass);


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