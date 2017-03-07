<?php

  //-----
  // annotatepost.php
  // created: 15-jun-2011/chipp
  //
  // update a post's annotation (comments) by annotatorID
  //-----

?>

<?php

// make sure we have a valid session
session_start();
if ( ! isset( $_SESSION['userid'] ) ||
     ! isset( $_SESSION['username'] ) ||
     ! isset( $_SESSION['usertype'] )) {
  echo "SESSION ERROR<br />";
  echo "<a href=\"index.php\">please connect again.</a>";
}
else { // valid session
  
  // initialize connection to database
  $thisdirname = dirname(__FILE__);
  require_once( $thisdirname . '/../globals.php' );
  require_once( $thisdirname . '/../Connection.php' );
  require_once( $thisdirname . '/../Sentence.php' );
  require_once( $thisdirname . '/../Queries.php' );
  $connectionObject = new Connection( $db_host, $db_user, $db_pass, $db_name );
  $db = $connectionObject->createDBObject();
  $qryObject = new Queries( $db );
  
  // Annotator's ID is the SESSION userid
  $annotatorID = $_SESSION['userid'];
  
  if($_SERVER['REQUEST_METHOD'] == 'POST') { // only allow POST requests
    $clean = validate_post_args();
    // Update posts_annotators table
    $results = $qryObject->updatePostAnnotation( $clean['postID'], $annotatorID, $clean['comment'], $clean['state'] );
    echo json_encode(array(
      'status' => $results ? "SUCCESS" : "ERROR",
      'postID' => $clean['postID']
    ));
  }
} // end valid session

/**
 * validate_post_args()
 *  
 * validates the POST request arguments
 *
 * @return array cleaned arguements as keys in array
 * @author Chipp
 */
function validate_post_args() {
  $args = array(
    'comment' => FILTER_SANITIZE_STRING,
    'postID'  => FILTER_SANITIZE_NUMBER_INT,
    'state' => FILTER_SANITIZE_STRING
  );

  $clean = filter_input_array(INPUT_POST, $args) or die('invalid vars'); // POST args
  if(!array_key_exists('comment', $clean)) {
    $clean['comment'] = null;
  }
  if(!array_key_exists('state', $clean)) {
    $clean['state'] = null;
  }  
  if(array_key_exists('postID', $clean)) { // all required args exist
    return $clean;
  } else {
    die('invalid annotatepost arguements');
  }
} // end of validate_post_args()

?>
