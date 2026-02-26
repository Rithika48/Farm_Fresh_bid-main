// bid_app/static/js/your_script.js
$(document).ready(function() {
    $("#programming").change(function() {
        //var url = '/load-courses/';  // URL of the `load_courses` view
        //var programmingId = $(this).val();  // Get the selected category ID

        //$.ajax({
          //  url: url,
           // data: {
              //  'programming': programmingId
          //  },
           // success: function(data) {
               // $("#courses").html('');  // Clear previous options
               // $("#courses").append('<option value="">--- Select Subcategory ---</option>'); // Add default option
               // $.each(data, function(index, item) {
             //       $("#courses").append('<option value="' + item.id + '">' + item.name + '</option>'); // Populate the subcategory dropdown
           //     });
          //  },
           // error: function(xhr, status, error) {
           //     console.error("AJAX Error: " + status + error); // Log the error
          //      alert("An error occurred while loading subcategories. Please try again.");
       // });
    });
});