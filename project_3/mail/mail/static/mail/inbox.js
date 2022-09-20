document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';


  // Send email after submitting and be redirected to Send tab
  document.querySelector('form').onsubmit = function() {
    // Get values from the fields
    const recipient_value = document.querySelector('#compose-recipients').value;
    const subject_value = document.querySelector('#compose-subject').value;
    const body_value = document.querySelector('#compose-body').value;

    // Send email
    fetch('/emails', {
              method: 'POST',
              body: JSON.stringify({
                  recipients: recipient_value,
                  subject: subject_value,
                  body: body_value,
                  })
        })
    .then(response => response.json())
    .then(result => {
                    if (result.error) {
                      //console.log(result.error)
                      alert(result.error)
                    }
                    else {
                      //console.log(result)
                      load_mailbox('sent');
                    }
            })
    // in order to stay at the same page if error occurs    
    return false;
    }
  };

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Clear values
  document.querySelector('#from_value').innerHTML = '';
  document.querySelector('#to_value').innerHTML = '';
  document.querySelector('#subject_value').innerHTML = '';
  document.querySelector('#timestamp_value').innerHTML = '';
  document.querySelector('#body_value').innerHTML = '';

  if (mailbox === 'sent') {
   
        fetch('/emails/' + mailbox)
        .then(response => response.json())
        .then(emails => {
            if (emails.length == 0) {
              document.querySelector('#emails-view').append("No Sent Emails.")
            }
            // Print emails
            //console.log(emails);
              emails.forEach( (email) => {
                  //console.log(email);
                  // Create new div and fill it with sent email
                  const sent_mail = document.createElement('div');
                  sent_mail.className = 'sent_mail_div';
                  sent_mail.innerHTML = `<b>${email.recipients} &nbsp;&nbsp;&nbsp;</b>  <strong id="email-subject-strong-in-div">${email.subject}</strong> <i id="float-right-in-div">${email.timestamp}</i>`;

                  // Add email to DOM
                  document.querySelector('#emails-view').append(sent_mail);

                  sent_mail.addEventListener('click', function() {
                    //console.log('click')
                    // Go to view the email
                    view_email(email, mailbox)
                 });
            })
        });
    };

    if (mailbox === 'inbox') {

      fetch('/emails/' + mailbox)
        .then(response => response.json())
        .then(emails => {
              if (emails.length == 0) { 
                document.querySelector('#emails-view').append("No Emails in Inbox.")
              }
              emails.forEach( (email) => {       
                  // Create new div and fill it with sent email
                  const sent_mail = document.createElement('div');
                  sent_mail.className = 'sent_mail_div';
                  if (email.read === true) {
                    sent_mail.style.backgroundColor = 'LightGray ';
                  }
                  sent_mail.innerHTML = `<b>${email.sender} &nbsp;&nbsp;&nbsp;</b>  <strong id="email-subject-strong-in-div">${email.subject}</strong> <i id="float-right-in-div">${email.timestamp}</i>`;
                  
                  // Add email to DOM
                  document.querySelector('#emails-view').append(sent_mail);
                  
                  sent_mail.addEventListener('click', function() {
                      //console.log('click')

                      // Go to view the email
                      view_email(email, mailbox)
                      
                      // marked email as read
                      fetch('/emails/'+ email.id, {
                        method: 'PUT',
                        body: JSON.stringify({
                            read: true
                        })
                      })
                });
            })
        });
    };

    if (mailbox === 'archive') {
      fetch('/emails/' + mailbox)
        .then(response => response.json())
        .then(emails => {
          //console.log(emails)
              if (emails.length == 0) {
                document.querySelector('#emails-view').append("No Archived Emails.")
              }
              emails.forEach( (email) => {
                  //console.log(email)
                  // Create new div and fill it with sent email
                  const sent_mail = document.createElement('div');
                  sent_mail.className = 'sent_mail_div';
                  sent_mail.innerHTML = `<b>${email.sender} &nbsp;&nbsp;&nbsp;</b>  <strong id="email-subject-strong-in-div">${email.subject}</strong> <i id="float-right-in-div">${email.timestamp}</i>`;
        
                  // Add email to DOM
                  document.querySelector('#emails-view').append(sent_mail);

                  sent_mail.addEventListener('click', function() {
                    //console.log('click')

                    // Go to view the email
                    view_email(email, mailbox)                   
                  });
               })
        });
    };
  }


function view_email(email, mailbox) {
  // Show view email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'block';

  fetch('/emails/' + email.id)
  .then(response => response.json())
  .then(email => {
      // Print email
      //console.log(email);
      // Create new divs and fill it with different names
      const email_sender = document.createElement('div');
      const email_recipient = document.createElement('div');
      const email_subject = document.createElement('div');
      const email_timestamp = document.createElement('div');
      const email_body = document.createElement('div');
      email_sender.className = 'email_sender_div';
      email_recipient.className = 'email_recipient_div';
      email_subject.className = 'email_subject_div';
      email_timestamp.className = 'email_timestamp_div';
      email_body.className = 'email_body_div';

      email_sender.innerHTML = email.sender
      email_recipient.innerHTML = email.recipients
      email_subject.innerHTML = email.subject
      email_timestamp.innerHTML = email.timestamp
      email_body.innerHTML = email.body
      // Add info to DOM
      document.querySelector('#from_value').append(email_sender);
      document.querySelector('#to_value').append(email_recipient);
      document.querySelector('#subject_value').append(email_subject);
      document.querySelector('#timestamp_value').append(email_timestamp);
      document.querySelector('#body_value').append(email_body); 
    });

  if (mailbox === 'sent') {
    document.querySelector('#archived_div_parent').style.display = 'none';
    document.querySelector('#reply_div_parent').style.display = 'none';
  }
  else { // 'inbox' and 'archive'
    document.querySelector('#archived_div').innerHTML = '';
    document.querySelector('#archived_div_parent').style.display = 'block';

    const archive_button = document.createElement('button');
    if (mailbox === 'inbox') {
      document.querySelector('#reply_div_parent').style.display = 'block';
      document.querySelector('#reply_div').innerHTML = '';


      archive_button.innerHTML = 'Archive';
      archive_button.addEventListener('click', function() {
          //console.log('click')
          fetch('/emails/'+ email.id, {
            method: 'PUT',
            body: JSON.stringify({
                archived: true
                })
            })
          archive_button.remove();
          document.querySelector('#view-email').style.display = 'none';
          //load_mailbox(mailbox)
          document.location.reload ()
        });
      // Reply button
      const reply_button = document.createElement('button');
      reply_button.innerHTML = 'Reply';
      reply_button.addEventListener('click', function() {
        //console.log('click');
        reply_button.remove();
        document.querySelector('#view-email').style.display = 'none';
        compose_email()

        // Pre-fill the fields
        document.querySelector('#compose-recipients').value = email.sender;
        if (email.subject.startsWith('Re: ')) {
          document.querySelector('#compose-subject').value = email.subject;
        }
        else {
          document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
        }
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body} \n`;
      })
      document.querySelector('#reply_div').append(reply_button);
    }
    else  // mailbox === 'archive'
    {
      document.querySelector('#reply_div_parent').style.display = 'none';

      archive_button.innerHTML = 'Unarchive';
      archive_button.addEventListener('click', function() {
        //console.log('click')
        fetch('/emails/'+ email.id, {
          method: 'PUT',
          body: JSON.stringify({
              archived: false
          })
        })
        archive_button.remove();
        //document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#view-email').style.display = 'none';
        //load_mailbox(mailbox)
        document.location.reload ()
      });
    }
    document.querySelector('#archived_div').append(archive_button);
  }
}