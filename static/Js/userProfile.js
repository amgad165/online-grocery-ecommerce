const sidebar = document.getElementById('sidebar');
const toggleSideBarExit=document.getElementById('toggle-sideBar');
const cartIcon = document.getElementById('cartIcon');
const profileDetailsContainer= document.getElementById('profile-details-container');

let userDetailsNameInput;
let newEmailInput;
let confirmNewEmailInput;
let passwordEmailUpdateInput;
let newPass;
let confirmNewPass;
let oldPass;
let userDetailsTel;
let userDetailsEmail;
console.log(toggleSideBarExit);
console.log(cartIcon);
console.log(sidebar);



//toggle and exit sidebar
toggleSideBarExit.addEventListener('click',()=>{
  sidebar.style.right='-1000px';

})
// sidebar in
cartIcon.addEventListener('click',()=>{
  sidebar.style.right='0';
 
})
// sidebar close when click outside
document.addEventListener('click', (event) => {
  const targetElement = event.target;
  if (!sidebar.contains(targetElement) && targetElement !== cartIcon) {
    sidebar.style.right = '-1000px';
  }
});

// function displayMyOrders(){
//     profileDetailsContainer.innerHTML=''
//     let markup = `<h2>Meine Bestellungen</h2>
                            
//     {% for order in orders %}

//    <h3>Order Date: </h3> <span>{{order.ordered_date}}</span>
//    <br>
//    <br>

//     <h3>Order details: </h3>

//     <ol>
//     {% for item in order.items.all  %}
//     <li>{{item}}</li>
//     {% endfor %}
//   </ol>


//     {% endfor %}`
  
//   profileDetailsContainer.innerHTML=markup
  
//   }


function displayMyOrders() {
  $.ajax({
      type: 'GET',
      url: '/get_orders/',
      success: function(response) {
          profileDetailsContainer.innerHTML = response.orders_html;
      },
      error: function(xhr, status, error) {
          console.error('Error fetching orders:', error);
      }
  });
}
  
function displayPersonalData() {
  profileDetailsContainer.innerHTML = '';

  $.ajax({
      type: 'GET',
      url: '/get_personal_info/',
      success: function(response) {
          profileDetailsContainer.innerHTML = response.personal_html;

          // Attach event listener to the Save changes button
          $('#saveChangesBtn').click(updateUserDetails);

            // $('#btn-email-update').click(updateEmail);

            // if email form submitted
          $('#edit-email-form').submit(function(event) {
            event.preventDefault(); // Prevent default form submission
        
            // Call the updateEmail function
            updateEmail();
        });

          // if change password form submitted
        $('#password-change-form').submit(function(event) {
          event.preventDefault(); // Prevent default form submission
      
          // Call the updateEmail function
          change_password();
      });
      },
      error: function(xhr, status, error) {
          console.error('Error fetching personal data:', error);
      }
  });
  

   userDetailsNameInput = document.getElementById('userDetailsName');
   newEmailInput = document.getElementById('newEmail');
   confirmNewEmailInput = document.getElementById('confirmNewEmail');
   passwordEmailUpdateInput = document.getElementById('confirmNewEmail');
   newPass = document.getElementById('newPass');
   confirmNewPass = document.getElementById('confirmNewPass');
   oldPass = document.getElementById('oldPass');
   userDetailsTel = document.getElementById('userDetailsTel');
   userDetailsEmail = document.getElementById('userDetailsEmail');
  
  
  
  }


  function updateUserDetails() {
    // Get the updated user details from the form inputs
    var userDetailsName = $('#userDetailsName').val();
    var userDetailsLastName = $('#userDetailsLastName').val();
    var userDetailsTel = $('#userDetailsTel').val();

    // Prepare the data to send in the AJAX request
    var userData = {
        name: userDetailsName,
        last_name: userDetailsLastName,
        tel: userDetailsTel
    };

    // Send an AJAX request to update the user details
    $.ajax({
        type: 'POST',
        url: '/get_personal_info/',
        data: userData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function(response) {
            // If the update is successful, display the updated user details
            if (response.success) {
                console.log('success')
                displayPersonalData();
            } else {
                // If there's an error, display an error message
                console.error('Error updating user details:', response.error);
                
            }
        },
        error: function(xhr, status, error) {
            console.error('Error updating user details:', error);
        }
    });
}



function updateEmail() {
  // Get the updated user details from the form inputs
  var email = $('#newEmail').val();
  var email_confirm = $('#confirmNewEmail').val();
  var password = $('#passwordEmailUpdate').val();

  // Prepare the data to send in the AJAX request
  var userData = {
      email: email,
      email_confirm: email_confirm,
      password: password
  };

  // Send an AJAX request to update the user details
  $.ajax({
      type: 'POST',
      url: '/update_email/',
      data: userData,
      headers: {
          'X-CSRFToken': getCookie('csrftoken')
      },
      success: function(response) {
          // If the update is successful, display the updated user details
          if (response.success) {
              console.log('success')
              displayPersonalData();
          } else {
              // If there's an error, display an error message
              console.error('Error updating email :', response.error);
              
          }
      },
      error: function(xhr, status, error) {
        var errorMessage = JSON.parse(xhr.responseText).error;
        console.log(errorMessage)
        var alertHtml = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            ${errorMessage}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    $('#alertContainer').html(alertHtml);



    }
  });
}



