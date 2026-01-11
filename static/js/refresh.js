const result = document.querySelector('.alert')
const btn = document.querySelector('.btn-txt')

/*---------------------------------------resend verification----------------------------*/
const resendBtn =document.querySelector('.resendbtn')
const resendNotificationTxt = document.querySelector('.notification-container')
const resendspinner = document.querySelector('.resendbtn-spinner')


$(document).on('submit', '#resendVerification', function(e){
    e.preventDefault();
    resendBtn.textContent = ' '
    resendspinner.style.display="block"

    $.ajax({
        type:'POST',
        url:'/resend-verification',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },


success: function(data){
    if ('success' in data) {
        setTimeout(()=>{

           const newHTML = `
           <div class="notification-container" style="color:#1c32ff; font-weight:600;">
               ${data.success}
               <button type="submit" style="border: none; background: none;text-decoration:none; cursor: pointer;color:#57bcff">
                   <i class="fa fa-spinner resendbtn-spinner" aria-hidden="true" style="display:none;"></i>
               </button>
           </div>`;
            resendNotificationTxt.innerHTML=newHTML
            resendspinner.style.display="none"
            resendBtn.innerHTML='resend'
           
            
             // Show the modal after redirect
        }, 1200)
       
    } else {
        setTimeout(()=>{
            resendspinner.style.display="none"

            resendBtn.innerHTML='resend'
            swal('Email Verification', data.error, 'error') 
            .then(() => {
                // Refresh the page after the OK button is clicked
                location.reload(); // Refresh the page
            });
           

            
             // Show the modal after redirect
        }, 1000)
       
        // Handle other responses or errors
      
    }


},
    

error:function(data){
    setTimeout(()=>{
        resendspinner.style.display="none"

        resendBtn.innerHTML='resend'
        swal('Email Verification', data.error, 'error') 
        .then(() => {
            // Refresh the page after the OK button is clicked
            location.reload(); // Refresh the page
        });
        
        
        
         
          // Show the modal after redirect
     }, 1000)
 
   

}




    });


})










