function sortTripsByDate(results) {
 
    const { trips, tripsAsPassenger, tripsByDate } = results;

    let todaysDate = new Date()
    let todaysDateUTC = Date.UTC(todaysDate.getUTCFullYear(),
                                 todaysDate.getUTCMonth(),
                                 todaysDate.getUTCDate())
   
    let upcomingTrips = [];
    let pastTrips = [];
    let todaysTrips = [];

    let passengerUpcomingTrips = [];
    let passengerPastTrips = [];
    let passengerTodaysTrips = [];

    for (let i = 0; i < trips.length; i++) {
        
        date = new Date(trips[i]["dateOfTrip"]);
        utc_date = Date.UTC(date.getUTCFullYear(),
                            date.getUTCMonth(),
                            date.getUTCDate());

        if (utc_date == todaysDateUTC) {
            todaysTrips.push(trips[i]);
        } else if (utc_date > todaysDateUTC) {
            upcomingTrips.push(trips[i]);
        } else if (utc_date < todaysDateUTC) {
            pastTrips.push(trips[i]);
        }
    }

    for (let i = 0; i < tripsAsPassenger.length; i++) {
        
        date = new Date(tripsAsPassenger[i]["dateOfTrip"]);
        utc_date = Date.UTC(date.getUTCFullYear(),
                            date.getUTCMonth(),
                            date.getUTCDate());


        if (utc_date == todaysDateUTC) {
            passengerTodaysTrips.push(tripsAsPassenger[i]);
        } else if (utc_date > todaysDateUTC) {
            passengerUpcomingTrips.push(tripsAsPassenger[i]);
        } else if (utc_date < todaysDateUTC) {
            passengerPastTrips.push(tripsAsPassenger[i]);
        }
    }

    createTripTable(todaysTrips, "Today\'s Trip", 'todayTable');
    createTripTable(upcomingTrips, 'Upcoming Trips', 'upcomingTable');
    createTripTable(pastTrips, 'Past trips', 'pastTable');

    createPassengerTripTable(passengerTodaysTrips, "Today\'s' Trips", 'passengerTodayTable')
    createPassengerTripTable(passengerUpcomingTrips, 'Upcoming Trips', 'passengerUpcomingTable')
    createPassengerTripTable(passengerPastTrips, 'Past Trips', 'passengerPastTable')

    createCarbonFootprintChart(trips);
    createCarbonFootprintOvertimeChart(tripsByDate);
}