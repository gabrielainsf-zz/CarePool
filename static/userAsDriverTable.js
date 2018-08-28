function createTripTable(trips, title, elementID) {

    if (trips.length === 0) {
        return null;
    } else {
        let table = "<table class='table'>";
        table += `<h3>${title}</h3>`;
        table += "<thead>";
        table += "<tr>";
        table += "<th scope='col'>Date:</th>";
        table += "<th scope='col'>From:</th>";
        table += "<th scope='col'>To:</th>";
        table += "<th scope='col'>Passengers:</th>";
        table += "</tr>";
        table += "</thead>";

        
        for (let i = trips.length-1; i >= 0; i--) {

            table += "<tbody>";
            table += "<tr>";
            table += "<td>" + trips[i]["dateOfTrip"]+"</td>";
            table += "<td>" + trips[i]["origin"]+"</td>";
            table += "<td>" + trips[i]["destination"]+"</td>";

            passengerList = trips[i]["passengers"];

            if (passengerList.length === 0) {
                table +=  "<td> No passengers yet! </td>";
            } else {
                for (let j = 0; j < passengerList.length; j++) {
                    passengerFirstName = passengerList[j]["userFirstName"]
                    passengerProfileImg = passengerList[j]["userProfileImg"]

                    table += "<td>" + `<img src=${passengerProfileImg}>`
                                    +  '&nbsp; &nbsp;'
                                    +  passengerFirstName
                                    +  '&nbsp; &nbsp;'
                                    +  '<button type="button" class="btn btn-sm btn-primary" data-toggle="modal" data-target="#exampleModalCenter">Message</button>'
                                    + "</td>"
                } 
            }
            
            table += "</tr>";
        }  
        table += "</tbody>"
        table += "</table>";
        document.getElementById(elementID).innerHTML = table;
        
        }

}

// function displayPassengers(passengerFirstName, passengerProfileImg) {

//         += "<td>" + (passengerFirstName != undefined ? `<img 
//           src=${passengerProfileImg}>`
//         +  '&nbsp; &nbsp;'
//         +  passengerFirstName
//         +  '&nbsp; &nbsp;'
//         +  '<button type="button" class="btn btn-sm btn-primary" data-toggle="modal" data-target="#exampleModalCenter">Message</button>'
//        : "No passengers yet!");
//          + "</td>";

// }