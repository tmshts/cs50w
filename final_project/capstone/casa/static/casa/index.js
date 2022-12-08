document.addEventListener('DOMContentLoaded', function() {

    // Default currency is USD
    if (document.querySelector('.currency_select')) {
    document.querySelector('.currency_select').value = 'USD'
    }

    // Change Currency
    const edit_currency = document.querySelector('.currency_select')
    if(edit_currency){
        document.querySelector('.currency_select').onchange = handle_currency;
        }

    // Default size is square meter
    if (document.querySelector('.metric_select')) {
        document.querySelector('.metric_select').value = 'feet'
    }

    // Change size
    const edit_size = document.querySelector('.metric_select')
    if(edit_size){
        document.querySelector('.metric_select').onchange = handle_metric;
        }

    // Filter
    const filter = document.querySelector('#btn_filter');
    if (filter){
        filter.addEventListener('click', () => handle_filter());
        }

    // Widest Screen of a Smartphone 414 px in 2021 https://worship.agency/mobile-screen-sizes-for-2021
    if (document.documentElement.clientWidth < 450) {
        document.querySelector('#map').style.height = '350px';

        let listings_div = document.getElementById('flex-container-index-id');
        listings_div.classList.remove('flex-container-index');
        listings_div.classList.add("flex-container-index_up");

        let map_div = document.getElementById('map');
        map_div.classList.remove('map_index');
        map_div.classList.add("map_index_down");
    }
    else {
        document.querySelector('#map').style.height = '550px';
    }

    // Set map
    let map = L.map('map').setView([41.15, -96.50], 4);
    map.attributionControl.setPrefix(false)

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://leafletjs.com/">Leaflet</a> &copy; <a href="http://www.openstreetmap.org/">OpenStreetMap</a>',
    }).addTo(map);

    // Button for 'search in this area' in leaflet map
    /*
    let search_button = document.getElementById('search_button');
    search_button.addEventListener('click', () => {
        let bounds = map.getBounds();
        console.log(bounds)

        let northeast = bounds.getNorthEast();
        let southwest = bounds.getSouthWest();
    
        console.log (
            'northeast:' + northeast +'\n'+
            'southwest:' + southwest +'\n'
        )

        let north_east_lat = northeast.lat
        let north_east_lng = northeast.lng
        let south_west_lat = southwest.lat
        let south_west_lng = southwest.lng

        console.log(
            'north_east_lat:' + north_east_lat + '\n' +
            'north_east_lng:' + north_east_lng + '\n' +
            'south_west_lat:' + south_west_lat + '\n' +
            'south_west_lng:' + south_west_lng + '\n'
        )
    });
    */

    // Fill the map with visible divs
    const entire_list = document.querySelectorAll('#flex-item-index');
    // Nodelist -> Array -> sort function works
    const entire_list_array = Array.from(entire_list)

    for(let i = 0; i < entire_list_array.length; i++){
        elem = entire_list_array[i]
        if (elem.style.display == 'block') {
            let latitude = elem.querySelector('#latitude').innerHTML
            let longitude = elem.querySelector('#longitude').innerHTML
            let url_property = elem.querySelector(".a_property_class").href;
            let image_source = elem.querySelector("#image_source").src;
            let property_type = elem.querySelector("#property_type").innerHTML;
            let sales_or_rent = elem.querySelector("#sales_or_rent").innerHTML;
            
            // Get address
            let street_number = elem.querySelector("#street_number").innerHTML;
            let city = elem.querySelector("#city").innerHTML; 
            let state = elem.querySelector("#state").innerHTML;
            let postal_code = elem.querySelector("#postal_code").innerHTML;

            // Get features
            let bedroom = elem.querySelector("#bedroom").innerHTML;
            let bathroom = elem.querySelector("#bathroom").innerHTML; 
            let size = elem.querySelector("#size").innerHTML;
            let metric = elem.querySelector("#metric").innerHTML; 
            let currency_symbol = elem.querySelector('#currency_symbol').innerHTML
            let price = elem.querySelector('#price').innerHTML

            //if (longitude != 0 && latitude != 0) {
                // Extract coordinates and save
                let coordinate_property = []
                coordinate_property.push(latitude)
                coordinate_property.push(longitude)

                // Extract currency and save
                let currency = []
                currency.push(currency_symbol)
                currency.push(price)

                // Create marker
                let marker = L.marker([coordinate_property[0], coordinate_property[1]]).addTo(map)

                // Pop Up with link leading to property
                let pop = L.popup({
                }).setContent(`<a href=${url_property} target="_blank" style="color: black; text-decoration: none;">
                            <b>${property_type} ${sales_or_rent}</b>
                            <br>
                            ${street_number}
                            <br>
                            ${city} ${state} ${postal_code}
                            <br>
                            <b style="color: blueviolet; font-size: 17px">${currency[0]} ${currency[1]}</b>
                            <br>
                            Beds: ${bedroom} &nbsp|&nbsp Bath ${bathroom} &nbsp|&nbsp Size ${size} ${metric}
                            <br>
                            <div style="text-align: center">
                                <img class="popup_image" src=${image_source}>
                            </div>
                        </a>`)

                marker.bindPopup(pop);


                // Labels with the prices
                let toollip = L.tooltip({
                    permanent: true
                }).setContent(`<b>${currency[0]} ${currency[1]}</b>`)

                marker.bindTooltip(toollip)


                // Look Up Property on map
                //elem.addEventListener('mouseover', function() {
                //    map.flyTo([coordinate_property[0], coordinate_property[1]], 15);
                //})
            //}

        }
    }
});

