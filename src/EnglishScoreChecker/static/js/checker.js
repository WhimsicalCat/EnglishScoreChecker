
$(function() {
  var activeTab = $('a[data-toggle="tab"][class*="active"]').attr('href');
  $('a[data-toggle="tab"]').on('click', function(e) {
    activeTab = $(e.target).attr('href');
//    console.log(activeTab);
  });
  $('textarea[id="inputtext"]').keyup(function(e) {
//    console.log($(e.target).val());
    $.ajax({
      url: 'count_word',
      type: "POST",
      data: {
        'data':$(e.target).val()
      }
    })
    .done(function(recv){
      $('#num_of_word').text(recv)
//      console.log(parseInt(recv));
      if (parseInt(recv) >= 10){
        $('#check_mark').removeClass('fa-ban');
        $('#check_mark').addClass('fa-check');
        $('#submit_button').removeAttr('disabled');
        console.log('bigger')
      } else {
        $('#check_mark').removeClass('fa-check');
        $('#check_mark').addClass('fa-ban');
        $('#submit_button').attr('disabled', '');
        console.log('smaller')
      }
    })
    .fail(function(recv){
      
    });
  });
//  console.log(activeTab);
});