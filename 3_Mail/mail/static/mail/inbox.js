document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email({recVal = '', subVal = '', bodyVal = ''} = {}) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recVal;
  document.querySelector('#compose-subject').value = subVal;
  document.querySelector('#compose-body').value = bodyVal;

  // Send POST request to API when form is submitted
  document.querySelector('#compose-form').onsubmit = async () => {
    // Get form data
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    // Post email data to API, wait for database to be updated
    try {
      await post_email(recipients, subject, body);
    } catch(e) {
      console.log(e);
    }

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
  document.querySelector('#single-email-view').style.display = 'none';

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
    // console.log(emails);

    // Container is template div
    const container = document.querySelector('#emails-view');

    // Check if emails array is empty or not
    if (Array.isArray(emails) && emails.length) {
      // Loop over items in mailbox and display them
      emails.forEach(email => {
        // Create bootstrap row
        const row = document.createElement('div');
        row.classList.add("row", "border", "email-box", "align-items-center", "popout");

        // If email is read, give it a grey background
        // Otherwise give it a white background
        if (email["read"]) {
          row.classList.add("bg-light");
        } else {
          row.classList.add("bg-white");
        }

        // Mark email as read and go to email view when row is clicked
        row.addEventListener('click', async () => {
          try {
            await mark_email(email["id"], {read: true});
          } catch(e) {
            console.log(e);
          }
          get_email(email["id"]);
        });
        // Add row to container div
        container.append(row);

        // Should display author, subject, timestamp
        const rowData = ["sender", "subject", "timestamp"];
        // Create object to give unique styling to each column
        const colClass = {
          "sender": ["col-md-3", "text-md-left"],
          "subject": ["col"],
          "timestamp": ["col-md-3", "text-md-right"]
        };

        // Create column for each email attribute
        rowData.forEach(colData => {
          // Create bootstrap column
          const col = document.createElement('div');
          // Add multiple classes using spread syntax
          col.classList.add(...colClass[colData]);
          // Add styling to text in different columns
          if (colData === "sender") {
            col.innerHTML = `<p class="font-weight-bold mb-0">${email[colData]}</p>`;
          } else if (colData === "timestamp") {
            col.innerHTML = `<p class="mb-0"><small class="text-secondary">${email[colData]}</small></p>`;
          } else {
            col.innerHTML = `<p class="mb-0">${email[colData]}</p>`;
          }
          // Add column to newly creeated row div
          row.append(col);
        });
      });
    } else {
      container.innerHTML = "Mailbox is empty";
    }
  });
}

function get_email(email_id) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  // Clear email view
  document.querySelector('#single-email-view').innerHTML = '';
  document.querySelector('#single-email-view').style.display = 'block';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    // console.log(email);

    // Container is template div
    const container = document.querySelector('#single-email-view');

    // Create bootstrap row
    const row = document.createElement('div');
    row.classList.add("row");
    container.append(row);

    // Create bootstrap column
    const col = document.createElement('div');
    col.classList.add("col-md-10");
    row.append(col);

    // Email attribute to display
    const emailData = ["sender", "recipients", "subject", "timestamp"];
    // Object for email tags
    const emailTags = {
      "sender": "From",
      "recipients": "To",
      "subject": "Subject",
      "timestamp": "Timestamp"
    };

    emailData.forEach(value => {
      // Create paragraph for each attribute
      const para = document.createElement("p");
      para.innerHTML = `<span class="font-weight-bold">${emailTags[value]}: </span>`;
      para.append(`${email[value]}`);
      col.append(para);
    });

    // Add reply button and functionality
    const replyBtn = document.createElement('button');
    replyBtn.innerHTML = "Reply";
    replyBtn.classList.add("btn", "btn-sm", "btn-outline-primary", "mr-1");
    // Pre-fill form in reply email
    const prefilledVals = {
      recVal: email["sender"],
      subVal: `Re: ${email["subject"]}`,
      bodyVal: `On ${email["timestamp"]} ${email["sender"]} wrote: \r\n> ${email["body"].replace(/\n/g, "\n> ")}\n\n`
    };
    replyBtn.addEventListener('click', () => compose_email(prefilledVals));
    container.append(replyBtn);

    // Add archive button and functionality
    const archiveBtn = document.createElement('button');
    archiveBtn.classList.add("btn", "btn-sm", "btn-outline-primary", "mr-1");
    // Allow user to unarchive email if email is archived
    const modification = {};
    if (email["archived"]) {
      archiveBtn.innerHTML = "Unarchive";
      modification.archived = false;
    } else {
      archiveBtn.innerHTML = "Archive";
      modification.archived = true;
    }
    archiveBtn.addEventListener('click', async () => {
      try {
        await mark_email(email_id, modification);
      } catch(e) {
        console.log(e);
      }
      // Redirect to inbox one email is archived
      load_mailbox('inbox');
    });
    container.append(archiveBtn);

    // Add unread button and functionality
    const unreadBtn = document.createElement('button');
    unreadBtn.classList.add("btn", "btn-sm", "btn-outline-primary");
    const modification2 = {};
    if (email["read"]) {
      unreadBtn.innerHTML = "Mark as unread";
      modification2.read = false;
    } else {
      unreadBtn.innerHTML = "Mark as read";
      modification2.read = true;
    }
    // Mark email as unread and redirect to inbox
    unreadBtn.addEventListener('click', async () => {
      try {
        await mark_email(email_id, modification2);
      } catch(e) {
        console.log(e);
      }
      // Reload page once email is unread
      get_email(email_id);
    });
    container.append(unreadBtn);

    // Add horizontal rule
    const hr = document.createElement('hr');
    container.append(hr);

    // Create second bootstrap row
    const row2 = document.createElement('div');
    row2.classList.add("row");
    container.append(row2);

    // Create second bootstrap column
    const col2 = document.createElement('div');
    col2.classList.add("col-md-10");
    row2.append(col2);
    const para2 = document.createElement("p");
    // Preserve white space in email body text
    para2.style.whiteSpace = "pre-line";
    para2.append(`${email["body"]}`);
    col2.append(para2);
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
    // console.log(result);
  });
}

function mark_email(email_id, modification) {

  // Send put request to email view
  return fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify(modification)
  });
}