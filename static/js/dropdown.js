

document.addEventListener('DOMContentLoaded', function () {
    const dropdown = document.querySelector('.dropdown-onmouse');
    const dropdownContent = document.querySelector('.dropdown-content');

    // Toggle dropdown on button click
    dropdown.addEventListener('click', () => {
        // Toggle display property
        if (dropdownContent.style.display === 'block') {
            dropdownContent.style.display = 'none';
        } else {
            dropdownContent.style.display = 'block';
        }
       
    });

    // Close the dropdown if the user clicks outside of it

        dropdownContent.style.display = 'none';


 
});



$.ajax({
        type:'POST',
        url:'/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },


  success: function(data){
    if ('success' in data) {
        setTimeout(()=>{
            signbtntxt.textContent = 'Sign In '
            signinicon.style.display="none"
            window.location.replace(data.redirect)
        }, 4000)
    } else {
        setTimeout(()=>{
            signbtntxt.textContent = 'Sign In '
            signinicon.style.display="none"
            signinalert.innerHTML=data.error



        }, 4000)
        // Handle other responses or errors

    }


  },


  error:function(data){
    setTimeout(()=>{

        signbtntxt.textContent = 'Sign In '
        signinicon.style.display="none"
        signinalert.innerHTML='something went wrong'



    }, 4000)



  }




    });

 