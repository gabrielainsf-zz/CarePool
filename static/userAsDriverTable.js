function createTripTable(trips, title, elementID) {

    if (trips.length === 0) {
        return null;
    } else {
        let table = "<table class='table table-hover'>";
        table += '<br>'
        table += `<h3>${title}</h3>`;
        table += "<thead>";
        table += "<tr>";
        table += "<th><i class='far fa-calendar fa-2x'></i></th>";
        table += "<th><i class='far fa-clock fa-2x'></i></th>";
        table += "<th><i class='fas fa-map-marker-alt fa-2x'></i></th>";
        table += "<th><i class='fas fa-map-marked-alt fa-2x'></i></th>";
        table += "<th><i class='fas fa-car fa-2x'></i></th>";
        table += "</tr>";
        table += "</thead>";
        
        for (let i = trips.length-1; i >= 0; i--) {

            table += "<tbody>";
            table += "<tr>";
            table += "<td>" + trips[i]["dateOfTrip"]+"</td>";
            table += "<td>" + trips[i]["time"]+"</td>";
            table += "<td>" + trips[i]["origin"]+"</td>";
            table += "<td>" + trips[i]["destination"]+"</td>";

            passengerList = trips[i]["passengers"];

            if (passengerList.length === 0) {
                table +=  "<td> No passengers ~</td>";
            } else {
                table += "<td>"
                for (let j = 0; j < passengerList.length; j++) {
                    let passengerFirstName = passengerList[j]["userFirstName"]
                    let passengerProfileImg = passengerList[j]["userProfileImg"]
                    let passengerBio = passengerList[j]["userBio"]

                    table += "<div class='row'>"
                                    + "<div class='col-sm'>"
                                    + `<img src=${passengerProfileImg} class="passenger-img rounded-circle" id="popover" data-placement="right" data-toggle="popover" tabindex="0" data-trigger="hover" data-content="<strong>${passengerFirstName}</strong>  ${passengerBio}">`
                                    + "<br>"
                                    + '<button type="button" class="badge btn-custom" data-toggle="modal" data-target="#exampleModalCenter">Message</button>'
                                    + "</div>"
                                    + "</div>"
                                    + "<br>"
                } 
                table += "</td>"
            }
            table += "</tr>";
        }  
        table += "</tbody>"
        table += "</table>";
        document.getElementById(elementID).innerHTML = table;
        
    }

}