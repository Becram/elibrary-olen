/*
This file is suppose to be used in place of video_detail_new.html script but csrf_token does
not run, therefor it has no use at this moment
*/

/***************************Review code****************************/

   // review trigger for a tag
   $("#rev_this").click(function (e){
      e.preventDefault();
        var user_name = $("input[type='hidden'][name='user']").val().trim();
        if(user_name == "" || user_name == "AnonymousUser" ){
          $("#information_message_p_tag").text('Login to post your message');
          $("#info_message_display").click();
          return;
        }else{
        $("#review_btn_trigger").click();
        }

     });

  //review_btn_trigger
   $("#review_btn_real").click(function (e){
    e.preventDefault();
      var user_name = $("input[type='hidden'][name='user']").val().trim();
      if(user_name == "" || user_name == "AnonymousUser" ){
        $("#information_message_p_tag").text('Login to post your message');
        $("#info_message_display").click();
        return;
      }else{
      $("#review_btn_trigger").click();
      }

   });

    //--for the review system
    $("#submitButton").click(function (e){
      e.preventDefault();
      var user_title = $("input[type='text'][name='title_input']").val().trim();
      var user_input = $("textarea[type='text'][name='input']").val().trim();
      var content_type = $("input[type='hidden'][name='content_type']").val().trim();
      var content_id = $("input[type='hidden'][name='content_id']").val().trim();
      var user_name = $("input[type='hidden'][name='user']").val().trim();
      //alert("title="+ user_title);
      //alert("detail="+ user_input);
      //return;
      if(user_name == "" || user_name == "AnonymousUser" ){
        //alert("Login to post you message");

        //$("#close_model_box").click();
        $("#information_message_p_tag").text('Login to post you message');
        $("#info_message_display").click();


        return;
      }else if(user_input == "" || user_title == "" ){
        //alert("Please enter the title and message properly!");

        //$("#close_model_box").click();
        $("#information_message_p_tag").text('Please enter the title and message properly!');
        $("#info_message_display").click();

        return;
      }
       $.ajax({
        type:'post',
        url: '/review_system/',
         headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                },
        data: {
          "input": user_input,
          "content_type" : content_type,
          "content_id" : content_id,
          "input_title":user_title,
        },
        success: function (data) {
          $("textarea[type='text'][name='input']").val('');
          $("input[type='text'][name='title_input']").val('');
          //alert("Your review message has been sent. It will be display here after approval from moderator");
          var pk_value = data.pk_value;

          //close_model_box
           $("#information_message_p_tag").text('Your review has been sent to the moderator. It will be available to the general public after the approval. However, you still can edit or delete your review.');
           $("#close_model_box").click();
           $("#info_message_display").click();
             //when success we need to append the data to the comment section
             $("#reviews").prepend('<div class="review-container" id="comment_'+pk_value+'">' +
                  '<br><h5 id="posted_title_'+pk_value+'">'+user_title+'</h5>'+
                  '<p>By: <span>' +user_name+'</span></p>'+
                  '<p id="posted_message_'+pk_value+'">'+user_input+'</p>'+
                  '<p>review status is unpublished</p>'+
                  '<button type="button" value="'+pk_value+'" id="'+pk_value+'" class="btn btn-sm btn-primary font-weight-bold EditComment">Edit</button>'+
                   '<button type="button" value="'+pk_value+'" class="btn btn-sm btn-warning font-weight-bold DeleteComment">Delete</button><hr>'+
             '</div>');

        },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
      });
    });

     //Method to EditComment
     $("#reviews").delegate("button.EditComment","click",function (e){

      var id_value = $(this).val();
      posted_title= $("#posted_title_"+id_value).text().trim();
      posted_message= $("#posted_message_"+id_value).text().trim();

      //alert("title="+posted_title+ "message"+posted_message);
      //alert("element="+element[0]+"id="+element_class);

      //return;
      $("#edited_title_input").val(posted_title);
      $("#edited_message_id").val(id_value);
      $("textarea#edited_message_input").val(posted_message);
       $("#edit_hidden_btn").click();

     });


    /*This is triggered when editing and sending item*/
    function sendButtonClick(){

      //data capture
      var user_input = $("textarea#edited_message_input").val().trim();
      var user_input_title =$("#edited_title_input").val().trim();
      var content_type = $("input[type='hidden'][name='content_type']").val().trim();
      var content_id = $("input[type='hidden'][name='content_id']").val().trim();
      var user_name = $("input[type='hidden'][name='user']").val().trim();
      var pk_value = $("#edited_message_id").val();
      //alert("pk="+pk_value);
      //return;



      if(user_input_title.trim() == "" || user_input.trim() == "" ){
        $("#information_message_p_tag").text('Please enter the title and message properly!');
        $("#info_message_display").click();
        return;
      }
       $.ajax({
        type:'post',
        url: '/review_system/edit/',
         headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                },
        data: {
          "input": user_input,
          "input_title":user_input_title,
          "content_type" : content_type,
          "content_id" : content_id,
          "pk_val":pk_value,
        },
        success: function (data) {

        //alert("update successful")

        //close_model_box
         $("#information_message_p_tag").text('Your message has been edited successfully!');
         $("#edited_cancel_button").click();
         $("#info_message_display").click();

         var pk_value = data.pk_value;
         var id_div = "comment_"+pk_value;
         $("#"+id_div).empty(); //Remove child element in a div

         /* 1. Delete the item first and append the new edited item in the list */

         $("#"+id_div).append('<br><h5 id="posted_title_'+pk_value+'">'+user_input_title+'</h5>'+
              '<p>By: <span>' +user_name+'</span></p>'+
              '<p id="posted_message_'+pk_value+'">'+user_input+'</p>'+
              '<p>review status is unpublished</p>'+
              '<button type="button" value="'+pk_value+'" id="'+pk_value+'" class="btn btn-sm btn-primary font-weight-bold EditComment">Edit</button>'+
              '<button type="button" value="'+pk_value+'" class="btn btn-sm btn-warning font-weight-bold DeleteComment">Delete</button><hr>'+
         '');


        },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
      });


    }//CLose of sendButtonClick

    //Function delete
    $("#reviews").delegate("button.DeleteComment","click",function (e){

      //alert("delete btn clicked")
      var pk_value = $(this).val();

      $("#message_delete_id").val(pk_value);
      $("#yes_no_message_display").click()



   }); //Close of delete container

   function DeleteButtonYes(){
     // alert("inside delete buton yes");
     //var pk_value = $(this).val();
         var pk_value = $("#message_delete_id").val()


          //alert(pk_value)
          //return;
         //console.log(pk_value);
       $.ajax({
        type:'post',
        url: '/review_system/delete/',
         headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                },
        data: {
          "input_pk": pk_value,
        },
        success: function (data) {
          //if (data.is_taken) {
          //alert('SUCCESS');

          $("#information_message_p_tag").text('Your message has been deleted !');
         $("#edited_cancel_button").click();
         $("#info_message_display").click();


         // Lets remove the element here
         $("#comment_"+pk_value).remove();



        },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
      });



   }


