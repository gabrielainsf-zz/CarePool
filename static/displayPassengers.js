function displayPassengers(passengerList) {
    for (let i = 0; i < passengerList.length; i++) {
        passengerFirstName = passengerList[i]["userFirstName"];
        passengerProfileImg = passengerList[i]["userProfileImg"];

        table += "<td>" + (passengerFirstName != undefined ? `<img 
                          src=${passengerProfileImg}>`
                        +  '&nbsp; &nbsp;'
                        +  passengerFirstName
                        +  '&nbsp; &nbsp;'
                        +  '<button type="button" class="btn btn-sm btn-primary" data-toggle="modal" data-target="#exampleModalCenter">Message</button>'
                       : "No passengers yet!");
                         + "</td>";
    }
}