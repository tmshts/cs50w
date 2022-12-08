document.addEventListener('DOMContentLoaded', function() {

    let description = document.querySelector('#property_description')
    if (description) {
        plain_text = document.querySelector('#property_description').innerHTML
        html_text = plain_text.replace(/\r?\n/g, '<br />');
        document.querySelector('#property_description').innerHTML = html_text;
    }
      
    // Button to edit description
    const edit_description = document.querySelector('#edit_description');
    if (edit_description){
        edit_description.addEventListener('click', () => handle_description());
        }

    // Button to edit price
    const edit_price = document.querySelector('#edit_price');
    if (edit_price){
        edit_price.addEventListener('click', () => handle_price());
        }

    // Button to edit title
    const edit_title = document.querySelector('#edit_title');
    if (edit_title){
        edit_title.addEventListener('click', () => handle_title());
        }

    // Button to delete pictures
    const delete_pictures = document.querySelector('#delete_pictures');
    if (delete_pictures){
        delete_pictures.addEventListener('click', () => handle_pictures());
        }

    let longitude = document.querySelector('#longitude');
    if (longitude) {
        longitude = document.querySelector('#longitude').innerHTML;
    }

    let latitude = document.querySelector('#latitude');
    if (latitude) {
        latitude = document.querySelector('#latitude').innerHTML;
    }

    document.querySelector('#map').style.height = '250px';
    document.querySelector('#map').style.width = '100%';

    // Show map with a position of property
    //if (!(longitude == 0 && latitude == 0)){

        var map = L.map('map').setView([latitude, longitude], 14);
        map.attributionControl.setPrefix(false)
    
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://leafletjs.com/">Leaflet</a> &copy; <a href="http://www.openstreetmap.org/">OpenStreetMap</a>',
            }).addTo(map);
          
        var marker = L.marker([latitude, longitude]).addTo(map);

        const title = document.querySelector('#title').innerHTML;
    
        marker.bindPopup(`<b>${title}</b>`).openPopup();
    //}
    // Since user has to find his/her property -> latitude and longitude should not be 0, but
    // it can happen that user overwrites the fields for latitude and longitude
    //else {
    //    const message_div = document.createElement('div');
    //    message_div.className = 'no_search';
    //    message_div.innerHTML = `A map is not shown as the location can not be found.`;
    //    document.querySelector('#map').append(message_div)
    //    document.querySelector('#map').style.height = '40px';
    //    document.querySelector('#map').style.marginBottom = '40px';
    //}

    // Button to show contact
    const show_contact = document.querySelector('#show_contact');
    if (show_contact){
        show_contact.addEventListener('click', () => handle_contact());
        }

});

function handle_contact(){

    // Hide button contact details
    document.querySelector('#open_div_request').style.display = 'none';

    // Get property_id
    const property_id = document.querySelector('#property_id').innerHTML;

    // CSRF token
    const csrftoken = getCookie('csrftoken');

    // Communicate with back end regarding contact
    fetch('/property/' + property_id, {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({
            pro_id: property_id,
            })
    })
    .then(response => response.json())
    .then(result => {

        // Create elements
        const contact_details_div = document.createElement('div');
        const email_div = document.createElement('div');
        const email_value = document.createElement('b');
        const whatsapp_div = document.createElement('div');
        const whatsapp_value = document.createElement('b');

        // Fill elements
        contact_details_div.className = 'contact_details_div_class';
        email_div.className = 'email_div_class';
        email_div.innerHTML = 'Email:';
        email_value.className = 'email_value_class';
        email_value.innerHTML = result.email;
        whatsapp_div.className = 'whatsapp_div_class';
        whatsapp_div.innerHTML = 'WhatsApp:';
        whatsapp_value.className = 'whatsapp_value_class';
        whatsapp_value.innerHTML = result.whatsapp;

        // Added to the DOM
        document.querySelector('#contact_details').append(contact_details_div);
        document.querySelector('#contact_details').append(email_div);
        document.querySelector('#contact_details').append(email_value);
        document.querySelector('#contact_details').append(whatsapp_div);
        document.querySelector('#contact_details').append(whatsapp_value);
    })

   
}

