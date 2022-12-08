document.addEventListener('DOMContentLoaded', function() {

    // Delete property
    document.querySelectorAll('#btn-delete').forEach(eleme => {
        // () => 
       eleme.onclick = function() {
        delete_property(eleme)
       }
    });

    // Pause property
    document.querySelectorAll('#btn-pause').forEach(eleme => {
        // () => 
       eleme.onclick = function() {
        pause_property(eleme)
       }
    });

    // Default currency is USD
    if (document.querySelector('.currency_select')) {
        document.querySelector('.currency_select').value = 'USD'
    }

    // Change currency
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

    // Default order is Newest First
    if (document.querySelector('.order_select')) {
        document.querySelector('.order_select').value = 'new_first'
        }

    // Change Order
    const edit_order = document.querySelector('.order_select')
    if(edit_order){
        document.querySelector('.order_select').onchange = handle_order;
        }

    // Show All, Sales or Rent
    document.querySelectorAll('.salesrent').forEach(eleme => {
        eleme.onclick = function() {
            handle_search_salesrent(this.value)
        }
        });

    // Highligh buttons for sales_rent
    const button_container = document.getElementById("button_container");
    const buttons_in_container = button_container.getElementsByClassName("btn");
    for (let i = 0; i < buttons_in_container.length; i++) {
        buttons_in_container[i].addEventListener("click", function(){
            const current = document.getElementsByClassName("active");
            current[0].className = current[0].className.replace(" active", "");
            this.className += " active";
        });
    }
});

// Generate CSRF token
// taken from https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function handle_search_salesrent(sales_or_rent) {
    const selected_rent_list = document.querySelectorAll('.' + sales_or_rent);
    const entire_list = document.querySelectorAll('#flex-item-index');

    for(var i = 0; i < entire_list.length; i++){
        div_for_rent = entire_list[i]
        if (sales_or_rent == 'All') {
            div_for_rent.style.display = 'block'
        }
        else {
            div_for_rent.style.display = 'none'
            }
    }

    for(var i = 0; i < selected_rent_list.length; i++){
        div_for_rent = selected_rent_list[i].parentElement.parentElement.parentElement
        div_for_rent.style.display = 'block'
        }
}

function pause_property(eleme) {
    // Get the entire specific div
    const spec_div = eleme.parentElement;
    let property_id = spec_div.querySelector('#property_id').innerHTML;

    // CSRF token
    const csrftoken = getCookie('csrftoken');

    // Communicate with back-end to pause/activate property
    fetch('/property/' + property_id, {
        method: 'POST',
        // Place CSRF
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({
            active_pause_property_id: property_id,
            })
    })
    .then(response => response.json())
    .then(result => {
            spec_div.querySelector('#btn-pause').innerHTML = result.value;
        })        
}


function delete_property(eleme) {
    // Get the entire specific div
    const spec_div = eleme.parentElement;

    property_id = spec_div.querySelector('#property_id').innerHTML;

    // CSRF token
    const csrftoken = getCookie('csrftoken');

    // Communicate with back-end to delete property
    fetch('/property/' + property_id, {
        method: 'POST',
        // Place CSRF
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({
            prop_id: property_id,
            })
    })
    // Remove property div
    .then(spec_div.remove())
}

