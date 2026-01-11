//------------------------section1  height adjustment-------------------------------------------
const chatBox = document.getElementById('chatBox');
const chatInput = document.querySelector('.custom-textarea');
const postbutton = document.querySelector('.paper-plane')
const createpost= document.querySelector('#openModalBtn')
const commentinput= document.querySelectorAll("#comment-input")
const commentimagefile= document.querySelectorAll(".comment-openModalBtn")
const commentsendicon= document.querySelectorAll(".comment-paper-plane")
const commentchatInput= document.querySelectorAll(".commentchatInput")

chatInput.addEventListener('input', adjustHeight);

function adjustHeight() {
    chatInput.style.height = 'auto';  // Reset the height
    chatInput.style.height = chatInput.scrollHeight + 'px';  // Set it to the scrollHeight

}


const textInput = document.getElementById('chatInput');


function formatBold(text) {
    // Replace *word* with <strong>word</strong>
    return text.replace(/\*(.*?)\*/g, '<strong>$1</strong>');
}

textInput.addEventListener('input', function() {
    const currentText = textInput.innerHTML;
    const formattedText = formatBold(currentText);


    // Update innerHTML to remove asterisks and apply bold formatting
    textInput.innerHTML = formattedText;

    // Move the cursor to the end

});






// for coment input----------------------------------------------------
commentinput.forEach((commentinput, index) => {
    commentinput.addEventListener('input', () => {

        if (commentinput.value.trim().length > 0) {

            commentsendicon[index].style.display = 'inline-block';
            commentimagefile[index].style.display = 'none';
        } else {
            commentsendicon[index].style.display = 'none';
            commentimagefile[index].style.display = 'inline-block';
        }

    });
});

chatInput.addEventListener('input', () => {
            if (chatInput.value.trim().length > 0) {
                postbutton.style.display = 'inline-block';

                 createpost.style.display='none'

            } else {
                postbutton.style.display = 'none';
                createpost.style.display="inline-block"
            }
        });



        //----------------------commment modal------------------------------------
        document.addEventListener('DOMContentLoaded', () => {
            const commentmodal = document.querySelector('.comment-modal');
            const commentopenModalBtn = document.querySelectorAll('.comment-openModalBtn');
            const commentpostid = document.querySelector('.comment-input')
            const commentcloseBtn = document.querySelector('.comment-close-btn');
            const postid = document.querySelector('.comment-img-file-post_id')


            commentopenModalBtn.forEach((commentopenModalBtn, index) => {
            commentopenModalBtn.addEventListener('click', () => {

                commentmodal.style.display = 'block';
                var postId = document.querySelectorAll('#postdata');
                postid.value = postId[index].getAttribute('data')





            });

            commentcloseBtn.onclick = function() {
                commentmodal.style.display = 'none';
            }
            window.onclick = function(event) {
                if (event.target == modal) {
                    commentmodal.style.display = 'none';
                }
            }




        });


        })


//--------------------------------openmodal--------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    const openModalBtn = document.getElementById('openModalBtn');
    const closeBtn = document.getElementsByClassName('close-btn')[0];




    openModalBtn.onclick = function() {
        modal.style.display = 'block';
    }

    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});

//-------------------fielextention---------------------------------------
var fileExtension = document.querySelectorAll('.file-extension')
    var url_link = document.querySelectorAll('.download_url')
    var url = url_link.innerHTML;  // Replace with your actual URL or file name



    fileExtension.forEach((fileExtension, index) => {
        var url = url_link[index].innerHTML;  //
        fileExtension.innerHTML = url.split('.').pop().toUpperCase();

});

//--------------------------file extension----------------------------------
var fileExtension = document.querySelectorAll('.comment-file-extension')
var url_link = document.querySelectorAll('.comment-download_url')
var url = url_link.innerHTML;  // Replace with your actual URL or file name



fileExtension.forEach((fileExtension, index) => {
    var url = url_link[index].innerHTML;  //
    fileExtension.innerHTML = url.split('.').pop().toUpperCase();

});
//-----------------------------------------extension------------------------------
// Initialize the current match index
let currentMatchIndex = -1; // To keep track of the current match index