function handle_pictures() {
    // Get property_id
    const property_id = document.querySelector('#property_id').innerHTML;

    // CSRF token
    const csrftoken = getCookie('csrftoken');

    // Communicate with back end regarding pictures
    fetch('/property/' + property_id, {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({
            property_id: property_id,
            })
    })
    .then(response => response.json())
    .then(result => {
                    document.location.reload() 
            })
    
}

function handle_title() {
    // Hide description
    document.querySelector('#title').style.display = 'none';
    document.querySelector('#title_hide').style.display = 'none';

    // Get title
    let title = document.querySelector('#title').innerHTML;

    // Create elements
    const div_for_edit_title = document.createElement('div');
    const edit_title = document.createElement("input");
    edit_title.type = "text";
    const edit_buttons_title = document.createElement('div')
    const edit_save_title = document.createElement('button');
    const edit_cancel_title = document.createElement('button');

    // Fill elements
    div_for_edit_title.className = 'div_for_edit_class_title';
    edit_buttons_title.className = 'edit_buttons_class';
    edit_title.className = 'edit_textarea_class_title inputfield';
    edit_title.value = title;
    edit_title.style.marginTop = '25px';

    edit_save_title.innerHTML = 'Save';
    edit_save_title.className = 'edit_save_class_title btn_design';
    edit_cancel_title.className = 'edit_cancel_class_title btn_design';
    edit_cancel_title.innerHTML = 'Cancel';

    edit_buttons_title.append(edit_save_title)
    edit_buttons_title.append(edit_cancel_title)

    div_for_edit_title.append(edit_title)
    div_for_edit_title.append(edit_buttons_title)

    // Added to the DOM
    document.querySelector('#div_for_title').append(div_for_edit_title);

    // Save price
    document.querySelector('.edit_save_class_title').addEventListener('click', () => {
    const edited_title = document.querySelector('.edit_textarea_class_title').value;
    const property_id_title = document.querySelector('#property_id').innerHTML

    // CSRF token
    const csrftoken = getCookie('csrftoken');

        // Communicate with back end regarding title
        fetch('/property/' + property_id_title, {
            method: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({
                edited_title: edited_title,
                })
        })
        .then(response => response.json())
        .then(result => {
                    document.querySelector('.div_for_edit_class_title').remove() ;
                    document.querySelector('#title').innerHTML = result.title;
                    document.querySelector('#title').style.display = 'block';
                    document.querySelector('#title_hide').style.display = 'block';
                })
        });

        // Cancel price
        document.querySelector('.edit_cancel_class_title').addEventListener('click', () => {
        document.querySelector('#title').style.display = 'block';
        document.querySelector('#title_hide').style.display = 'block';
        document.querySelector('.div_for_edit_class_title').remove();
        });  

}

function handle_price() {
    // Hide description
    document.querySelector('#price_div').style.display = 'none';
    document.querySelector('#price_hide').style.display = 'none';

    // Get default price
    let price = document.querySelector('#default_price').innerHTML;

    // Create elements
    const div_for_edit_price = document.createElement('div');
    const currency_symbol = document.createElement('b');
    const edit_price = document.createElement("input");
    edit_price.type = "float";
    const edit_buttons_price = document.createElement('div')
    const edit_save_price = document.createElement('button');
    const edit_cancel_price = document.createElement('button');

    // Fill elements
    div_for_edit_price.className = 'div_for_edit_class_price';
    currency_symbol.innerHTML = 'USD'
    edit_buttons_price.className = 'edit_buttons_class';
    edit_price.className = 'edit_textarea_class_price inputfield';
    edit_price.value = price;
    edit_save_price.innerHTML = 'Save';
    edit_save_price.className = 'edit_save_class_price btn_design';
    edit_cancel_price.className = 'edit_cancel_class_price btn_design';
    edit_cancel_price.innerHTML = 'Cancel';

    edit_buttons_price.append(edit_save_price)
    edit_buttons_price.append(edit_cancel_price)

    div_for_edit_price.append(currency_symbol)
    div_for_edit_price.append(edit_price)
    div_for_edit_price.append(edit_buttons_price)

    // Added to the DOM
    document.querySelector('#div_for_price').append(div_for_edit_price);

    // Save price
    document.querySelector('.edit_save_class_price').addEventListener('click', () => {
    const edited_price = document.querySelector('.edit_textarea_class_price').value;
    const property_id_price = document.querySelector('#property_id').innerHTML

    // CSRF token
    const csrftoken = getCookie('csrftoken');

        // Communicate with back end regarding contact
        fetch('/property/' + property_id_price, {
            method: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({
                edited_price: edited_price,
                })
        })
        .then(response => response.json())
        .then(result => {
                    document.querySelector('.div_for_edit_class_price').remove() ;
                    document.querySelector('#price').innerHTML = result.price;
                    document.querySelector('#currency_symbol').innerHTML = 'USD';
                    document.querySelector('#price_div').style.display = 'block';
                    document.querySelector('#price_hide').style.display = 'block';
                    document.querySelector('#default_price').innerHTML = result.price;

                    //after I save it I should change selection on USD option
                    document.querySelector('.currency_select').value = 'USD'
                })
        //.catch((error) => {
            //alert("Please write just digits")
            //console.log(error)
            //});
        });

        // Cancel price
        document.querySelector('.edit_cancel_class_price').addEventListener('click', () => {
        //alert("You want to cancel?")
        document.querySelector('#price_div').style.display = 'block';
        document.querySelector('#price_hide').style.display = 'block';
        document.querySelector('.div_for_edit_class_price').remove();
        });

}

