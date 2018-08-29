   function createPassengerTripTable(trips, title, elementID) {

        if (trips.length === 0) {
            return null;
        } else {
            let table = "<table class='table table-dark'>";
            table += `<h3>${title}</h3>`;
            table += "<th>Date:</th>";
            table += "<th>From:</th>";
            table += "<th>To:</th>";
            table += "<th>Driver:</th>";

            
            for (let i = trips.length-1; i >= 0; i--) {

                let driverProfileImg = trips[i]["userProfileImg"];

                table += "<tr>";
                table += "<td>" + trips[i]["dateOfTrip"]+"</td>";
                table += "<td>" + trips[i]["origin"]+"</td>";
                table += "<td>" + trips[i]["destination"]+"</td>";
                table += "<td>" + `<img src="${driverProfileImg}">`
                                + '&nbsp; &nbsp;'
                                + trips[i]["userFirstName"]
                                + '&nbsp; &nbsp;'
                                + '<button type="button" class="btn btn-sm btn-primary" data-toggle="modal" data-target="#exampleModalCenter">Message</button>';
                                + "</td>";
        
                table += "</tr>";
            }  

            table += "</table>";
            document.getElementById(elementID).innerHTML = table;
            }

    }