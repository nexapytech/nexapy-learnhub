
const postText= document.querySelector('#postText')
const icon = document.querySelector('.post-icon')
 submiButton = document.querySelector('#tweet-button');



$(document).one('submit', '#createNote', function(e){
    e.preventDefault();
    submiButton.type='button'
    var formData = new FormData(this);
    icon.style.display="inline-block";
    postText.innerHTML='Posting...'


    $.ajax({
        type:'POST',
        url:'/create_post',
        processData: false,
        contentType: false,
        data:  formData,

success: function(data){
    if ('success' in data) {
        setTimeout(()=>{
           icon.style.display="None"
            postText.innerHTML='Post'
            swal('POST', data.success, 'success')
            .then(() => {
                // Refresh the page after the OK button is clicked
                location.reload(); // Refresh the page
            });





             // Show the modal after redirect
        }, 1500)


    }

    else{
        setTimeout(()=>{

            icon.style.display="none"
            postText.innerHTML='Post'
            swal('POST', data.error, 'error')
          .then(() => {
            // Refresh the page after the OK button is clicked
            location.reload(); // Refresh the page
        });



             // Show the modal after redirect
        }, 1000)



    }


},
error:function(data){
    setTimeout(()=>{

        icon.style.display="none"
        postText.innerHTML='Post'
        swal('Error', data.error, "error")




    },1000)


}

    });


})
//=---------------------------------------------------functions

var uploadButton = document.querySelector('#upload-button');
var tweetbutton = document.querySelector('#tweet-button')
var inputfile = document.querySelector('#image-video-input');
var previewContainer = document.querySelector('#file-preview-container');
var tweetButton = document.querySelector('#tweet-button');
var codefile = document.querySelector('#codefile-input')
var codefileicon = document.querySelector('#codefile-icon')





const comment_image_input = document.querySelector('#comment-image-input')
const comment_codefile_input = document.querySelector('#comment-codefile-input')
const comment_upload_button = document.querySelector('#comment-upload-button')
const comment_codefile_icon = document.querySelector('#comment-codefile-icon')
const comment_tweetButton = document.querySelector('#comment-tweet-button');
const comment_previewContainer = document.querySelector('#comment-file-preview-container')




comment_upload_button.onclick = function() {
    comment_image_input.click();

 };
comment_codefile_icon.onclick = function() {
   comment_codefile_input.click();

 };


//------------------------------------this is for comment----------------------------------------------------------
function commenthandleFiles(inputfile) {

    comment_previewContainer.innerHTML = ''; // Clear the preview container

    for (var i = 0; i < inputfile.files.length; i++) {
        var file = inputfile.files[i];


        if (comment_previewContainer.children.length <2){
        var comment_filePreview = document.createElement('div');
        comment_filePreview.classList.add('file-preview');


        var commentfileUrl = URL.createObjectURL(file);
        if (file.type.startsWith('image/') || file.type.startsWith('video/')) {
            var comment_mediaElement;
            if (file.type.startsWith('image/')) {
                comment_mediaElement = document.createElement('img');
            } else if (file.type.startsWith('video/')) {
                comment_mediaElement = document.createElement('video');
                comment_mediaElement.controls = true;
                comment_mediaElement.autoplay = true; // Enable autoplay
                comment_mediaElement.muted = true; // Mute the video
            }
            comment_mediaElement.src = commentfileUrl;
            comment_mediaElement.onload = function() {
                URL.revokeObjectURL(comment_mediaElement.src);  // Clean up memory
            };
            comment_filePreview.appendChild(comment_mediaElement);
        } else {
            var comment_fileIcon = document.createElement('div');
            comment_fileIcon.classList.add('file-icon');
            comment_filePreview.appendChild(comment_fileIcon);

            var comment_fileExtension = document.createElement('div');
            comment_fileExtension.classList.add('file-extension');
            comment_fileExtension.textContent = file.name.split('.').pop().toUpperCase();
            comment_fileIcon.appendChild(comment_fileExtension);
        }
    }
    else{
        alert('you can upload up to 5 files')
        break
    }
        var comment_selectedOverlay = document.createElement('div');
        comment_selectedOverlay.classList.add('comment-selected-overlay');
        comment_filePreview.appendChild(comment_selectedOverlay);

        comment_filePreview.addEventListener('click', function(event) {
            var comment_fileKey = event.currentTarget.dataset.key;
            if (selectedFiles[comment_fileKey]) {
                // Deselect file
                selectedFiles[comment_fileKey] = false;
                event.currentTarget.querySelector('.comment-selected-overlay').classList.remove('show');
            } else {
                // Select file
                selectedFiles[comment_fileKey] = true;
                event.currentTarget.querySelector('.comment-selected-overlay').classList.add('show');
            }
        });

        comment_filePreview.dataset.key = i; // Set a unique key for each file preview
        comment_previewContainer.appendChild(comment_filePreview);
    }
 }






 document.querySelector('#comment-image-input').onchange = function() {
    if (this.files.length == 1) {
        commenthandleFiles(this);
        comment_tweetButton.disabled = false
    }
    else{
      alert('You can only select up to 1 files.')
      this.value=''
 }


 };

 document.querySelector('#comment-codefile-input').onchange = function() {
    if (this.files.length == 1) {

             commenthandleFiles(this);
             comment_tweetButton.disabled = false
    }
    else{
     alert('You can only select up to 5 files.')
     this.value=''
 }
 };











