
function createCarbonFootprintChart(trips) {

    // Carbon saved bar chart w/ steps by month
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
        carbonDioxideCarpool.push(((trips[i]['distanceMeters']/1609.34) * 404)/1000);
        carbonDioxideIndividual.push((((trips[i]['distanceMeters']/1609.34) * 404)/1000)
                                        * (trips[i]['numPassengers'] + 1));
        trip.push(origin + ' to ' + destination);
    }

    let ctx = document.getElementById("carbonFootprintChart").getContext("2d")

    data = {
        datasets: [{
            label: "Carbon Dioxide per Rideshare",
            data: carbonDioxideCarpool,
            backgroundColor: "#808000"
        },{
            label: "Carbon Dioxide if Each Individual Drove",
            data: carbonDioxideIndividual,
            backgroundColor: "#7A1607"
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
                text: 'Liters of Carbon Dioxide Emitted Comparison'
            },
            scales: {
              xAxes: [{
                ticks: {
                  autoSkip: true,
                  maxRotation: 0,
                  minRotation: 0
                }
              }]
            }
        }
    });
}