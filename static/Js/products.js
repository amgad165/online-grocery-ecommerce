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



// Function to calculate total price
function calculateTotalPrice(modal) {
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

// Function to get the max quantity based on the selected radio button
function getMaxQuantity(modal) {
  var maxQuantity = Infinity; // Default to no limit
  var selectedRadio = modal.find('.size-radio:checked');
  if (selectedRadio.length) {
    maxQuantity = parseInt(selectedRadio.data('max-quantity')) || maxQuantity;
  }
  return maxQuantity;
}

// Function to calculate the total quantity of all ingredients
function getTotalQuantity(modal) {
  var totalQuantity = 0;
  modal.find('.quantity span').each(function() {
    totalQuantity += parseInt($(this).text().trim());
  });
  return totalQuantity;
}

// Event handlers scoped to the current modal
function attachEventHandlers(modal) {
  // Add click event listeners to each plus button
  modal.find('.plus.circled.plus-icon').on('click', function() {
    // Get the checkbox corresponding to this plus button
    var checkbox = $(this).closest('.row').find('.ingredient-checkbox');

    // Check if the checkbox is checked
    if (!checkbox.prop('checked')) {
      return; // Exit the function if the checkbox is not checked
    }

    // Increment quantity when plus button is clicked
    var quantityElement = $(this).siblings('.quantity').find('span');
    var quantity = parseInt(quantityElement.text().trim());
    var maxQuantity = getMaxQuantity(modal);
    var totalQuantity = getTotalQuantity(modal);

    // Increment the quantity if the total quantity is less than the max quantity
    if (totalQuantity < maxQuantity) {
      quantity += 1;
      quantityElement.text(quantity);
    }

    // Recalculate total price for this modal
    calculateTotalPrice(modal);
  });

  // Add click event listeners to each minus button
  modal.find('.minus.circled.minus-icon').on('click', function() {
    // Get the checkbox corresponding to this minus button
    var checkbox = $(this).closest('.row').find('.ingredient-checkbox');

    // Check if the checkbox is checked
    if (!checkbox.prop('checked')) {
      return; // Exit the function if the checkbox is not checked
    }

    // Decrement quantity when minus button is clicked
    var quantityElement = $(this).siblings('.quantity').find('span');
    var quantity = parseInt(quantityElement.text().trim());

    // Ensure quantity doesn't go below zero
    if (quantity > 0) {
      quantity -= 1;
      quantityElement.text(quantity);
    }

    // Recalculate total price for this modal
    calculateTotalPrice(modal);
  });

  // Add change event listener to each checkbox
  modal.find('.ingredient-checkbox').on('change', function() {
    // Get the corresponding plus and minus buttons within the same row
    var row = $(this).closest('.row');
    var plusButton = row.find('.plus-icon');
    var minusButton = row.find('.minus-icon');

    // Enable or disable the plus and minus buttons based on the checkbox's checked state
    if ($(this).prop('checked')) {
      plusButton.prop('disabled', false);
      minusButton.prop('disabled', false);

      // If quantity is 0, set it to 1, ensuring it doesn't exceed max quantity
      var quantityElement = row.find('.quantity span');
      var quantity = parseInt(quantityElement.text().trim());
      var maxQuantity = getMaxQuantity(modal);
      var totalQuantity = getTotalQuantity(modal);

      if (quantity === 0 && totalQuantity < maxQuantity) {
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
    calculateTotalPrice(modal);
  });

  // Add change event listener to size radio buttons
  modal.find('.size-radio').on('change', function() {
    // When radio button is changed, adjust the max quantity
    var maxQuantity = getMaxQuantity(modal);

    // Ensure the total quantity does not exceed the new max quantity
    var totalQuantity = getTotalQuantity(modal);
    if (totalQuantity > maxQuantity) {
      var excess = totalQuantity - maxQuantity;
      modal.find('.quantity span').each(function() {
        var quantityElement = $(this);
        var quantity = parseInt(quantityElement.text().trim());
        if (quantity > 0 && excess > 0) {
          var reduction = Math.min(quantity, excess);
          quantityElement.text(quantity - reduction);
          excess -= reduction;
        }
      });
    }

    // Recalculate total price for this modal
    calculateTotalPrice(modal);
  });
}

// Attach event handlers when the modal is shown
$('.product-details-modal').on('shown.bs.modal', function() {
  var modal = $(this);
  attachEventHandlers(modal);

  // Initial adjustment to enforce max quantity if needed
  var maxQuantity = getMaxQuantity(modal);
  var totalQuantity = getTotalQuantity(modal);
  if (totalQuantity > maxQuantity) {
    var excess = totalQuantity - maxQuantity;
    modal.find('.quantity span').each(function() {
      var quantityElement = $(this);
      var quantity = parseInt(quantityElement.text().trim());
      if (quantity > 0 && excess > 0) {
        var reduction = Math.min(quantity, excess);
        quantityElement.text(quantity - reduction);
        excess -= reduction;
      }
    });
  }

  // Recalculate total price for this modal
  calculateTotalPrice(modal);
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



