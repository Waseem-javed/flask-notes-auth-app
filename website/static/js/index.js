
$(document).ready(function(){
  $('.toast').toast('show');
});

setTimeout(function(){
    $('.toast').remove();
  }, 2000);