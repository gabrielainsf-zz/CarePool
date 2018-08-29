
function createCarbonFootprintChart(trips) {

    let meters = [];
    let trip = [];
    let carbonDioxideCarpool = [];
    let carbonDioxideIndividual = [];
    let colors = [];

    let generateBackgroundColors = function() {
        let r = Math.floor(Math.random() * 255);
        let g = Math.floor(Math.random() * 255);
        let b = Math.floor(Math.random() * 255);

        return `rgb(${r}, ${b}, ${g})`;
    };

    for (let i = 0; i < trips.length; i++) {
        originArray = trips[i]['origin'].split(',');
        origin = originArray[0];
        destinationArray = trips[i]['destination'].split(',');
        destination = destinationArray[0]

        meters.push(trips[i]['distance_meters']);
        carbonDioxideCarpool.push((trips[i]['distance_meters']/1609.34) * 404);
        carbonDioxideIndividual.push(((trips[i]['distance_meters']/1609.34) * 404)
                                        * (trips[i]['numPassengers'] + 1));
        trip.push(origin + ' to ' + destination);
        colors.push(generateBackgroundColors());
    }

    console.log(carbonDioxideIndividual)
    console.log(carbonDioxideCarpool)

    let ctx = document.getElementById("carbonFootprintChart").getContext("2d")

    data = {
        datasets: [{
            label: "Carbon Dioxide Carpool",
            data: carbonDioxideCarpool,
            backgroundColor: "#8e5ea2"
        },{
            label: "Carbon Dioxide Each Passenger",
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
                text: 'Carbon Dioxide Saved'
            }
        }
    });
}