// Function to highlight all matching usernames
function highlightText() {
    // Get the search term (username) from input
    let searchTerm = document.getElementById('search-input').value;
    let foundMatches = []; // Array to hold matches

    // Get all spans in the user list
    let spans = document.querySelectorAll('span');
    spans.forEach(span => {
        // Remove any existing highlights
        span.innerHTML = span.textContent;

        if (searchTerm) {
            // Create a regex pattern to match the search term (case insensitive)
            let regex = new RegExp(searchTerm, 'gi');

            // Replace matching text with a highlighted version
            let updatedText = span.textContent.replace(regex, function(match) {
                return `<span class="highlight">${match}</span>`;
            });

            span.innerHTML = updatedText;

            // Check if the span contains highlighted text
            if (updatedText.includes('highlight')) {
                foundMatches.push(span); // Add matched span to the array
            }
        }
    });

    // Store matches in a global variable for navigation
    window.foundMatches = foundMatches;

    // Reset current index and show/hide the next match button
    currentMatchIndex = -1; // Reset the index
    document.getElementById('next-match-button').style.display = foundMatches.length > 0 ? 'block' : 'none';

    // Scroll to the first matched username if any match is found
    if (foundMatches.length > 0) {
        // Scroll to the first match and ensure it's visible
        currentMatchIndex = 0; // Set the current index to the first match
        foundMatches[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Function to go to the next match
function goToNextMatch() {
    if (window.foundMatches && window.foundMatches.length > 0) {
        currentMatchIndex = (currentMatchIndex + 1) % window.foundMatches.length; // Cycle through matches
        window.foundMatches[currentMatchIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Attach event listener to the input field to trigger highlight on input
document.getElementById('search-input').addEventListener('input', highlightText);

// Attach event listener to the next match button
document.getElementById('next-match-button').addEventListener('click', goToNextMatch);

//--------------------------loadmore0---------------------------------------------
$(document).ready(function() {
    var $loadMoreContainer = $('#loadmore-container');

    // Function to check if the user has scrolled to the bottom of the page
    function checkVisibility() {
        var scrollPosition = $(window).scrollTop() + $(window).height();  // Position of the bottom of the viewport
        var documentHeight = $(document).height();  // Total height of the page

        // Check if the page is scrollable (content height is greater than the window height)
        if (documentHeight > $(window).height()) {
            // Check if the user has scrolled to the bottom
            if (scrollPosition >= documentHeight - 100) {  // Adjust this offset as needed
                $loadMoreContainer.fadeIn();  // Show the button
            } else {
                $loadMoreContainer.fadeOut();  // Hide the button
            }
        } else {
            $loadMoreContainer.hide();  // Hide the button if no scrolling is possible
        }
    }

    // Initially check visibility
    checkVisibility();

    // Bind the checkVisibility function to the scroll event
    $(window).on('scroll', function() {
        checkVisibility();
    });

    // Re-check visibility when the window is resized (in case of dynamic content changes)
    $(window).on('resize', function() {
        checkVisibility();
    });
});

//---------------------refrsh icon -------------------------------------------
const refreshContainer = document.querySelector('.refresh-container');
const refreshIcon = document.getElementById('refresh-icon');

let isRefreshing = false;
let startY = 0;
let threshold = 70; // Minimum drag distance to trigger refresh

// Detect when the user starts touching the screen
document.addEventListener('touchstart', (e) => {
  if (window.scrollY === 0) { // Only detect if at the top of the page
    startY = e.touches[0].clientY;
  }
});

// Detect when the user is dragging
document.addEventListener('touchmove', (e) => {
  const currentY = e.touches[0].clientY;
  const distance = currentY - startY;

  if (distance > 0 && window.scrollY === 0 && !isRefreshing) { // Ensure user is pulling down from the top
    e.preventDefault(); // Prevent default scroll behavior

    // Move the refresh container down as the user pulls
    refreshContainer.style.top = `${Math.min(distance - 50, 50)}px`; // Max 50px down
    refreshIcon.style.opacity = Math.min(distance / 100, 1); // Increase icon opacity based on pull
  }
});

// Detect when the user stops touching (release gesture)
document.addEventListener('touchend', (e) => {
  const currentY = e.changedTouches[0].clientY;
  const distance = currentY - startY;

  // Check if the pull was enough to trigger a refresh
  if (distance > threshold && !isRefreshing) {
    triggerRefresh();
  } else {
    // If not enough, reset the refresh container
    refreshContainer.style.top = '-50px';
  }
});

function triggerRefresh() {
  isRefreshing = true;

  // Trigger rotation animation
  refreshIcon.classList.add('rotate');

  // Simulate a loading time (e.g., for fetching data)
  setTimeout(() => {
    // After loading, refresh the page or perform some action
    window.location.reload();
  }, 1000); // Simulated loading time
}
// Grab the refresh icon element
const apprefreshIcon = document.getElementById('app-refresh-icon');

// Add event listener to rotate icon and refresh page on click
apprefreshIcon.addEventListener('click', () => {
  // Add rotate class to trigger animation
  apprefreshIcon.classList.add('rotate');

  // Wait for the animation to finish (600ms), then reload the page
  setTimeout(() => {
    window.location.reload(); // Reload the page after rotation
  }, 1000); // Match this duration to the CSS animation duration (0.6s)
});
//-------------------maxlenght word--------------------

// Maximum number of characters allowed
const maxChars = 2000;

document.getElementById('chatInput').addEventListener('input', function() {
    let text = this.value;

    // Get the number of characters written
    let charsWritten = text.length;

    // Update the character count display
    document.getElementById('char-counter').innerText = charsWritten;

    // Change color to red if the character limit is reached
    if (charsWritten >= maxChars) {
        document.getElementById('word-count-status').classList.add('red');
    } else {
        document.getElementById('word-count-status').classList.remove('red');
    }
});

