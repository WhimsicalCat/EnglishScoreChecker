function change_data(data) {
//  console.log('change_data called');
//  console.log(data);
  $('#r_num_of_chars').text(data.num_of_chars);
  $('#r_num_of_words').text(data.num_of_words);
  $('#r_num_of_grammers').text(data.num_of_used_grammer_content);
  $('#r_num_of_incorrect').text(data.num_of_incorrect);
  $('#r_cefr_level').text(data.CEFR_level);
}

$(function() {
  var activeTab = $('a[data-toggle="tab"][class*="active"]').attr('href');
  
  $('a[data-toggle="tab"]').on('click', function(e) {
    activeTab = $(e.target).attr('href');
    $('#inputtext').val('').keyup();
//    console.log(activeTab);
  });
  
  function when_text_changed(e) {
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
//        console.log('bigger')
      } else {
        $('#check_mark').removeClass('fa-check');
        $('#check_mark').addClass('fa-ban');
        $('#submit_button').attr('disabled', '');
//        console.log('smaller')
      }
    })
    .fail(function(recv){
      
    });
  }
  
  $('#inputtext').on('paste', function(e) {
    setTimeout( function() {
      when_text_changed(e);
    }, 10);
  });
  
  $('#inputtext').on('mouseup', function(e) {
    setTimeout( function() {
      when_text_changed(e);
    }, 10);
  });
  
  $('#inputtext').keyup(when_text_changed);
  
  var def_activated_type = location.search.match('type=(.*?)(&|$)');
  if (def_activated_type){
//    console.log(decodeURIComponent(def_activated_type[1]));
    $(decodeURIComponent(def_activated_type[1])).click();
  }
  var def_text = location.search.match('txt=(.*?)(&|$)');
//  console.log(def_text);
  if (def_text){
    $('#inputtext').val(decodeURIComponent(def_text[1])).keyup();
  }
  
  if (rcv_data){
    change_data(rcv_data);
    
    var chart_canvas = document.getElementById('level_chart').getContext('2d');
//    console.log(rcv_data.chart_data);
//    console.log(rcv_data.chart_options);
    
    var myPieChart = new Chart(chart_canvas,{
      type: 'pie',
      data: rcv_data.chart_data,
      options: rcv_data.chart_options
    });
  }
  
  $('#submit_button').on('click', function(e) {
    window.location.search = 'txt=' 
                             + encodeURIComponent($('#inputtext').val()) 
                             + '&type=' 
                             + activeTab;
  });
//  console.log(activeTab);
});