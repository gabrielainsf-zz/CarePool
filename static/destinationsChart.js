
function organizeData(trips) {

    let destinationsObj = {};

    for (let i = 0; i < trips.length; i++) {
        destination = trips[i]['destination']

        if (!(destination in destinationsObj)) {
            destinationsObj[destination] = 1;
        } else {
            destinationsObj[destination] += 1;
        } 
    }

    let cities = [];
    let counts = [];
    let colors = [];

    let generateBackgroundColors = function() {
        let r = Math.floor(Math.random() * 255);
        let g = Math.floor(Math.random() * 255);
        let b = Math.floor(Math.random() * 255);

        return `rgb(${r}, ${b}, ${g})`;
    };

    for (city in destinationsObj) {
        cities.push(city);
        counts.push(destinationsObj[city]);
        colors.push(generateBackgroundColors());
    }

    let ctx = document.getElementById("myChart").getContext("2d")

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