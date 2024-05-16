const firmRegBtn = document.getElementById('firmReg');
const privateReg = document.getElementById('privateReg');
const inputsPriv = document.getElementById("inputs-priv")
const inputsFirm = document.getElementById("inputs-firm")
const registerModal = document.getElementById("registerModal")
const loginModal = document.getElementById('loginModal')
const sidebar = document.getElementById('sidebar');
const toggleSideBarExit=document.getElementById('toggle-sideBar');
const cartIcon = document.getElementById('cartIcon');
const profileDetailsContainer= document.getElementById('profile-details-container');



// validation signup firm
const vornameFirmInput= document.querySelector('#inputs-firm #vornameFirm');
const nachnameFirmInput= document.querySelector('#inputs-firm #nachnameFirm');
const firmNameInput= document.querySelector('#inputs-firm #firmNameFirm');
const atuFirmInput= document.querySelector('#inputs-firm #atuFirm');
const emailFirmInput= document.querySelector('#inputs-firm #emailFirm');
const addressFirmInput= document.querySelector('#inputs-firm #addressFirm');

const bezirkFirmInput= document.querySelector('#inputs-firm #bezirkFirm');
const street_addressFirmInput= document.querySelector('#inputs-firm #street_addressFirm');
const hausnummerFirmInput= document.querySelector('#inputs-firm #hausnummerFirm');
const plz_zipFirmInput= document.querySelector('#inputs-firm #plz_zipFirm');






const passFirmInput= document.querySelector('#inputs-firm #passFirm');
const confpassFirmInput= document.querySelector('#inputs-firm #confirmPasswordFirm');

// errors displayed
const vornameFirmError = document.getElementById('vornameFirmError');
const nachnameFirm = document.getElementById('nachnameFirmError');
const firmNameError = document.getElementById('firmNameError');
const atuFirmError = document.getElementById('atuFirmError');
const emailFirmError = document.getElementById('emailFirmError');
const passFirmError = document.getElementById('passFirmError');


// validation signup priv
const vornamePrivInput= document.querySelector('#inputs-priv #vornamePriv');
const nachnamePrivInput= document.querySelector('#inputs-priv #nachnamePriv');
const emailPrivInput= document.querySelector('#inputs-priv #emailPriv');

const bezirkPrivInput= document.querySelector('#inputs-priv #bezirkPriv');
const street_addressPrivInput= document.querySelector('#inputs-priv #street_addressPriv');
const hausnummerPrivInput= document.querySelector('#inputs-priv #hausnummerPriv');
const plz_zipPrivInput= document.querySelector('#inputs-priv #plz_zipPriv');


const passPrivInput= document.querySelector('#inputs-priv #passwordPriv');
const confpassPrivInput= document.querySelector('#inputs-priv #confirmPasswordFirm');

// errors displayed
const vornamePrivError = document.getElementById('vornameErrorPriv');
const nachnamePrivError  = document.getElementById('nachnameErrorPriv');
const firmNamePrivError = document.getElementById('FirmNameErrorPriv');
const atuPrivError = document.getElementById('atuErrorPriv');
const emailPrivError = document.getElementById('emailErrorPriv');
const passPrivError = document.getElementById('passwordErrorPriv');


let userDetailsNameInput;
let newEmailInput;
let confirmNewEmailInput;
let passwordEmailUpdateInput;
let newPass;
let confirmNewPass;
let oldPass;
let userDetailsTel;
let userDetailsEmail;




