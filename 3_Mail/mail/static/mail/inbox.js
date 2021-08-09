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

    // Create boostrap container and add it to template div
    const container = document.createElement('div');
    container.classList.add("container");
    const emailDiv = document.querySelector('#emails-view');
    emailDiv.append(container);
    const containerDiv = emailDiv.querySelector('.container');

    // Check if emails array is empty or not
    if (Array.isArray(emails) && emails.length) {
      // Loop over items in mailbox and display them
      emails.forEach(email => {
        // Create bootstrap row
        const row = document.createElement('div');
        row.classList.add("row", "border", "email-box", "align-items-center");
        // If email is read, give it a grey background
        // Otherwise give it a white background
        if (email["read"]) {
          row.classList.add("bg-light");
        } else {
          row.classList.add("bg-white");
        }
        // Toggle action when row is clicked
        row.addEventListener('click', function() {
          console.log('This element has been clicked!')
        });
        // Add row to container div
        containerDiv.append(row);
        // Should display author, subject, timestamp
        rowData = ["sender", "subject", "timestamp"];
        // Create object to give unique styling to each column
        colClass = {
          "sender": "col-md-3",
          "subject": "col",
          "timestamp": ["col-md-3", "text-md-right"]
        };
        // Create column for each email attribute
        rowData.forEach(colData => {
          // Create bootstrap column
          const col = document.createElement('div');
          col.classList.add(colClass[colData]);
          // Give timestamp smaller text
          if (colData === "timestamp") {
            col.innerHTML = `<small class="text-secondary">${email[colData]}</small>`;
          } else {
            col.innerHTML = email[colData];
          }
          // Add column to newly creeated row div
          row.append(col);
        });
      });
    } else {
      containerDiv.innerHTML = "Mailbox is empty";
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