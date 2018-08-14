
// Google Place API
let inputs = document.getElementsByClassName('query');

let options = {
    types: ['(cities)'],
    componentRestrictions: {country: "us"}
}; 

function initialize() {
    for (let i = 0; i < inputs.length; i++) {

        // Instantiate Autocomplete object for each input
        let autocomplete = new google.maps.places.Autocomplete(inputs[i], options);
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
        });
    }

    // Prevent auto-submit on first 'enter' click
    $('.query').keydown(function (e) {
      if (e.which == 13 && $('.pac-container:visible').length)
        return false;
    });
}