function filterInputsAccordingToRole(button) {
  var roleInput = document.getElementById('role');
  if(button.innerHTML.trim() =='Privat'){
    console.log('Privat');
    firmRegBtn.classList.remove('activeRegsiterBtn');
    inputsFirm.classList.add('d-none')
    inputsPriv.classList.remove('d-none')

    // Enable inputs in inputs-priv and disable inputs in inputs-firm
    enableInputs(inputsPriv);
    disableInputs(inputsFirm);
    
    // add required to inputs
    vornamePrivInput.setAttribute("required", "");
    nachnamePrivInput.setAttribute("required", "");
    emailPrivInput.setAttribute("required", "");

    bezirkPrivInput.setAttribute("required", "");
    street_addressPrivInput.setAttribute("required", "");
    hausnummerPrivInput.setAttribute("required", "");
    plz_zipPrivInput.setAttribute("required", "");

    passPrivInput.setAttribute("required", "");

    // remove required from inputs
    vornameFirmInput.removeAttribute('required');
    nachnameFirmInput.removeAttribute('required');
    firmNameInput.removeAttribute('required');
    atuFirmInput.removeAttribute('required');
    emailFirmInput.removeAttribute('required');

    bezirkFirmInput.removeAttribute('required');
    street_addressFirmInput.removeAttribute('required');
    hausnummerFirmInput.removeAttribute('required');
    plz_zipFirmInput.removeAttribute('required');




    passFirmInput.removeAttribute('required');
    confpassFirmInput.removeAttribute('required');

    roleInput.value = 'private';
    
  }else{
    console.log('firm');
    privateReg.classList.remove('activeRegsiterBtn');
    inputsFirm.classList.remove('d-none')
    inputsPriv.classList.add('d-none')
      // Enable inputs in inputs-firm and disable inputs in inputs-priv
      enableInputs(inputsFirm);
      disableInputs(inputsPriv);

    // add required to inputs
    vornameFirmInput.setAttribute("required", "");
    nachnameFirmInput.setAttribute("required", "");
    firmNameInput.setAttribute("required", "");
    atuFirmInput.setAttribute("required", "");
    emailFirmInput.setAttribute("required", "");

    bezirkFirmInput.setAttribute("required", "");
    street_addressFirmInput.setAttribute("required", "");
    hausnummerFirmInput.setAttribute("required", "");
    plz_zipFirmInput.setAttribute("required", "");


    passFirmInput.setAttribute("required", "");
    confpassFirmInput.setAttribute("required", "");


    // remove required from inputs firm
    vornamePrivInput.removeAttribute('required');
    nachnamePrivInput.removeAttribute('required');

    bezirkPrivInput.removeAttribute('required');
    street_addressPrivInput.removeAttribute('required');
    hausnummerPrivInput.removeAttribute('required');
    plz_zipPrivInput.removeAttribute('required');

    emailPrivInput.removeAttribute('required');
    passPrivInput.removeAttribute('required');

    roleInput.value = 'company';
  
  }
button.classList.add('activeRegsiterBtn')
}

function enableInputs(container) {
  var inputs = container.querySelectorAll('input, select, textarea');
  inputs.forEach(function(input) {
      input.removeAttribute('disabled');
  });
}

function disableInputs(container) {
  var inputs = container.querySelectorAll('input, select, textarea');
  inputs.forEach(function(input) {
      input.setAttribute('disabled', 'disabled');
  });
}


function displayLogin() {
  registerModal.classList.add('d-none')
  loginModal.classList.replace('d-none', 'd-block')
}
function backToRegister() {
  registerModal.classList.remove('d-none')
  loginModal.classList.add('d-none')

  loginModal.classList.replace('d-block', 'd-none')
}

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





vornameFirmInput.addEventListener('input',validateVorNameFirmForm)
function validateVorNameFirmForm(){
  // +vornameFirmInput.value.length
  console.log(+vornameFirmInput.value.length);
  if(vornameFirmInput.value == '' || +vornameFirmInput.value.length  < 3 ){
    vornameFirmError.innerText='at least 3 chars'
  }else{
    vornameFirmError.innerText=''
    
  }
  
}
nachnameFirmInput.addEventListener('input',validateNachNameFirmForm)
function validateNachNameFirmForm(){
  if(nachnameFirmInput.value == '' || +nachnameFirmInput.value.length  < 3 ){
    nachnameFirm.innerText='at least 3 chars'
  }else{
    nachnameFirm.innerText=''
    
  }
  
}


