
$(function() {
  var activeTab = $('a[data-toggle="tab"][class*="active"]').attr('href');
  $('a[data-toggle="tab"]').on('click', function(e) {
    activeTab = $(e.target).attr('href');
    console.log(activeTab);
  });
  $('textarea[id="inputtext"').keyup(function(e) {
    console.log($(e.target).val())
  });
  console.log(activeTab);
});