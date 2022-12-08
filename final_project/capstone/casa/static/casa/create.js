document.addEventListener('DOMContentLoaded', function() {

    // Find
    let find = document.querySelector('#find');
    if (find){
        find.addEventListener('click', () => find_address());
        }

    let map = L.map('map_create').setView([41.15, -96.50], 4);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(map);

    // To get latitude and longitude
    //map.on('click', function(e) {
    //    console.log("Latitude:" + e.latlng.lat + ", " + "Longitude:" + e.latlng.lng)
    //});

})

function show_addresses(){
    let addresses = document.querySelector('#addresses');

    addresses.innerHTML = '';
    if (address_data.length > 0) {
        address_data.forEach(address => {
            addresses.innerHTML += "<div class='address_result' onclick='select_address(" + '"' + address.display_name + '"' + "," 
                                    + address.lat + "," + address.lon + ")'>"
                                    + address.display_name 
                                    + "</div>"
        })
    }
}


function select_address(address, latitude, longitude) {

    let id_address = document.querySelector('#id_address')
    let id_longitude = document.querySelector('#id_longitude')
    let id_latitude = document.querySelector('#id_latitude')

    // Fill fields
    id_address.value = address
    id_latitude.value = latitude
    id_longitude.value = longitude


    let container = L.DomUtil.get('map_create');
    if(container != null){
        container._leaflet_id = null;
    }

    let map = L.map('map_create').setView([latitude, longitude], 4);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(map);

    // Create marker
    let marker = L.marker([latitude, longitude]).addTo(map)

    map.flyTo([latitude, longitude], 16, {
        duration: 3
    })
    //marker.setLatLng([latitude, longitude])

}

function find_address(){
    let address = document.querySelector('#address');

    url = 'https://nominatim.openstreetmap.org/search?format=json&limit=3&q=' + address.value
    fetch(url)
        .then(response => response.json())
        .then(data => address_data = data)
        .then(result => {
                //console.log(result);
                show_addresses()
            })
}