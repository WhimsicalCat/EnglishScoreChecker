//$('#selector a').on('click', function (e) {
//  e.preventDefault()
//  $(this).tab('show')
//})

$(function() {
  $('a[data-toggle="tab"]').on('click', function(e) {
//        window.localStorage.setItem('activeTab', $(e.target).attr('href'));
    var activeTab = $(e.target).attr('href');
    $('#selector a[href="' + activeTab + '"]').tab('show');
  });
//  var activeTab = window.localStorage.getItem('activeTab');
//  if (activeTab) {
//    $('#myTab a[href="' + activeTab + '"]').tab('show');
//    window.localStorage.removeItem("activeTab");
  }
});