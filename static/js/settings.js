
$(document).ready(function() {
    // Function to handle the edit action
    function editEmail() {
        // Access the email input field
        const emailContainer = document.getElementById('emailContainer');
        
        // Make the email input field editable
        emailContainer.readOnly = false;

        // Remove the "readonly" attribute to allow editing
        emailContainer.removeAttribute('readonly');
        emailContainer.value = '';

        // Focus on the email input field for user convenience
        emailContainer.focus();
      
    }

    // Event listener for the edit button
    $('#editButton').on('click', function() {
        editEmail();
    });
});


const settingsText= document.querySelector('.settingTxt')
const settingsSpinner = document.querySelector('.fa-spinner')
const settingsMsg = document.querySelector('.notificationText')
const settingsmodal = document.querySelector('.notifymodal')

/*------------------------------------smanage resstingsn----------------------------------*/

$(document).on('submit', '#manageSettings', function(e){
    e.preventDefault();
    var formData = new FormData(this);
    settingsText.textContent = 'saving...';
    settingsSpinner.style.display="inline-block";
   
    
    $.ajax({
        type:'POST',
        url:'/accounts',
        processData: false,
        contentType: false,
        data:  formData,

success: function(data){
    if ('success' in data) {
        setTimeout(()=>{
            settingsSpinner.style.display="none"
            settingsText.innerHTML='Save'
            swal('Account Settings', data.success, 'success') 
            .then(() => {
                // Refresh the page after the OK button is clicked
                location.reload() // Refresh the page
            });
           
            
           
            
             // Show the modal after redirect
        }, 1200)

    } 
   
    else{
        setTimeout(()=>{
           
            settingsSpinner.style.display="none"
            settingsText.innerHTML='Save'
            swal('Account Settings', data.error, 'error') 
            .then(() => {
                // Refresh the page after the OK button is clicked
                location.reload() // Refresh the page
            });
           
           
            
             // Show the modal after redirect
        }, 1000)



    }
   

},
error:function(data){
    setTimeout(()=>{
  
         settingsSpinner.style.display="none"
         settingsText.innerHTML='Save'
         swal('Account Settings', data.error, 'error') 
            .then(() => {
                // Refresh the page after the OK button is clicked
                location.reload() // Refresh the page
            });
           
  
  
  
    }, 1000)
    

}

    });


})



// Get current date
var currentDate = new Date();

// Format the date in YYYY-MM-DD format
var year = currentDate.getFullYear();
var month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Add leading zero if needed
var day = String(currentDate.getDate()).padStart(2, '0'); // Add leading zero if needed
var formattedDate = year + "-" + month + "-" + day;

// Set the max attribute of the date input field to the current date
document.getElementById("dateofbirth").setAttribute("max", formattedDate);








