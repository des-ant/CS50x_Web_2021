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

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Send POST request to API when form is submitted
  document.querySelector('#compose-form').onsubmit = async () => {
    // Get form data
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    // Post email data to API, wait for database to be updated
    await post_email(recipients, subject, body)

    // Load user's sent mailbox
    load_mailbox('sent');

    // Stop form from submitting and redirecting page
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Get mailbox info from API
  get_mailbox(mailbox)
  
}

function get_mailbox(mailbox) {

  // Make web request to inbox API
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
    // Check if emails array is empty or not
    if (Array.isArray(emails) && emails.length) {
      // Loop over items in mailbox and display them
      emails.forEach(email => {
        const element = document.createElement('div');
        element.innerHTML = email["id"] + " " + email["body"];
        element.addEventListener('click', function() {
          console.log('This element has been clicked!')
        });
        // Add email to template
        document.querySelector('#emails-view').append(element);
      });
    } else {
      const element = document.createElement('div');
      element.innerHTML = "Mailbox is empty";
      // Add div to template
      document.querySelector('#emails-view').append(element);
    }
  });
}

function get_email(email_id) {

  return fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);

    // ... do something else with email ...
  });
}

function post_email(recipients, subject, body) {

  // Return promise after posting to API
  return fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
  });
}

function mark_email(email_id, modification) {

  return fetch(`/email/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify(modification)
  });
}