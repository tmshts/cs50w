document.addEventListener('DOMContentLoaded', function() {

    const followers_button = document.querySelector('#follow_button');

    if(followers_button){
        followers_button.addEventListener('click', () => handle_followers());
    }

    document.querySelectorAll('#likes_button').forEach(eleme => {
        // () => 
       eleme.onclick = function() {
        handle_likes(eleme)
       }
    });

    document.querySelectorAll('#edit_button').forEach(elem => {
        // () => 
       elem.onclick = function() {
        handle_edit(elem)
       }
    });

});

function handle_followers() {
    //alert("click")

    const wants_follow_user = document.querySelector('#wants_follow').innerHTML;
    //alert(wants_follow_user)
    const is_followed_user = document.querySelector('#is_followed').innerHTML;
    //alert(is_followed_user)

    // Check followers and following for the specific user -> first send data
    fetch('/profil/' + wants_follow_user, {
        method: 'POST',
        body: JSON.stringify({
            wants_follow: wants_follow_user,
            is_followed: is_followed_user,
            })
      })
    .then(response => response.json())
    .then(result => {
                    //console.log(result.user_follow_counts)
                    //console.log(result.user_is_followed_counts)
                    //console.log(result.follow)
                    document.getElementById("following_id").innerHTML = result.user_follow_counts
                    document.getElementById("followers_id").innerHTML = result.user_is_followed_counts
                    document.getElementById("follow_button").innerHTML = result.follow
            })
    /*
    // second solution to the "Follow" and "Unfollow" button
    const btn = document.getElementById("follow_button");
    if (btn.innerText === "Follow") {
        btn.innerText = "Unfollow";
    }
    else {
        btn.innerText= "Follow";
    }
    */
}

function handle_likes(eleme) {
    // Get the entire specific div
    const spec_div = eleme.parentElement;
    
    number_of_likes = spec_div.querySelector("#likes_value").innerHTML
    current_user = spec_div.querySelector("#current_user").innerHTML
    post_id = spec_div.querySelector('#post_id').innerHTML;
    //alert(post_id)
    //alert("Like clicked")

    // Check likes
    fetch('/likes/' + post_id, {
        method: 'POST',
        body: JSON.stringify({
            current_user: current_user,
            })
    })
    .then(response => response.json())
    .then(result => {
                    //console.log(result.numero_of_likes)
                    spec_div.querySelector("#likes_value").innerHTML = result.numero_of_likes
            })

};

function handle_edit(elem) {
    //alert("Edit clicked")
    // Get the entire specific div
    const spec_div = elem.parentElement.parentElement;
    // Hide content_post
    spec_div.querySelector('#content_post').style.display = 'none';
    spec_div.querySelector('#edit_hide').style.display = 'none';

    // Get content_post from this entire specific div
    const content_post = spec_div.querySelector('#content_post').innerHTML;
    // Create elements
    const div_for_edit = document.createElement('div');
    const edit_textarea = document.createElement('textarea');
    const edit_buttons = document.createElement('div')
    const edit_save = document.createElement('button');
    const edit_cancel = document.createElement('button');
    // Fill textarea with content_post and name classes
    div_for_edit.className = 'div_for_edit_class';
    edit_buttons.className = 'edit_buttons_class';
    edit_textarea.className = 'edit_textarea_class';
    edit_textarea.value = content_post;
    edit_save.innerHTML = 'Save';
    edit_save.className = 'edit_save_class';
    edit_cancel.className = 'edit_cancel_class';
    edit_cancel.innerHTML = 'Cancel';

    edit_buttons.append(edit_save)
    edit_buttons.append(edit_cancel)

    div_for_edit.append(edit_textarea)
    div_for_edit.append(edit_buttons)

    // Added to the DOM
    spec_div.querySelector('#div_for_textarea').append(div_for_edit);

    spec_div.querySelector('.edit_save_class').addEventListener('click', () => {
        const edited_text = spec_div.querySelector('.edit_textarea_class').value;
        const post_id = spec_div.querySelector('#post_id').innerHTML
        
        // Check followers and following for the specific user -> first send data
        fetch('/post/' + post_id, {
            method: 'POST',
            body: JSON.stringify({
                edited_text: edited_text,
                })
        })
        .then(response => response.json())
        .then(result => {
                        //console.log(result.content_post)
                        spec_div.querySelector('.div_for_edit_class').remove() ;
                        spec_div.querySelector('#content_post').innerHTML = result.content_post;
                        spec_div.querySelector('#content_post').style.display = 'block';
                        spec_div.querySelector('#edit_hide').style.display = 'block';
                })
        //alert(post_id)
    });

    // it should be working now without reloading page
    spec_div.querySelector('.edit_cancel_class').addEventListener('click', () => {
        //alert("You want to cancel?")
        spec_div.querySelector('#content_post').style.display = 'block';
        spec_div.querySelector('#edit_hide').style.display = 'block';
        spec_div.querySelector('.div_for_edit_class').remove();
    });

    //alert(content_post)
    
};
