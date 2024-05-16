const sidebar = document.getElementById('sidebar');
const toggleSideBarExit=document.getElementById('toggle-sideBar');
const cartIcon = document.getElementById('cartIcon');
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

  // Get all the quantity elements 
  var quantityElements = document.querySelectorAll('.quantity');

  // Get all the plus and minus buttons
  var plusButtons = document.querySelectorAll('.plus');
  var minusButtons = document.querySelectorAll('.minus');

  // // Set the initial quantities
  // var quantities = Array.from(quantityElements).map(function(element) {
  //   return 1;
  // });

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



  // // Function to calculate total price
  // function calculateTotalPrice() {
   
  //     let totalPrice = 0;
      
  //     // Loop through each ingredient
  //     $('.row.m-0.p-0').each(function() {
        
  //         // Get quantity and price of the ingredient
  //         const quantity = parseInt($(this).find('.quantity').text().trim());
  //         const price = parseFloat($(this).find('.ingredient-price').val());
          
  //         // Calculate subtotal for this ingredient and add to total price
  //         const subtotal = quantity * price;
  //         console.log(subtotal)
  //         totalPrice += subtotal;
  //     });
  //     // Display total price
  //     $('#total-price').text(totalPrice.toFixed(2)+'€'); 
  // }
  

//   //modal update quantity
  
// // Get all the plus and minus buttons
// var plusButtons = document.querySelectorAll('.plus-icon');
// var minusButtons = document.querySelectorAll('.minus-icon');

// // // calculate the total price initially
// // calculateTotalPrice();


// // Add click event listeners to each plus button
// plusButtons.forEach(function(button) {
//   button.addEventListener('click', function() {
//     // Get the quantity element of the current row
//     var quantityElement = button.parentNode.querySelector('.quantity span');
//     // Get the current quantity value
//     var quantity = parseInt(quantityElement.textContent);
//     // Increment the quantity valuez
//     quantity += 1;
//     // Update the quantity element
//     quantityElement.textContent = quantity;
//     calculateTotalPrice()
//   });
// });

// // Add click event listeners to each minus button
// minusButtons.forEach(function(button) {
//   button.addEventListener('click', function() {
//     // Get the quantity element of the current row
//     var quantityElement = button.parentNode.querySelector('.quantity span');
//     // Get the current quantity value
//     var quantity = parseInt(quantityElement.textContent);
//     // Decrement the quantity value (if greater than 0)
//     if (quantity > 0) {
//       quantity -= 1;
//     }
//     // Update the quantity element
//     quantityElement.textContent = quantity;
//     calculateTotalPrice()
//   });
// });




// Function to calculate total price
function calculateTotalPrice() {
  // Find the modal container
  var modal = $('.product-details-modal.show');
 
  // Initialize total price for this modal
  var totalPrice = 0;
  
  // Loop through each ingredient within the modal
  modal.find('.row.m-0.p-0').each(function() {
      // Get quantity and price of the ingredient
      var quantity = parseInt($(this).find('.quantity span').text().trim());
      var price = parseFloat($(this).find('.ingredient-price').val());
      
      // Calculate subtotal for this ingredient and add to total price
      var subtotal = quantity * price;
      totalPrice += subtotal;
  });
  
  // Display total price within the modal
  modal.find('#total-price').text(totalPrice.toFixed(2) + '€');
}

// Add click event listeners to each plus button
$('.plus.circled.plus-icon').on('click', function() {
  // Get the checkbox corresponding to this plus button
  var checkbox = $(this).closest('.row').find('.ingredient-checkbox');
  
  // Check if the checkbox is checked
  if (!checkbox.prop('checked')) {
    return; // Exit the function if the checkbox is not checked
  }
  
  // Get the modal container
  var modal = $(this).closest('.modal');
  
  // Increment quantity when plus button is clicked
  var quantityElement = $(this).siblings('.quantity').find('span');
  var quantity = parseInt(quantityElement.text().trim());
  quantity += 1;
  quantityElement.text(quantity);
  
  // Recalculate total price for this modal
  calculateTotalPrice();
});

// Add click event listeners to each minus button
$('.minus.circled.minus-icon').on('click', function() {
  // Get the checkbox corresponding to this minus button
  var checkbox = $(this).closest('.row').find('.ingredient-checkbox');
  
  // Check if the checkbox is checked
  if (!checkbox.prop('checked')) {
    return; // Exit the function if the checkbox is not checked
  }
  
  // Get the modal container
  var modal = $(this).closest('.modal');
  
  // Decrement quantity when minus button is clicked
  var quantityElement = $(this).siblings('.quantity').find('span');
  var quantity = parseInt(quantityElement.text().trim());
  quantity -= 1;
  // Ensure quantity doesn't go below zero
  if (quantity < 0) {
    quantity = 0;
  }
  quantityElement.text(quantity);
  
  // Recalculate total price for this modal
  calculateTotalPrice();
});


// Add change event listener to each checkbox
$('.ingredient-checkbox').on('change', function() {
  // Get the corresponding plus and minus buttons within the same row
  var row = $(this).closest('.row');
  var plusButton = row.find('.plus-icon');
  var minusButton = row.find('.minus-icon');
  
  // Enable or disable the plus and minus buttons based on the checkbox's checked state
  if ($(this).prop('checked')) {
      plusButton.prop('disabled', false);
      minusButton.prop('disabled', false);
      
      // If quantity is 0, set it to 1
      var quantityElement = row.find('.quantity span');
      var quantity = parseInt(quantityElement.text().trim());
      if (quantity === 0) {
          quantityElement.text('1');
      }
  } else {
      plusButton.prop('disabled', true);
      minusButton.prop('disabled', true);
      
      // Set quantity to 0
      var quantityElement = row.find('.quantity span');
      quantityElement.text('0');
  }
    // Recalculate total price for this modal
    calculateTotalPrice();
});

// Check if the quantity is greater than zero and set the checkbox as checked
$('.quantity span').each(function() {
  var quantity = parseInt($(this).text().trim());
  if (quantity > 0) {
    $(this).closest('.row').find('.ingredient-checkbox').prop('checked', true);
  }


  
});

// Get all the "Entfernen" buttons
var removeButtons = document.querySelectorAll('.remove-btn button');

// Add click event listener to each button
removeButtons.forEach(function(button) {
  button.addEventListener('click', function(event) {
    // Stop event propagation
    event.stopPropagation();

    // Get the parent row element
    var row = this.closest('.row-item');

    // Add animation class to fade out the row
    row.classList.add('animate__animated');
    row.classList.add('animate__fadeOut');

    // Remove the row from the DOM after the animation ends
    row.addEventListener('animationend', function() {
      row.parentNode.removeChild(row);
    });
  });
});



