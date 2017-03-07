/**
 * tagpost.js
 * created: 27-jun-2011/chipp
 *
 * Corresponds with the 'tagpost.php' page, and facilitates interactive
 * elements such as Tag buttons, and asynchronous communication with tagging
 * and annotating sentences with the database via POST requests to ajax/*.php
 * 
 * @author chipp
 */
$(document).ready(function() {
  
  /**
   * Makes a AJAX request to the server (ajax/tag.php) to tag a specific 
   * sentence with a request 
   * 
   * @param {string} actionType Possible actions 'INSERT', 'DELETE'
   * @param {integer} sentenceID Sentence ID
   * @param {integer} tagID Tag ID
   * @param {integer} postID Post ID
   */
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
  } // function tagSentenceRequest

  /**
   * Makes an AJAX request to the server (ajax/annotation.php) to annotate
   * a comment for a particular Post.
   * 
   * @param {integer} postID Post ID
   * @param {string} comment Updated coment
   */
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
  } // function annotatePostRequest

  /**
   * Makes an AJAX request to the server (ajax/annotation.php) update a Post's
   * Annotation State ('DONE' or'PROBLEM')
   * 
   * @param {integer} postID Post ID
   * @param {string} state Annotation State ('DONE' or'PROBLEM')
   */
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
  } // function updatePostAnnotationStateRequest
  
  /**
   * PostId Accessor from the DOM
   */
  var getPostId = function() { 
    return $(".postTbl").prop("id").substr(1); // chop prefix 'p' from id
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

  // -- Tag Button Behavior --
  // When a Tag Button is clicked on at the bottom of the interface, the
  // currently selected row has a tag added to it, and an tagSentenceRequest
  // is called.
  $(".tagBtn").click(function() {
    // Check if the tag is disabled
    if($(this).hasClass("tagDisabled")) {
      return; // skip if tag is disabled
    }                  
    
    // Currently selected sentence ID
    var sentenceID = $(".selected").prop("id").substr(1);  // chop prefix 's' from id
    var tagID = $(this).prop("id").substr(1); // chop prefix 't' from id
    var postID = getPostId();

    if(sentenceID && tagID &&  postID) { // valid post
      // Only post INSERT if tag is not already in the selected row's tags
      // AND only 
      if($('.selected .tagsSentence #t' + tagID).length == 0) {
        $(this).clone()
               .removeClass("tagBtn")
               .addClass("tagInstance")
               .click(function() { 
                 if($(this).hasClass("tagDisabled")) {
                   return; // skip if tag is disabled
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
  
  // Clicking on the 'Show/Hide Others Comments' button
  $('#othersComments').hide();  
  $('#othersCommentsDisplay').click(function() {
    $('#othersComments').toggle();
  });
  
  // Initially hide the Save Button
  $('#annotatorsCommentSave').addClass("invisible");

  // Annotators Comment Box
  // - This implements an automatic editably comment box.
  // $('#annotatorsComment textarea').toggleEdit({
  //   onpreview: function(event, ui) {
  //                // Save the updated Comment Box Value back to the server
  //                var postID = getPostId();
  //                annotatePostRequest(postID, ui.text);                 
  //                // log.val(log.val()+'onpreview triggered\n');
  //                $('#annotatorsCommentSave').addClass("invisible");
  //              },
  //   onedit: function() {
  //             // log.val(log.val()+'onedit triggered\n');
  //             $('#annotatorsCommentSave').removeClass("invisible");                 
  //           }
  // }); // $('#annotatorsComment textarea').toggleEdit
  
  // Implements a Comment Box with id='annotatorsComment' textarea
  $("#annotatorsCommentSave").click(function(event) {
	  // Save the updated Comment Box Value back to the server
	  var postID = getPostId();
	    annotatePostRequest(postID, $("#annotatorsComment").val());
  });

  // Implements a Comment Box with a input form
   // $("#annotatorsCommentSave").click(function() {
   //    // Save the updated Comment Box Value back to the server
   //    var postID = getPostId();
   //    annotatePostRequest(postID, $("#annotatorsComment").val());
   // });
  
  
  // -- (un)Finalize and (un)Flag --
  // Manage toggling the Finalize and the Problem Flagging buttons
  $(".initiallyHidden").toggle(false); // initially hidden


  // "PROBLEM" flag is disabled - chipp 25jan2011
  // $(".flagPostBtn").click(function() { // when a flagPostBtn is clicked
  //   $(".flagPostBtn").toggle(); // toggle *all* flagPostBtns
  // });

  $(".finalizePostBtn").click(function() { // when a finalizePostBtn is clicked
    // Check if the finalized button is disabled
    if($(this).hasClass("finalizedDisabled")) {
      return; // skip if tag is disabled
    }
    $(".finalizePostBtn").toggle(); // toggle *all* finalizePostBtns 
      });
  
  // -- Flag/Finalize Button actions --
  
  // "PROBLEM" flag is disabled - chipp 25jan2011
  // $('#flag').click(function() {
  //   var postID = getPostId();
  //   updatePostAnnotationStateRequest(postID, 'PROBLEM');
  //   $('#unfinalize').toggle(false); // enforce mutex to finalize state
  //   $('#finalize').toggle(true);
  // });
  // 
  // $('#unflag').click(function() {
  //   var postID = getPostId();
  //   updatePostAnnotationStateRequest(postID, 'IN_PROGRESS');
  // });
   
  $('#finalize').click(function() {
    // Check if the finalized button is disabled
    if($(this).hasClass("finalizedDisabled")) {
      return; // skip if tag is disabled
    }
    var postID = getPostId();
    
    if($(this).hasClass("adjudicatorPostBtn")) { // Finalize btn on Adjudication interface
      updatePostAnnotationStateRequest(postID, 'ADJUDICATED');
    } else { // Finalize btn on Annotator's interface
      updatePostAnnotationStateRequest(postID, 'DONE');
    }
    
    $('#unflag').toggle(false); // enforce mutex to flag state
    $('#flag').toggle(true);
    $(".tag").addClass("tagDisabled");
  });
  
  $('#unfinalize').click(function() {
    // Check if the finalized button is disabled
    if($(this).hasClass("finalizedDisabled")) {
      return; // skip if tag is disabled
    }
    var postID = getPostId();
    updatePostAnnotationStateRequest(postID, 'IN_PROGRESS');
    $(".tag").removeClass("tagDisabled");
  });
  
  if($('#finalize').hasClass("initiallyHidden")) {
    $(".tag").addClass("tagDisabled");
  }
  // Disable all tags if post is finalized (i.e., postState = ADJUDICATED)    
  if($('#finalize').hasClass("finalizedDisabled")) {
    $(".tag").addClass("tagDisabled");
  }
  if($('#unfinalize').hasClass("finalizedDisabled")) {
    $(".tag").addClass("tagDisabled");
  }
  
});