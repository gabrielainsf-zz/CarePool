
function createCarbonFootprintChart(trips) {

    let meters = [];
    let trip = [];
    let carbonDioxideCarpool = [];
    let carbonDioxideIndividual = [];
    let colors = [];

    for (let i = 0; i < trips.length; i++) {
        originArray = trips[i]['origin'].split(',');
        origin = originArray[0];
        destinationArray = trips[i]['destination'].split(',');
        destination = destinationArray[0]

        meters.push(trips[i]['distanceMeters']);
        carbonDioxideCarpool.push((trips[i]['distanceMeters']/1609.34) * 404);
        carbonDioxideIndividual.push(((trips[i]['distanceMeters']/1609.34) * 404)
                                        * (trips[i]['numPassengers'] + 1));
        trip.push(origin + ' to ' + destination);
    }

    let ctx = document.getElementById("carbonFootprintChart").getContext("2d")

    data = {
        datasets: [{
            label: "Carbon Dioxide per Rideshare",
            data: carbonDioxideCarpool,
            backgroundColor: "#8e5ea2"
        },{
            label: "Carbon Dioxide if Each Individual Drove",
            data: carbonDioxideIndividual,
            backgroundColor: "#3e95cd"
        }],

        labels: trip
    };

    let myDoughnutChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            legend: { display: true },
            title: {
                display: true,
                text: 'Carbon Dioxide Emitted Comparison'
            }
        }
    });
}