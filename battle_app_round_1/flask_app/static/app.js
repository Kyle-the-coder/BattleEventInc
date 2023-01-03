
let autocomplete;

function initMap() {

    //Map option
    var options = {
        center: {lat: 37.8044 , lng: -122.2712},
        zoom: 10
    }
    //new map
    map = new google.maps.Map(document.getElementById('map'), options)
    
    //marker
    const marker =  new google.maps.Marker({
        position: {lat: 37.8044 , lng: -122.2712},
        map: map
    });




}    
