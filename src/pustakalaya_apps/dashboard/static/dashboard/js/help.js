$(document).ready(function(){
  $(".help-main-ques").click(function(){
    $(this).children(".help-ico").text(function(i, v){
       return v === '+' ? '-' : '+'
    });
  });

  $(".exp-main").click(function(){
    $(".collapse").removeAttr( "style" )
    $('.collapse').toggle(function() {
      $('.collapse').addClass('show');
}, function() {
  $('.collapse').removeClass('show');
});

    $(this).children(".exp-txt").text(function(i, v){
      // $('#help1').collapse({
      //   toggle: true
      // });

       return v === 'EXPAND ALL +' ? 'COLLAPSE ALL -' : 'EXPAND ALL +';
    });
  });

});
