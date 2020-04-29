function update(name) {
    form = document.getElementById('nameid')
    form.caller.value = name;
    form.submit();
}



function populateDropdown(){

    $(document).ready(function() {
        $('#foodkind').change(function() {
        
          var foodkind = $('#foodkind').val();
        
          // Make Ajax Request and expect JSON-encoded data
          $.getJSON(
            '/get_food' + '/' + foodkind,
            function(data) {
        
              // Remove old options
              $('#food').find('option').remove();                                
        
              // Add new items
              $.each(data, function(key, val) {
                var option_item = '<option value="' + val + '">' + val + '</option>'
                $('#food').append(option_item);
              });
            }
          );
        });
    });
}