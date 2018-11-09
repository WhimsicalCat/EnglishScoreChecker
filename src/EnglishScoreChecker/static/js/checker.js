//$('#selector a').on('click', function (e) {
//  e.preventDefault()
//  $(this).tab('show')
//})

$(function() {
  var activeTab = $('a[data-toggle="tab"][class*="active"]').attr('href');
  $('a[data-toggle="tab"]').on('click', function(e) {
    activeTab = $(e.target).attr('href');
//    $('#selector a[href="' + activeTab + '"]').tab('show');
    console.log(activeTab);
  });
  $('textarea[id="inputtext"').keyup(function(e) {
    console.log($(e.target).val())
  });
  console.log(activeTab);
});