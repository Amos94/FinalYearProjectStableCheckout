
$(document).ready(function() {

  var tagSentenceRequest = function (actionType, sentenceID, tagID, postID) {
    var jqxhr = $.ajax({
      type: 'POST',
      url: "ajax/tag.php",
      data: { action: actionType, sentenceID: sentenceID, tagID: tagID, postID: postID } 
    })
    .success(function(data) { 
       console.log("tagSentenceRequest: " + data); }) 
    .error(function() { 
       console.log("Error posting sentenceID: " + sentenceID + 
                                     " tagID: " + tagID + 
                                    " postID: " + postID);
    });     
  }

  var annotatePostRequest = function(postID, comment) {
    var jqxhr = $.ajax({
      type: 'POST',
      url: "ajax/annotation.php",
      data: { postID: postID, comment: comment } 
    })
    .success(function(data) { 
       console.log("annotatePostRequest: " + data); }) 
    .error(function() { 
       console.log("Error annotating post: " + postID +
                                " comment: " + comment);
    });
  }
  var updatePostAnnotationStateRequest = function(postID, state) {
    var jqxhr = $.ajax({
      type: 'POST',
      url: "ajax/annotation.php",
      data: { postID: postID, state: state } 
    })
    .success(function(data) { 
       console.log("updatePostAnnotationStateRequest: " + data); }) 
    .error(function() { 
       console.log("Error annotating post: " + postID +
                                " state: "   + state);
    });
  }
  var getPostId = function() { 
    return $(".postTbl").prop("id").substr(1);
  }

  // -- Tag Instance Behavior --
  // Clicking on a tag instance of a sentence removes the Tag from being
  // associated with that sentence.
  $(".tagInstance.editable").click(function() {
    // Check if the tag is disabled
    if($(this).hasClass("tagDisabled")) {
      return; // skip if tag is disabled
    }                  
    
    // for sentenceID, selects the parent 'tr' tag for the sentence id
    var sentenceID = $(this).parent().parent().prop("id").substr(1);  // chop prefix 's' from id
    var tagID = $(this).prop("id").substr(1); // chop prefix 't' from id
    var postID = getPostId();
    tagSentenceRequest('DELETE', sentenceID, tagID, postID);
    $(this).remove();
  });

  $(".tagBtn").click(function() {
    if($(this).hasClass("tagDisabled")) {
      return;
    }                  
    

    var sentenceID = $(".selected").prop("id").substr(1);
    var tagID = $(this).prop("id").substr(1);
    var postID = getPostId();

    if(sentenceID && tagID &&  postID) {
      if($('.selected .tagsSentence #t' + tagID).length == 0) {
        $(this).clone()
               .removeClass("tagBtn")
               .addClass("tagInstance")
               .click(function() { 
                 if($(this).hasClass("tagDisabled")) {
                   return;
                 }                  
                 tagSentenceRequest('DELETE', sentenceID, tagID, postID);
                 $(this).remove();                   
               })
               .appendTo(".selected .tagsSentence");
        tagSentenceRequest('INSERT', sentenceID, tagID, postID);        
      }
    } 
  });
  
  // Enforcing that only 1 sentence row at a time can be selected
  $(".sentenceRow").click(function() {
    $(".sentenceRow").removeClass("selected"); // clear other selected row
    $(this).addClass("selected");
  });
  
  // Clicking on the 'Show/Hide Instructions' button
  $('#instructions').hide();
  $('#instructionsDisplay').click(function() {
    $('#instructions').toggle();
  });

  $('#othersComments').hide();  
  $('#othersCommentsDisplay').click(function() {
    $('#othersComments').toggle();
  });

  $('#annotatorsCommentSave').addClass("invisible");

  $(".initiallyHidden").toggle(false);

  $(".finalizePostBtn").click(function() {
    if($(this).hasClass("finalizedDisabled")) {
      return;
    }
    $(".finalizePostBtn").toggle();
      });
   
  $('#finalize').click(function() {
    if($(this).hasClass("finalizedDisabled")) {
      return;
    }
    var postID = getPostId();
    
    if($(this).hasClass("adjudicatorPostBtn")) {
      updatePostAnnotationStateRequest(postID, 'ADJUDICATED');
    } else {
      updatePostAnnotationStateRequest(postID, 'DONE');
    }
    
    $('#unflag').toggle(false);
    $('#flag').toggle(true);
    $(".tag").addClass("tagDisabled");
  });
  
  $('#unfinalize').click(function() {
    if($(this).hasClass("finalizedDisabled")) {
      return;
    }
    var postID = getPostId();
    updatePostAnnotationStateRequest(postID, 'IN_PROGRESS');
    $(".tag").removeClass("tagDisabled");
  });
  if($('#finalize').hasClass("initiallyHidden")) {
    $(".tag").addClass("tagDisabled");
  }
  if($('#finalize').hasClass("finalizedDisabled")) {
    $(".tag").addClass("tagDisabled");
  }
  if($('#unfinalize').hasClass("finalizedDisabled")) {
    $(".tag").addClass("tagDisabled");
  }
  
});