function handle_filter() {
    // Hide Filter Button
    document.querySelector('#btn_filter').style.display = 'none';
    // Show Filter Div
    document.querySelector('#filter_div').style.display = 'block';

    document.querySelector('.filter_cancel').addEventListener('click', () => {

        // Hide Filter Button
        document.querySelector('#btn_filter').style.display = 'block';
        // Show Filter Div
        document.querySelector('#filter_div').style.display = 'none'; 
    });
}

// Only for 1 page
function handle_currency() {
    const selected_currency = this.value      

    // Get default prices for every property and save it in list
    let default_prices_list = document.querySelectorAll('[id=default_price]');

    // Get other currencies compared to USD
    //fetch('https://open.er-api.com/v6/latest/USD')
    fetch(`https:/api.exchangerate.host/convert?from=USD&to=${selected_currency}`)
    
    // asynchronous process
    .then(response => {
        //console.log(response)
        return response.json()
    })
    // different notation
    //.then(response => response.json())
    .then(data => {
        //console.log(data)
        //const rate = data.rates[selected_currency];
        const rate = data.result

        let prices_list = document.querySelectorAll('[id=price]');
        let currency_symbol_list = document.querySelectorAll('[id=currency_symbol]');
        
        // For each div change the currency
        for(var i = 0; i < prices_list.length; i++){
           converted_price = default_prices_list[i].innerHTML * rate

           formated_convert_price = new Intl.NumberFormat('en-US', { 
            style: 'currency',
            currency: selected_currency, 
            currencyDisplay: "code",
            minimumFractionDigits:0, maximumFractionDigits:0
            })
            .format(converted_price)
            .replace(selected_currency, "")
            .trim();

           prices_list[i].innerHTML = formated_convert_price
           currency_symbol_list[i].innerHTML = selected_currency
        }
    });
}

// Only for 1 page
function handle_metric() {
    const selected_metric = this.value

    // Get metric for every property and save it in list -> Nodelist
    let default_size_list = document.querySelectorAll('[id=default_size]');

    let size_list = document.querySelectorAll('[id=size]');
    let metric_symbol_list = document.querySelectorAll('[id=metric]');

    if (selected_metric == 'feet') {
        for(let i = 0; i < size_list.length; i++){
            size_list[i].innerHTML = default_size_list[i].innerHTML
            metric_symbol_list[i].innerHTML = 'ft²'
            }
    }
    else {
        for(let i = 0; i < size_list.length; i++){
            converted_size = default_size_list[i].innerHTML / 10.7639
            new_converted_size = converted_size.toLocaleString('en-US', {minimumFractionDigits:0, maximumFractionDigits:0})
            size_list[i].innerHTML = new_converted_size
            metric_symbol_list[i].innerHTML = 'm²'
            }
    }
}