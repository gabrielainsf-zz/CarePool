   function createPassengerTripTable(trips, title, elementID) {

        if (trips.length === 0) {
            return null;
        } else {
            let table = "<table class='table table-hover'>";
            table += '<br>';
            table += `<h3>${title}</h3>`;
            table += "<th><i class='far fa-calendar fa-2x'></i></th>";
            table += "<th><i class='fas fa-map-marker-alt fa-2x'></i></th>";
            table += "<th><i class='fas fa-map-marked-alt fa-2x'></i></th>";
            table += "<th><i class='fas fa-car fa-2x'></i></th>";

            
            for (let i = trips.length-1; i >= 0; i--) {

                let driverProfileImg = trips[i]["driverProfileImg"];
                let driverBio = trips[i]["driverBio"]
                let driverName = trips[i]["driverFirstName"]

                table += "<tr>";
                table += "<td>" + trips[i]["dateOfTrip"]+"</td>";
                table += "<td>" + trips[i]["origin"]+"</td>";
                table += "<td>" + trips[i]["destination"]+"</td>";
                table += "<td>" + `<img src="${driverProfileImg}" class="rounded-circle passenger-img" id="popover" data-toggle="popover" data-placement="right" tabindex="0" data-trigger="hover" data-content="<strong>${driverName}</strong>  ${driverBio}">`
                                    + "<br>"
                                    + "<button type='button' class='badge btn-custom' data-toggle='modal' data-target='#exampleModalCenter'>Message</button>"
                                + "</td>";
        
                table += "</tr>";
            }  

            table += "</table>";
            document.getElementById(elementID).innerHTML = table;
            }

    }