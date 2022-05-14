/*!
* Start Bootstrap - Simple Sidebar v6.0.5 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

$(document).ready(function() {
    $("button.add_form_field").click(function(e) {
        e.preventDefault();
        var name = $(this).closest(".container").find("input:first").attr("class")
        var numInputs = $(this).closest(".container").find("input").size()
        if (numInputs < 10) {
            numInputs++;
            if (name=="author_ids"){
                $(this).closest(".container").append('<div><input type="text" name="mytext[' + numInputs + ']"/><a href="#" class="delete">Delete</a></div>');
            }
        } else alert('You Reached the limits')
    });

    $(document).on("click", ".delete", function(e) {
        e.preventDefault();
        $(this).parent('div').remove();
    })
});