function handle_currency() {
    const selected_currency = this.value

    // Get default prices for every property and save it in list
    var default_prices_list = document.querySelectorAll('[id=default_price]');

    // Convert Nodelist to Array - not necessary
    //const default_prices_array = Array.from(default_prices_list)
    //console.log(default_prices_list)
    //console.log(default_prices_array)

    // Get other currencies compared to USD
    fetch('https://open.er-api.com/v6/latest/USD')
    // asynchronous process
    .then(response => {
        return response.json()
    })
    // different notation
    //.then(response => response.json())
    .then(data => {
        //console.log(data)
        const rate = data.rates[selected_currency];

        var prices_list = document.querySelectorAll('[id=price]');
        var currency_symbol_list = document.querySelectorAll('[id=currency_symbol]');
        
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

function handle_order() {
    const selected_order = this.value

    // Get all the divs
    let all_divs = document.querySelector('.flex-container').children;
    // Nodelist -> Array -> sort function works
    all_divs = Array.prototype.slice.call(all_divs, 0);

    if (selected_order === 'new_first') {
        all_divs.sort(function(a, b) {
            let new_a = a.querySelector('#second').querySelector('#date').innerHTML
            // Handle time
            let [monthStr_a, yearStr_a, timeStr_a] = new_a.split(',');
            // Handle month
            let [monthmonth_a, month_day_a] = monthStr_a.split(' ');
            let month_name_a = monthmonth_a.replaceAll('.','');
            // Handle year
            let year_a = yearStr_a.replaceAll(' ','')
            // Handle day
            let [space_a, time_a, m_a] = timeStr_a.split(' ')
            final_time_a = time_a + ':00'
            final_m_a = m_a.replaceAll('.','')
            final_m_a = final_m_a.toUpperCase()

            final_date_a = month_name_a + ' ' + month_day_a + ' ' + year_a + ' ' + final_time_a + ' ' + final_m_a
            // Convert date string into date
            date_a = new Date(final_date_a)

            let new_b = b.querySelector('#second').querySelector('#date').innerHTML
            let [monthStr_b, yearStr_b, timeStr_b] = new_b.split(',');
            // Handle month
            let [monthmonth_b, month_day_b] = monthStr_b.split(' ');
            let month_name_b = monthmonth_b.replaceAll('.','');
            // Handle year
            let year_b = yearStr_b.replaceAll(' ','')
            // Handle day
            let [space_b, time_b, m_b] = timeStr_b.split(' ')
            final_time_b = time_b + ':00'
            final_m_b = m_b.replaceAll('.','')
            final_m_b = final_m_b.toUpperCase()

            final_date_b = month_name_b + ' ' + month_day_b + ' ' + year_b + ' ' + final_time_b + ' ' + final_m_b
            // Convert date string into date
            date_b = new Date(final_date_b)

            return date_b - date_a;
        });
    }

    else if (selected_order === 'old_first') {
        all_divs.sort(function(a, b) {
            let new_a = a.querySelector('#second').querySelector('#date').innerHTML
            // Handle time
            let [monthStr_a, yearStr_a, timeStr_a] = new_a.split(',');
            // Handle month
            let [monthmonth_a, month_day_a] = monthStr_a.split(' ');
            let month_name_a = monthmonth_a.replaceAll('.','');
            // Handle year
            let year_a = yearStr_a.replaceAll(' ','')
            // Handle day
            let [space_a, time_a, m_a] = timeStr_a.split(' ')
            final_time_a = time_a + ':00'
            final_m_a = m_a.replaceAll('.','')
            final_m_a = final_m_a.toUpperCase()

            final_date_a = month_name_a + ' ' + month_day_a + ' ' + year_a + ' ' + final_time_a + ' ' + final_m_a
            // Convert date string into date
            date_a = new Date(final_date_a)

            let new_b = b.querySelector('#second').querySelector('#date').innerHTML
            //console.log(new_b)
            let [monthStr_b, yearStr_b, timeStr_b] = new_b.split(',');
            // Handle month
            let [monthmonth_b, month_day_b] = monthStr_b.split(' ');
            let month_name_b = monthmonth_b.replaceAll('.','');
            // Handle year
            let year_b = yearStr_b.replaceAll(' ','')
            // Handle day
            let [space_b, time_b, m_b] = timeStr_b.split(' ')
            final_time_b = time_b + ':00'
            final_m_b = m_b.replaceAll('.','')
            final_m_b = final_m_b.toUpperCase()

            final_date_b = month_name_b + ' ' + month_day_b + ' ' + year_b + ' ' + final_time_b + ' ' + final_m_b
            // Convert date string into date
            date_b = new Date(final_date_b)

            return date_a - date_b;
        });
    }

    else if (selected_order === 'big_first') {
        all_divs.sort(function(a, b) {
            let size_a = +a.querySelector('#second').querySelector('#default_size').innerHTML
            let size_b = +b.querySelector('#second').querySelector('#default_size').innerHTML
            return (size_b - size_a);
        }); 
    }

    else if (selected_order === 'small_first') {
        all_divs.sort(function(a, b) {
            let size_a = +a.querySelector('#second').querySelector('#default_size').innerHTML
            let size_b = +b.querySelector('#second').querySelector('#default_size').innerHTML
            return (size_a - size_b);
        });  
    }

    else if (selected_order === 'expensive_first') {

        all_divs.sort(function(a, b) {
            let price_a = +a.querySelector('#second').querySelector('#default_price').innerHTML
            let price_b = +b.querySelector('#second').querySelector('#default_price').innerHTML
            return (price_b - price_a);
        });
    }

    else if (selected_order === 'cheap_first') {
        all_divs.sort(function(a, b) {
            let price_a = +a.querySelector('#second').querySelector('#default_price').innerHTML
            let price_b = +b.querySelector('#second').querySelector('#default_price').innerHTML
            return (price_a - price_b);
        });
    }

    // Get parent node and clear it
    const parent_div = document.querySelector('.flex-container');
    parent_div.innerHTML = "";
    
    // Fill the parent node with the sorted divs
    for (let i = 0, l = all_divs.length; i < l; i++) {
        parent_div.appendChild(all_divs[i]);
    } 
}