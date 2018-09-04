$(document).ready(function(){

  // navbar selected
  var x, i, j, selElmnt, a, b, c;
  /*look for any elements with the class "ole-custom-select":*/
  x = document.getElementsByClassName("ole-custom-select");
  for (i = 0; i < x.length; i++) {
    selElmnt = x[i].getElementsByTagName("select")[0];
    /*for each element, create a new DIV that will act as the selected item:*/
    a = document.createElement("DIV");
    a.setAttribute("class", "select-selected");
    a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
    x[i].appendChild(a);
    /*for each element, create a new DIV that will contain the option list:*/
    b = document.createElement("DIV");
    b.setAttribute("class", "select-items select-hide");
    for (j = 0; j < selElmnt.length; j++) {
      /*for each option in the original select element,
      create a new DIV that will act as an option item:*/
      c = document.createElement("DIV");
      c.innerHTML = selElmnt.options[j].innerHTML;
      c.addEventListener("click", function(e) {
          /*when an item is clicked, update the original select box,
          and the selected item:*/
          var y, i, k, s, h;
          s = this.parentNode.parentNode.getElementsByTagName("select")[0];
          h = this.parentNode.previousSibling;
          for (i = 0; i < s.length; i++) {
            if (s.options[i].innerHTML == this.innerHTML) {
              s.selectedIndex = i;
              h.innerHTML = this.innerHTML;
              y = this.parentNode.getElementsByClassName("same-as-selected");
              for (k = 0; k < y.length; k++) {
                y[k].removeAttribute("class");
              }
              this.setAttribute("class", "same-as-selected");
              break;
            }
          }
          h.click();
      });
      b.appendChild(c);
    }
    x[i].appendChild(b);
    a.addEventListener("click", function(e) {
        /*when the select box is clicked, close any other select boxes,
        and open/close the current select box:*/
        e.stopPropagation();
        closeAllSelect(this);
        this.nextSibling.classList.toggle("select-hide");
        this.classList.toggle("select-arrow-active");
      });
  }
  setPadding();



  function closeAllSelect(elmnt) {
    /*a function that will close all select boxes in the document,
    except the current select box:*/
    var x, y, i, arrNo = [];
    x = document.getElementsByClassName("select-items");
    y = document.getElementsByClassName("select-selected");
    for (i = 0; i < y.length; i++) {
      if (elmnt == y[i]) {
        arrNo.push(i)
      } else {
        y[i].classList.remove("select-arrow-active");
      }
    }
    for (i = 0; i < x.length; i++) {
      if (arrNo.indexOf(i)) {
        x[i].classList.add("select-hide");
      }
    }
  }
  /*if the user clicks anywhere outside the select box,
  then close all select boxes:*/
  document.addEventListener("click", closeAllSelect);
  // navbar select end

  // burger menu for mobile view
  $("#burger-menu").click(function(){
      $( ".sidenav" ).toggle();
  });



// drop down menu code
  var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}

// title page grid, list view

$(".ole-gr-lt-icon").click(function(){
  if($(this).hasClass("ole-gr-ly-inactive")){
    $(this).siblings( ".ole-gr-ly-active" ).addClass("ole-gr-ly-inactive").removeClass("ole-gr-ly-active");
    $(this).addClass("ole-gr-ly-active").removeClass("ole-gr-ly-inactive");

    $(".grid-book-cont").toggleClass("list-book-cont");

    if($(this).hasClass("fa-list")){
      $(".grid-book-cont").parent().addClass("col-md-12").removeClass("col-md-3");
      $
    }
    else{
      $(".grid-book-cont").parent().addClass("col-md-3").removeClass("col-md-12");
    }

  }
});

// hide show filters in Title

$(".tit-filter-btn").click(function(){
  $(".tit-sid-lst").toggle();
});

$(".select-items div").click(function(){
  var forPadd;
  forPadd = $(".ole-custom-select").width();
  forPadd = forPadd + 10;
  $(".sbx-custom__input").css("padding-left", forPadd + "px");
});

});


function setPadding() {
    // script to set the padding of search bar
  var conceptName = $('#searchIn').find(":selected").val();
  var searchBox =  $("#project");

  var forPadd = 0;
  forPadd = $(".ole-custom-select").width();
  forPadd = forPadd + 10;

  if (conceptName === "audio") {
    searchBox.css("padding-left", forPadd);
  }

  if (conceptName === "document") {
    searchBox.css("padding-left", forPadd);
  }
  if (conceptName === "video") {
    searchBox.css("padding-left", forPadd);
  }
}


// book, audio and detail page read more code
function readMore($curRev){
  var length = $curRev.text().length;
  var originalText = $curRev.text();
  var splittedText = "";

  if (length > 100) {
    splittedText = $curRev.text().substring(0, 100);
    splittedText += "...";
    $curRev.siblings(".ole-read-more").show(0);
  }

  $curRev.text(splittedText);

  $("#button_more").click(function() {
    $curRev.text(originalText);
    $curRev.hide(0);
    $curRev.show(0);
    $("#button_more").hide(0);
  });
}

// book, audio and detail page read more code
function readMore($curRev){
  var length = $curRev.text().length;
  var originalText = $curRev.text();
  var splittedText = "";

  if (length > 100) {
    splittedText = $curRev.text().substring(0, 100);
    splittedText += "...";
    $curRev.siblings(".ole-read-more").show(0);
  }

  $curRev.text(splittedText);

  $("#button_more").click(function() {
    $curRev.text(originalText);
    $curRev.hide(0);
    $curRev.show(0);
    $("#button_more").hide(0);
  });
}

// Select all links with hashes
$('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .click(function(event) {
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
      &&
      location.hostname == this.hostname
    ) {
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }
  });

// scroll to top of the page
$(window).scroll(function () {
  if ($(this).scrollTop() > 50) {
      $('#back-to-top').fadeIn();
  } else {
      $('#back-to-top').fadeOut();
  }
});
// scroll body to 0px on click
$('#back-to-top').click(function () {
  $('#back-to-top').tooltip('hide');
  $('body,html').animate({
      scrollTop: 0
  }, 800);
  return false;
});

$('#back-to-top').tooltip('show');
