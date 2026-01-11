
  const closeModalBtn = document.getElementsByClassName("close-notification")[0];
  const resendverif = document.getElementsByClassName("resend-verification")[0];
   const btn = document.querySelector('.pop-btn-txt')
   var notificationText = document.querySelector('.notificationText')
  

  
$(document).on('submit', '#resend-verification-link-form', function(e){
  e.preventDefault();
   btn.textContent = ' '
    icon.style.display="block"

  $.ajax({
      type:'POST',
      url:'/resend-verification',
      data:{
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
      },

success: function(data){
  if ('success' in data) {
      setTimeout(()=>{
          btn.textContent = 'resend '
          icon.style.display="none"
          notificationText.innerHTML ='Email verification link has being sent to your mail\nkindly check your mail to activate your account'

           // Show the modal after redirect
      }, 4000)
  } else {
      setTimeout(()=>{

          btn.textContent = 'resend '
          icon.style.display="none"
          notificationText.innerHTML=data.error 
          
  
  
  
      }, 4000)
      // Handle other responses or errors
    
  }


},
  

error:function(data){
  setTimeout(()=>{

      btn.textContent = 'Sign Up '
      icon.style.display="none"
      notificationText.innerHTML='something went wrong'





  }, 4000)
  
 

}




  });


})