function handle_description() {

    // Hide description
    document.querySelector('#property_description').style.display = 'none';
    document.querySelector('#description_hide').style.display = 'none';

    // Get property description
    let property_description = document.querySelector('#property_description').innerHTML;

    // Create elements
    const div_for_edit_description = document.createElement('div');
    const edit_textarea = document.createElement('textarea');
    const edit_buttons_description = document.createElement('div')
    const edit_save_description = document.createElement('button');
    const edit_cancel_description = document.createElement('button');

    // Fill elements
    div_for_edit_description.className = 'div_for_edit_class_description';
    edit_buttons_description.className = 'edit_buttons_class';
    edit_textarea.className = 'edit_textarea_class_description inputfield';

    edit_textarea.style.height = '190px';
    edit_textarea.style.width = '100%';
    let regex = /(<([^>]+)>)/ig;
    edit_textarea.value = property_description.replace(regex, '\n');

    edit_save_description.innerHTML = 'Save';
    edit_save_description.className = 'edit_save_class_description btn_design';
    edit_cancel_description.className = 'edit_cancel_class_description btn_design';
    edit_cancel_description.innerHTML = 'Cancel'; 

    edit_buttons_description.append(edit_save_description)
    edit_buttons_description.append(edit_cancel_description)

    div_for_edit_description.append(edit_textarea)
    div_for_edit_description.append(edit_buttons_description)

    // Added to the DOM
    document.querySelector('#div_for_textarea').append(div_for_edit_description);

    // Save change
    document.querySelector('.edit_save_class_description').addEventListener('click', () => {
        const edited_text = document.querySelector('.edit_textarea_class_description').value;
        const property_id_description = document.querySelector('#property_id').innerHTML

        // CSRF token
        const csrftoken = getCookie('csrftoken');

            // Communicate with back end regarding description
            fetch('/property/' + property_id_description, {
                method: 'POST',
                headers: {"X-CSRFToken": csrftoken},
                body: JSON.stringify({
                    edited_text: edited_text,
                    })
            })
            .then(response => response.json())
            .then(result => {
                        document.querySelector('.div_for_edit_class_description').remove() ;
                        plain_text = result.description
                        html_text = plain_text.replace(/\r?\n/g, '<br />');
                        document.querySelector('#property_description').innerHTML = html_text;
                        document.querySelector('#property_description').style.display = 'block';
                        document.querySelector('#description_hide').style.display = 'block';
                    })
        });

        // Cancel change
        document.querySelector('.edit_cancel_class_description').addEventListener('click', () => {
        document.querySelector('#property_description').style.display = 'block';
        document.querySelector('#description_hide').style.display = 'block';
        document.querySelector('.div_for_edit_class_description').remove();
        });    

}

// taken from https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax
// Generate CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
