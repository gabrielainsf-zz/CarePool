
function createDestinationChart(trips) {

    let meters = [];
    let colors = [];

    for (let i = 0; i < trips.length; i++) {
        meters.push(trips[i]['distance_meters'])


    let generateBackgroundColors = function() {
        let r = Math.floor(Math.random() * 255);
        let g = Math.floor(Math.random() * 255);
        let b = Math.floor(Math.random() * 255);

        return `rgb(${r}, ${b}, ${g})`;
    };

    let ctx = document.getElementById("carbonFootprintChart").getContext("2d")

    data = {
        datasets: [{
            data: counts,
            backgroundColor: colors
        }],

        labels: cities
    };

    let myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {}
    });
}