/*------------------------------------refresh quary-------------------------------- code-----------------------------*/
const  btn = document.querySelector('.taskbtn-txt')
const  icon= document.querySelector('.fa-spinner')

$(document).one('submit', '#taskForm', function(e){
 e.preventDefault();
 var formData = new FormData(this);
 btn.textContent = ' '
 icon.style.display="block"


 $.ajax({
     type:'POST',
     url:'/course_task',
     processData: false,
     contentType: false,
     data: formData,

success: function(data){
 if ('success' in data) {
     setTimeout(()=>{
         btn.textContent = 'Submit'
         icon.style.display="none"
         swal('Task Submmited', data.success, 'success')





     }, 1000)}

   else if  ('tasktaken' in data) {
        setTimeout(()=>{
            btn.textContent = 'Submit'
            icon.style.display="none"
            swal('Task Submmited', data.tasktaken, 'info')





        }, 1000)}

  else {
     setTimeout(()=>{

         btn.textContent = 'Submit '
         icon.style.display="none"
         swal('Error', data.error, 'error')





     }, 1000)
     // Handle other responses or errors

 }


},


error:function(data){
 setTimeout(()=>{

     btn.textContent = 'Submit '
     icon.style.display="none"
     swal('Error', data.error, 'error')



 }, 1000)



}




 });


})