//------------------------------------------------------------------------------------------
// for coment file upload---------------------------------


uploadButton.onclick = function() {
   inputfile.click();

};
codefileicon.onclick = function() {
   codefile.click();

};

function handleFiles(inputfile) {

   previewContainer.innerHTML = ''; // Clear the preview container

   for (var i = 0; i < inputfile.files.length; i++) {
       var file = inputfile.files[i];


       if (previewContainer.children.length <5){
       var filePreview = document.createElement('div');
       filePreview.classList.add('file-preview');


       var fileUrl = URL.createObjectURL(file);
       if (file.type.startsWith('image/') || file.type.startsWith('video/')) {
           var mediaElement;
           if (file.type.startsWith('image/')) {
               mediaElement = document.createElement('img');
           } else if (file.type.startsWith('video/')) {
               mediaElement = document.createElement('video');
               mediaElement.controls = true;
               mediaElement.autoplay = true; // Enable autoplay
               mediaElement.muted = true; // Mute the video
           }
           mediaElement.src = fileUrl;
           mediaElement.onload = function() {
               URL.revokeObjectURL(mediaElement.src);  // Clean up memory
           };
           filePreview.appendChild(mediaElement);
       } else {
           var fileIcon = document.createElement('div');
           fileIcon.classList.add('file-icon');
           filePreview.appendChild(fileIcon);

           var fileExtension = document.createElement('div');
           fileExtension.classList.add('file-extension');
           fileExtension.textContent = file.name.split('.').pop().toUpperCase();
           fileIcon.appendChild(fileExtension);
       }
   }
   else{
       alert('you can upload up to 5 files')
       break
   }
       var selectedOverlay = document.createElement('div');
       selectedOverlay.classList.add('selected-overlay');
       filePreview.appendChild(selectedOverlay);

       filePreview.addEventListener('click', function(event) {
           var fileKey = event.currentTarget.dataset.key;
           if (selectedFiles[fileKey]) {
               // Deselect file
               selectedFiles[fileKey] = false;
               event.currentTarget.querySelector('.selected-overlay').classList.remove('show');
           } else {
               // Select file
               selectedFiles[fileKey] = true;
               event.currentTarget.querySelector('.selected-overlay').classList.add('show');
           }
       });

       filePreview.dataset.key = i; // Set a unique key for each file preview
       previewContainer.appendChild(filePreview);
   }
}






document.querySelector('#image-video-input').onchange = function() {
   if (this.files.length <= 5) {
       handleFiles(this);
       tweetButton.disabled = false
   }
   else{
     alert('You can only select up to 5 files.')
     this.value=''
}


};

document.querySelector('#codefile-input').onchange = function() {
   if (this.files.length <= 5) {

            handleFiles(this);
            tweetButton.disabled = false
   }
   else{
    alert('You can only select up to 5 files.')
    this.value=''
}
};


//------------------------------------------like post-------------------------------------------------------
function likepost(element) {
    // Find the span with the class 'amount' within the clicked element
    var likeBtn = element.querySelector('#like_post');
    if (likeBtn.style.color == 'black') {
        likeBtn.style.color = 'blue';
    } else {
        likeBtn.style.color = 'black';
    }

}


$(document).on('submit', '#LikePost', function(e){
    e.preventDefault();


    var formData = new FormData(this);




    $.ajax({
        type:'POST',
        url:'/like_post',
        processData: false,
        contentType: false,
        data:  formData,

success: function(data){
    if ('success' in data) {

        swal('POST', data.success, 'success')

        .then(() => {
            // Refresh the page after the OK button is clicked
            location.reload(); // Refresh the page
        });






    }
    else if ('info' in data) {

            swal('POST', data.info, 'info')

            .then(() => {
                // Refresh the page after the OK button is clicked
                location.reload(); // Refresh the page
            });



    }


},
error:function(data){



}

    });


})








