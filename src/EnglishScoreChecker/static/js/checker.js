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
    }, 100);
  });
  
  $('#inputtext').on('mouseup', function(e) {
    setTimeout( function() {
      when_text_changed(e);
    }, 1000);
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
//    console.log('clicked');
    target = 'txt=' 
             + encodeURIComponent($('#inputtext').val()) 
             + '&type=' 
             + encodeURIComponent(activeTab);
//    console.log(target);
    window.location.search = target;
  });
  
  $('#send_feedback').on('click', function(e){
    console.log('send_feedback submitted')
    var target_form = $(this).parents('form');
    
//    console.log(target_form);
    
    var form_button = target_form.find('button');
    var def_text = location.search.match('txt=(.*?)(&|$)');
    var json_data = target_form.serializeArray();
    
    json_data.push({"name":"text",
                    "value": decodeURIComponent(def_text[1])});
    json_data.push({"name":"type",
                    "value": activeTab});
                    
    console.log(json_data);
    
    $.ajax({
      url: 'receive_feedback',
      type: "PUT",
      data: json_data,
      timeout: 10000,
      beforeSend: function(xhr, settings) {
        // ボタンを無効化し、二重送信を防止
        form_button.attr('disabled', true);
      },
      // 応答後
      complete: function(xhr, textStatus) {
        
      },
      success: function(result, textStatus, xhr) {
        alert('送信に成功しました');
        form_button.text('送信済み');
      },
      error: function(xhr, textStatus, error) {
        alert('送信に失敗しました');
        // ボタンを有効化し、再送信を許可
        form_button.attr('disabled', false);
      }
    });
  });
    
//  console.log(activeTab);
});
