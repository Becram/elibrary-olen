$(document).ready(function(){
  $(".das-sett").click(function(){
    $(".dd-dash").toggle();
  });

  var pathArray = window.location.href;

  $(".nav-link").removeClass("active");
  var dasText1 = "/document/add/";
  var dasText2 = "/audio/add/";
  var dasText3 = "/video/add/";
  var dasText4 = "/submission/";
  var dasText5 = "/document/update/";
  var dasText6 = "/document/delete/";

  if(pathArray.indexOf(dasText1) != -1){
      $(".das-document").addClass("active");
  }
  else if(pathArray.indexOf(dasText2) != -1){
      $(".das-audio").addClass("active");
  }
  else if(pathArray.indexOf(dasText3) != -1){
      $(".das-video").addClass("active");
  }
  else if(pathArray.indexOf(dasText4) != -1){
      $(".das-submission").addClass("active");
  }
  else if(pathArray.indexOf(dasText5) != -1){
      $(".das-submission").addClass("active");
  }
   else if(pathArray.indexOf(dasText6) != -1){
      $(".das-submission").addClass("active");
  }
  else{
      $(".das-home").addClass("active");
  }
});