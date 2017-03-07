/**
 * sassign.js
 * created: 27-jun-2011/chipp
 *
 * Corresponds with the 'sassign.php' page, and facilitates assocaiting
 * user annotators with particular post Sets
 * 
 * @author chipp
 */
$(document).ready(function() {
  
  /**
   * Makes a AJAX request to the server (ajax/set.php) add or remove a 
   * particular annotator to a post set
   * 
   * @param {string} actionType Possible actions 'INSERT', 'DELETE'
   * @param {integer} annotatorID Annotator (user) ID
   * @param {integer} setID Set ID
   */  
   var annotatorsSetRequest = function (actionType, annotatorID, setID) {
    var jqxhr = $.ajax({
      type: 'POST',
      url: "ajax/set.php",
      data: { action: actionType, annotatorID: annotatorID, setID: setID } 
    })
    .success(function(data) { 
       console.log("annotatorsSetRequest: " + data); }) 
    .error(function() { 
       console.log("Error posting annotatorID: " + annotatorID + 
                                       "setID: " + setID);
    });
  } // function annotatorsSetRequest

  // Attach Delete Tag Instance Behavior to initially loaded Sentences Tags
  $(".annotatorInstance").click(function() {
    var setID = $(this).parent().parent().prop("id").substr(1);  // chop prefix 's' from id
    var annotatorID = $(this).prop("id").substr(1); // chop prefix 't' from id
    annotatorsSetRequest('DELETE',  annotatorID, setID);
    $(this).remove();
  });

  // Annotator Button Behavior 
  $(".annotatorBtn").click(function() {
    // Currently selected sentence ID
    var setID = $(".selected").prop("id").substr(1);  // chop prefix 's' from id
    var annotatorID = $(this).prop("id").substr(1); // chop prefix 't' from id

    if(setID && annotatorID) { // valid set
      // only post INSERT if tag is not already in the selected row's tags
      if($('.selected #a' + annotatorID).length == 0) {
        $(this).clone()
               .removeClass("annotatorBtn")
               .addClass("annotatorInstance")
               .click(function() { 
                 annotatorsSetRequest('DELETE', annotatorID, setID);
                 $(this).remove();
               })
               .appendTo(".selected .annotatorsSets");
        annotatorsSetRequest('INSERT',  annotatorID, setID); 
      }
    } 
  });
  
  // Selecting only one set row
  $(".setRow").click(function() {
    $(".setRow").removeClass("selected"); // clear other selected row
    $(this).addClass("selected");
  });
});