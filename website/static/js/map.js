let map;
let marker;
let savedCoordinates = { lat: null, lng: null };

function initMap() {
    const defaultLocation = { lat: 21.1938, lng: 81.3509 };

    map = new google.maps.Map(document.getElementById("map"), {
        center: defaultLocation,
        zoom: 8,
    });

    marker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        draggable: false,
        animation: google.maps.Animation.BOUNCE,
    });

    savedCoordinates.lat = defaultLocation.lat;
    savedCoordinates.lng = defaultLocation.lng;

    document.getElementById("latitude").value = savedCoordinates.lat;
    document.getElementById("longitude").value = savedCoordinates.lng;

    map.addListener("click", function (event) {
        placeMarker(event.latLng);
    });

    function placeMarker(location) {
        marker.setPosition(location);
        map.setCenter(location);
        map.setZoom(14);

        savedCoordinates.lat = location.lat();
        savedCoordinates.lng = location.lng();

        document.getElementById("latitude").value = savedCoordinates.lat;
        document.getElementById("longitude").value = savedCoordinates.lng;
        console.log("Coordinates saved:", savedCoordinates);
    }
}