/***************************Close of review code****************************/
/***************************Featured item code ****************************/

//for favourite likes #favourite_hanging_place
  $("#featured_item").delegate("button#featured_not_set","click",function (e){
      e.preventDefault();
      var user_input = "yes";

      var content_type = $("input[type='hidden'][name='content_type']").val().trim();
      var content_id = $("input[type='hidden'][name='content_id']").val().trim();
      var user_name = $("input[type='hidden'][name='user']").val().trim();
      //alert("some value="+content_type+"id="+content_id+"username="+user_name);
      //return;
      if(user_name == "" || user_name == "AnonymousUser" ){
        alert("Login to add to your favourite");
        return;
      }
       $.ajax({
        type:'post',
        url: '/set_featured/',
         headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                },
        data: {
          "input": user_input,
          "content_type" : content_type,
          "content_id" : content_id,
        },
        success: function (data) {
        //alert("success to add to feature");
          $('#featured_not_set').remove();
           //This reading is done for multi language support
           var featured_added_text = "Unfeature";//$('#added_to_fav').text();

           $("#featured_item").append(''+
                           '<button type="button" class="btn ole-btn-trans det-fav-added" value="'+ content_id +'" id="featured_set"><i class="fa fa-check-circle"></i> '+featured_added_text+'</button>'
                      +'');

        },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
      });
    });


  //Added_featured , remove form feature now
   $("#featured_item").delegate(" #featured_set","click",function (e){
      e.preventDefault();
      var user_input = "no";

      var content_type = $("input[type='hidden'][name='content_type']").val().trim();
      var content_id = $("input[type='hidden'][name='content_id']").val().trim();
      var user_name = $("input[type='hidden'][name='user']").val().trim();
      if(user_name == "" || user_name == "AnonymousUser" ){
        alert("Login to add to your favourite");
        return;
      }
       $.ajax({
        type:'post',
        url: '/set_featured/featured_unset/',
         headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                },
        data: {
          "input": user_input,
          "content_type" : content_type,
          "content_id" : content_id,
        },
        success: function (data) {
        //alert("success to remove");
          $("#featured_set").remove();

          //This reading is done for multi language support
           var featured_add_text = "Feature";//$('#add_to_fav').text();

           $("#featured_item").append(''+
                           '<button type="button" value="'+ content_id +'" class="btn ole-btn-trans " id="featured_not_set" > '+featured_add_text+'</button>'
               +'');

        },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
      });
    });

/***************************End: Featured item code ****************************/