
    const openModalBtn = document.querySelectorAll(".coursemodal");
    const modal = document.querySelector(".enrollmodal");
    const closeModalBtn = document.querySelector(".enrollclose");
    const courseTitle = document.querySelectorAll('.course-title')
    const coursefield  = document.querySelector('#coursefield')
    const courseDescription = document.querySelectorAll('.course-descpt')
    const courseDescriptionVal = document.querySelector('#course-descpt-val')
    const courseIDVal= document.querySelector('#courseidval')
    const courseID = document.querySelectorAll('.course-id')
  
openModalBtn.forEach((openModalBtn, index) => {
       
    openModalBtn.addEventListener("click", function () {
      modal.style.display = "block";
      let courseTitleVal =  courseTitle[index].textContent
      coursefield.value = courseTitleVal.toUpperCase()
      let courseDescript = courseDescription[index].textContent
      courseDescriptionVal.innerHTML = courseDescript
      let courseid= courseID[index].value
      courseIDVal.value = courseid

  
   
    });
    
   
    closeModalBtn.addEventListener("click", function () {
      modal.style.display = "none";
    });
  
  
  });
/*------------------------------------refresh quary-------------------------------- code-----------------------------*/
   const  btn = document.querySelector('.btn-txt')
   const  icon= document.querySelector('.fa-spinner')
  
  $(document).on('submit', '#enrollmentForm', function(e){
    e.preventDefault();
    var formData = new FormData(this);
    btn.textContent = ' '
    icon.style.display="block"
    
  
    $.ajax({
        type:'POST',
        url:'/course_enrollment',
        processData: false,
        contentType: false,
        data: formData,

success: function(data){
    if ('success' in data) {
        setTimeout(()=>{
            btn.textContent = 'Submit'
            icon.style.display="none"
        
            swal('Course Enrolled', data.success, 'success')
            .then(() => {
                // Refresh the page after the OK button is clicked
                location.reload() // Refresh the page
            });
            
            
        }, 1500)}
      else if ('enrolled' in data) {
            setTimeout(()=>{
                btn.textContent = 'Submit'
                icon.style.display="none"

                swal('Course Enrolled', data.enrroled, 'info')
           
              
            
                
                
            }, 1000)
    } else {
        setTimeout(()=>{

            btn.textContent = 'Submit '
            icon.style.display="none"
          
            swal('Course Enrollment', data.error, 'error')
           
            
    
    
    
        }, 1000)
        // Handle other responses or errors
      
    }


},
    

error:function(data){
    setTimeout(()=>{

        btn.textContent = 'Submit '
        icon.style.display="none"
        notifymdal.style.display='block'
        swal('Course Enrollment', data.error, 'error')
        



    }, 1000)
    
   

}




    });


})





  