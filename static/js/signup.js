
  ;
  const openModalBtn2 = document.querySelectorAll(".openModal2");

  const modal = document.querySelector('.signupmodal');
  const closeModalBtn = document.querySelector("#signupclose");
  const signinmodal= document.querySelector(".signinmodal");
 const signInModal = document.querySelectorAll(".openModal");
 const signincloseModalBtn = document.querySelector("#signinclose");









openModalBtn2.forEach((openModalBtn, index) => {
    openModalBtn.addEventListener('click',  function() {
           modal.style.display = "block"

    })

  closeModalBtn.addEventListener("click", function () {
    modal.style.display = "none";

});

})


/*-----------------------------------for signin------------------------------*/
signInModal.forEach((signInModal, index) => {
  signInModal.addEventListener('click',  function() {
         signinmodal.style.display = "block"

  })
  signincloseModalBtn.addEventListener("click", function () {
    signinmodal.style.display = "none";

});

})


const icon = document.querySelector('.fa-spinner')

 const btn = document.querySelector('.signupbtn-txt')

 // prevent a space bar for username
document.getElementById('username').addEventListener('keypress', function(e) {
    if (e.key === ' ') {
        e.preventDefault();  // Prevents the space character from being input
    }
  });

$(document).on('submit', '#signupform', function(e){
    e.preventDefault();
    var formData = new FormData(this);
    btn.innerHTML = ' '
    icon.style.display="block"

    $.ajax({
        type:'POST',
        url:'/signup',
        processData: false,
        contentType: false,
        data:  formData,

        success: function(data){
            if ('success' in data) {
                setTimeout(()=>{
                   icon.style.display="None"
                   btn.innerHTML = "SignUp"

                    swal('Account Created', data.success, 'success')
                    .then(() => {
                        // Refresh the page after the OK button is clicked
                        location.replace('/accounts'); // Refresh the page
                    });





                     // Show the modal after redirect
                }, 1200)


            }

            else{
                setTimeout(()=>{

                    icon.style.display="none"
                    btn.innerHTML='SignUp'
                    swal('Account Created', data.error, 'error')



                     // Show the modal after redirect
                }, 1000)



            }


        },
        error:function(data){
            setTimeout(()=>{

                icon.style.display="none"
                btn.innerHTML='SignUp'
                swal('Error', data.error, "error")




            },1000)


        }

            });


        })




function togglePasswordVisibility() {
    var password1 = document.getElementById("password1");
    var password2 = document.getElementById("password2");
    var showPasswordCheckbox = document.getElementById("showPassword");

    if (showPasswordCheckbox.checked) {
        password1.type = "text";  // Show password1
        password2.type = "text";  // Show password2
    } else {
        password1.type = "password";  // Hide password1
        password2.type = "password";  // Hide password2
    }
}

// Function to toggle password visibility
function togglePasswordVisibilitySignin() {
    var password1 = document.getElementById("spassword"); // Ensure the ID matches
    var showPasswordCheckbox = document.getElementById("showSignInPassword");

    if (showPasswordCheckbox.checked) {
        password1.type = "text"; // Show the password
    } else {
        password1.type = "password"; // Hide the password
    }
}