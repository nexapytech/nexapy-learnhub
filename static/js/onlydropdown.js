document.addEventListener('DOMContentLoaded', function () {
    const dropdown = document.querySelector('.dropdownonmouse');
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