//---------------------------------------------------------------------------------------------------------
chatinput = document.querySelector('#chatInput')
$(document).on('submit', '#ChatBox', function(e){
    e.preventDefault();


    var formData = new FormData(this);



    $.ajax({
        type:'POST',
        url:'/create_post',
        processData: false,
        contentType: false,
        data:  formData,

success: function(data){
    if ('success' in data) {
        chatinput.value = ''
        swal('POST', data.success, 'success')
        .then(() => {
            // Refresh the page after the OK button is clicked
            location.reload(); // Refresh the page
        });



    }

    else{
        setTimeout(()=>{


            swal('POST', data.error, 'error')
            .then(() => {
                // Refresh the page after the OK button is clicked
                location.reload(); // Refresh the page
            });





             // Show the modal after redirect
        }, 100)



    }


},
error:function(data){
    alert(data.error)

}

    });


})
//=----------------------------------coment----------------------------------------------------
  const commentinputextarea = document.querySelector('#comment-input')
$(document).on('submit', '#createcomment', function(e){
    e.preventDefault();


    var formData = new FormData(this);



    $.ajax({
        type:'POST',
        url:'/create_comment',
        processData: false,
        contentType: false,
        data:  formData,

success: function(data){
    if ('success' in data) {
        commentinputextarea.value = ''
        swal('comment', data.success, 'success')
        .then(() => {
            // Refresh the page after the OK button is clicked
            location.reload(); // Refresh the page
        });

    }

    else{

        swal('error', data.error, 'error')








    }


},
error:function(data){
    swal('comment', data.errror, 'error')
    .then(() => {
        // Refresh the page after the OK button is clicked
        location.reload(); // Refresh the page
    });

}

    });


})
//=----------------------------------




//=-----------------------------------------comment----------------------------------------------------
  const commentextarea = document.querySelector('.comment-input')
  const commentText = document.querySelector('#commentText')
  const commenticon = document.querySelector('.fa-spinner')
$(document).one('submit', '#createPostComment', function(e){
    e.preventDefault();
    commenticon.style.display="inline-block";


    var formData = new FormData(this);



    $.ajax({
        type:'POST',
        url:'/create_comment',
        processData: false,
        contentType: false,
        data:  formData,

success: function(data){
    if ('success' in data) {
          setTimeout(()=>{

        commentextarea.value = ''
        commenticon.style.display = 'None'
        commentText.innerHTML = 'Comment'
        swal('comment', data.success, 'success')
        .then(() => {
            // Refresh the page after the OK button is clicked
            location.reload(); // Refresh the page
        });


                 // Show the modal after redirect
                }, 1500)

    }

    else{
        setTimeout(()=>{
            swal('comment', data.error, 'error')
            .then(() => {
                // Refresh the page after the OK button is clicked
                location.reload(); // Refresh the page
            });
            commenticon.style.display = 'None'
            commentText.innerHTML = 'Comment'


          // Show the modal after redirect
        }, 1500)





    }


},
error:function(data){
    setTimeout(()=>{
        alert(data.error)
        commenticon.style.display = 'None'
        commentText.innerHTML = 'Comment'


      // Show the modal after redirect
    }, 1500)





}




    });

})


//=----------------------------------delete post -------------------------------------

$(document).on('submit', '#deletepost', function(e){
    e.preventDefault();

    var formData = new FormData(this);



    $.ajax({
        type:'POST',
        url:'/delete_post',
        processData: false,
        contentType: false,
        data:  formData,

success: function(data){
    if ('deletepost' in data) {
            swal('POST', data.deletepost, 'success')
            .then(() => {
                // Refresh the page after the OK button is clicked
                location.reload(); // Refresh the page
            });




    }

    else{

        swal('DATA', data.error, 'error')





    }


},
error:function(data){
    swal('DATA', data.error, 'error')

}

    });


})




//=----------------------------------loadmore -------------------------------------

$(document).on('submit', '#loadmore', function(e){
    e.preventDefault();

    var formData = new FormData(this);



    $.ajax({
        type:'POST',
        url:'/loadmore',
        processData: false,
        contentType: false,
        data:  formData,

success: function(data){
    if ('loadmore' in data) {

            location.reload(); // Refresh the page


    }

    else{

        swal('DATA', data.error, 'error')





    }


},
error:function(data){
    swal('DATA', data.error, 'error')

}

    });


})




window.onload = function() {
    if (window.location.hash) {
        const element = document.querySelector(window.location.hash);
        if (element) {
            element.scrollIntoView();
        }
    }
}