firmNameInput.addEventListener('input',validateFirmNameFirmForm)
function validateFirmNameFirmForm(){
  if(firmNameInput.value == '' ){
    firmNameError.innerText='firm name is required'
  }else{
    firmNameError.innerText=''
    
  }
  
}
atuFirmInput.addEventListener('input',validateAtuFirmForm)
function validateAtuFirmForm(){
  if(atuFirmInput.value == ''  ||  +atuFirmInput.value.length >9 ){
    atuFirmError.innerText='atu is not valid'
  }else{
    atuFirmError.innerText=''
    
  }
  
}

emailFirmInput.addEventListener('input',validateEmailFirmForm)
function validateEmailFirmForm(){
  const emailPattern =/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/
  if(emailPattern.test(emailFirmInput.value) ){
    emailFirmError.innerText=''
  }else{
    emailFirmError.innerText='email is not valid'
    
  }
  
}
passFirmInput.addEventListener('input',validatePassFirmForm)
function validatePassFirmForm(){
  const passPattern =/^.{8,}$/
  if(passPattern.test(passFirmInput.value) ){
    passFirmError.innerText=''
  }else{
    passFirmError.innerText='at least 8 chats tall'
    
  }
  
}




vornamePrivInput.addEventListener('input',validateVorNamePrivForm)
function validateVorNamePrivForm(){
  console.log(+vornameFirmInput.value.length);
  if(vornamePrivInput.value == '' || +vornamePrivInput.value.length  < 3 ){
    vornamePrivError.innerText='at least 3 chars'
  }else{
    vornamePrivError.innerText=''
    
  }
  
}
nachnamePrivInput.addEventListener('input',validateNachNamePrivForm)
function validateNachNamePrivForm(){
  if(nachnamePrivInput.value == '' || +nachnamePrivInput.value.length  < 3 ){
    nachnamePrivError.innerText='at least 3 chars'
  }else{
    nachnamePrivError.innerText=''
    
  }
  
}


firmNameInputPriv.addEventListener('input',validateFirmNamePrivForm)
function validateFirmNamePrivForm(){
  if(firmNameInputPriv.value == '' ){
    firmNamePrivError.innerText='firm name is required'
  }else{
    firmNamePrivError.innerText='' 
  }
  
}

atuPrivInput.addEventListener('input',validateAtuPrivForm)
function validateAtuPrivForm(){
  if(atuPrivInput.value == ''  ||  +atuPrivInput.value.length >9 ){
    atuPrivError.innerText='atu is not valid'
  }else{
    atuPrivError.innerText=''
    
  }
  
}

emailPrivInput.addEventListener('input',validateEmailPrivForm)
function validateEmailPrivForm(){
  const emailPattern =/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/
  if(emailPattern.test(emailPrivInput.value) ){
    emailPrivError.innerText=''
  }else{
    emailPrivError.innerText='email is not valid'
    
  }
  
}
passPrivInput.addEventListener('input',validatePassPrivForm)
function validatePassPrivForm(){
  const passPattern =/^.{8,}$/
  if(passPattern.test(passPrivInput.value) ){
    passPrivError.innerText=''
  }else{
    passPrivError.innerText='at least 8 chats tall'
    
  }
  
}








//update cart

  // Get all the quantity elements
  var quantityElements = document.querySelectorAll('.quantity');

  // Get all the plus and minus buttons
  var plusButtons = document.querySelectorAll('.plus');
  var minusButtons = document.querySelectorAll('.minus');

  // Set the initial quantities
  var quantities = Array.from(quantityElements).map(function(element) {
    return 1;
  });

  // // Function to update the quantity elements
  // function updateQuantities() {
  //   quantityElements.forEach(function(element, index) {
  //     element.textContent = quantities[index];
  //   });
  // }

  // // Event listeners for the plus buttons
  // plusButtons.forEach(function(button, index) {
  //   button.addEventListener('click', function() {
  //     quantities[index]++;
  //     updateQuantities();
  //   });
  // });

  // // Event listeners for the minus buttons
  // minusButtons.forEach(function(button, index) {
  //   button.addEventListener('click', function() {
  //     if (quantities[index] > 1) {
  //       quantities[index]--;
  //       updateQuantities();
  //     }
  //   });
  // });

  // // Initial update of the quantity elements
  // updateQuantities();





  