function change_password() {
  // Get the updated user details from the form inputs
  var password = $('#password').val();
  var newPass = $('#newPass').val();
  var confirmNewPass = $('#confirmNewPass').val();

  // Prepare the data to send in the AJAX request
  var userData = {
      password: password,
      newPass: newPass,
      confirmNewPass: confirmNewPass
  };

  // Send an AJAX request to update the user details
  $.ajax({
      type: 'POST',
      url: '/password_change/',
      data: userData,
      headers: {
          'X-CSRFToken': getCookie('csrftoken')
      },
      success: function(response) {
          // If the update is successful, display the updated user details
          if (response.success) {
              console.log('success')
              displayPersonalData();
          } else {
              // If there's an error, display an error message
              console.error('Error changing password :', response.error);
              
          }
      },
      error: function(xhr, status, error) {
        var errorMessage = JSON.parse(xhr.responseText).error;
        console.log(errorMessage)
        var alertHtml = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            ${errorMessage}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    $('#alertpasswords').html(alertHtml);



    }
  });
}


// Function to get the CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
  
  function displayadress(){
    profileDetailsContainer.innerHTML=''
  
    $.ajax({
      type: 'GET',
      url: '/get_address/',
      success: function(response) {
          profileDetailsContainer.innerHTML = response.address_html;

          
          $('#address-form').submit(function(event) {
            event.preventDefault(); // Prevent default form submission
        
            // Call the updateEmail function
            updateAddress();
        });
      },
      error: function(xhr, status, error) {
          console.error('Error fetching address:', error);
      }
  });
  
  
  }


  function updateAddress() {
    // Get the updated user details from the form inputs
    var bezirk = $('#bezirk-input').val();
    var street_address = $('#street_address-input').val();
    var hausnummer = $('#hausnummer-input').val();
    var plz_zip = $('#plz_zip-input').val();


    // Prepare the data to send in the AJAX request
    var userData = {
      bezirk: bezirk,
      street_address: street_address,
      hausnummer: hausnummer,
      plz_zip: plz_zip,
    };
  
    // Send an AJAX request to update the user details
    $.ajax({
        type: 'POST',
        url: '/address_change/',
        data: userData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function(response) {
            // If the update is successful, display the updated user details
            if (response.success) {
                console.log('success')
                displayadress();
            } else {
                // If there's an error, display an error message
                console.error('Error changing password :', response.error);
                
            }
        },
        error: function(xhr, status, error) {
          var errorMessage = JSON.parse(xhr.responseText).error;
          console.log(errorMessage)
  
  
      }
    });
  }



  // active class 
  let allBtns =Array.from(document.querySelectorAll('#profile-btns li '))
  console.log(allBtns)
  allBtns.forEach((btn)=>{
  btn.addEventListener('click',(e)=>{
    allBtns.forEach((btn)=>{
      btn.classList.remove('active')
      e.target.classList.add('active')
    })
  })
  })
  
  
  
  // validation for userDetails
  // modal 1
  function validateUserDetailsName(){
  //  console.log(userDetailsNameInput.value.length);
   if(userDetailsNameInput && userDetailsNameInput.value.length > 2){
    return true
  
  }
  return false
  }
  function validateUserDetailsEmail() {
    const emailPattern = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g;
    if (emailPattern.test(userDetailsEmail.value)) {
      console.log("Email is valid");
      return true;
    }
    console.log("Email is invalid");
    return false;
    
  }
  function validateUserDetailsTel() {
    const TelPattern = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/;
    console.log(userDetailsTel.value);
    if (TelPattern.test(userDetailsTel.value)) {
      console.log("tel is valid");
      return true;
    }
    console.log("tel is invalid");
    return false;
  }
  
  function validateAllUserDetailsInputs(){
  
    if(validateUserDetailsName() && validateUserDetailsEmail() &&  validateUserDetailsTel()){
      console.log("all is good");
      Swal.fire("Updated Done");
      hideModal('userDetails')
      return true
    }
    console.log("not good");
    return false
  }
  
  function hideModal(modalName) {
    const myModal = new bootstrap.Modal(`#${modalName}`)
  console.log(modalName);
    // Get the modal and backdrop elements
    const modalElement = document.getElementById(`${modalName}`);
    const backdropElement = document.querySelector('.modal-backdrop');
  
    // Hide the modal
    modalElement.classList.remove('show');
    modalElement.setAttribute('aria-hidden', 'true');
    modalElement.style.display = 'none';
  
    // Remove the backdrop
    if (backdropElement) {
      backdropElement.parentNode.removeChild(backdropElement);
    }
  }
  // validation for userDetails
  // modal 2 ( for update email)
  
  
  function validateUserDetailsEmailUpdate() {
    const emailPattern = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g;
    if (emailPattern.test(newEmailInput.value)) {
      console.log("Email is valid");
      return true;
    }
    console.log("Email is invalid");
    return false;
  }
  function confirmEmail(){
  if(newEmailInput.value =confirmNewEmailInput.value  ){
    console.log('email matched');
    return true
  }
  console.log('email not matched');
  return false
  }
   
  function validateToUpdateEmail(){
    if(validateUserDetailsEmailUpdate() && confirmEmail() && passwordEmailUpdateInput.value !='' ){
      console.log('email updated');
      hideModal('userEmail')
      Swal.fire("Email Updated");
  
      return true
    }
    return false
  }
  
  // validation for password reset
  // modal 3 ( for update password)
  
  function validateNewPassword(){
    const passwordPattern= /^.{8,}$/
    if(passwordPattern.test(newPass.value)){
      console.log('password accepted');
      return true
    }
    console.log('password not accepted');
    return false
  }
  
  function confirpasswordUpdated(){
    if(confirmNewPass.value =newPass.value  ){
      console.log('pass matched');
      return true
    }
    console.log('pass not matched');
    return false
    }
    function validateToChangePass(){
      if(validateNewPassword()&&confirpasswordUpdated() && oldPass.value!=''){
        console.log('password changed');
        Swal.fire("Password Changed");
        hideModal('userPass')
  
        return true
      }
      return false
    }



