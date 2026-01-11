var signinbtn = document.querySelector('.signbtn-txt')
var signinicon = document.querySelector('.signInIcon')
var signinalert = document.querySelector('.signin-alert')
  


// prevent a space bar for username 
document.getElementById('susername').addEventListener('keypress', function(e) {
  if (e.key === ' ') {
      e.preventDefault();  // Prevents the space character from being input
  }
});



/*------------------------------------signin refresh btn----------------------------------*/
$(document).on('submit', '#signinForm', function(e){
  e.preventDefault();
  signinbtn.textContent = ' '
  signinicon.style.display="block"

  $.ajax({
      type:'POST',
      url:'/signin',
      data:{
          susername:$('#susername').val(),
          spassword:$('#spassword').val(),
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
      },


success: function(data){
  if ('success' in data) {
      setTimeout(()=>{
          signinbtn.textContent = 'Sign In '
          signinicon.style.display="none"
          window.location.replace(data.success)
      }, 1000)
  } else {
      setTimeout(()=>{
          signinbtn.textContent = 'Sign In '
          signinicon.style.display="none"
          signinalert.innerHTML=data.error



      }, 4000)
      // Handle other responses or errors

  }


},


error:function(data){
  setTimeout(()=>{

      signinbtn.textContent = 'Sign In '
      signinicon.style.display="none"
      signinalert.innerHTML='something went wrong'



  }, 4000)



}




  });


})




