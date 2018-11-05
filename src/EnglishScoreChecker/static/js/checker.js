var activeTab = "#essay";

$(function() {
  $('a[data-toggle="tab"]').on('click', function(e) {
//        window.localStorage.setItem('activeTab', $(e.target).attr('href'));
    activeTab = $(e.target).attr('href');
    console.log(activeTab);
    $('#selector a[href="' + activeTab + '"]').tab('show');
  });
  console.log(activeTab);
//  var activeTab = window.localStorage.getItem('activeTab');
//  if (activeTab) {
//    $('#myTab a[href="' + activeTab + '"]').tab('show');
//    window.localStorage.removeItem("activeTab");
//  }
});