<?php

  //-----
  // tagsentence.php
  // created: 20-oct-2011/chipp
  //
  // web-service to tag sentences (called from tagpost.php's interface)
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
  require_once( $thisdirname . '/../Tag.php' );  
  require_once( $thisdirname . '/../Post.php' );  
  require_once( $thisdirname . '/../Sentence.php' );
  require_once( $thisdirname . '/../Queries.php' );
  require_once( $thisdirname . '/../Set.php' );
  
  $connectionObject = new Connection( $db_host, $db_user, $db_pass, $db_name );
  $db = $connectionObject->createDBObject();
  $qryObject = new Queries( $db );
  
  // Annotator's ID is the SESSION userid
  $annotatorID = $_SESSION['userid'];
  
  // Behavior differs upon REQUEST_METHOD:
  //   GET requests displays the HTML GUI
  //   POST requests insert/delete tagposts and display JSON responses
  switch($_SERVER['REQUEST_METHOD']) {
    case 'POST': 
      $clean = validate_post_args();
      if($clean['action'] == 'INSERT') {
        insert_sentencetag_to_db($qryObject, $annotatorID, $clean);        
      } else if($clean['action'] == 'DELETE') {
        delete_sentencetag_from_db($qryObject, $annotatorID, $clean);
      } else {
        die('invalid sentencetag action (INSERT or DELETE)');
      }
    break;
    // No PHP Request args avail. for HTTP DELETE requests
    // case 'DELETE': delete_tagpost_from_db($qryObject);
    // break;
  }  
} // end of valid session

/**
 * validate_post_args()
 *  
 * validates the POST request arguments
 *
 * @return array Cleaned arguments as keys in array
 * @author Chipp
 */
function validate_post_args() {
  $args = array(
    'action'     => FILTER_SANITIZE_STRING,
    'sentenceID' => FILTER_SANITIZE_NUMBER_INT,
    'tagID'      => FILTER_SANITIZE_NUMBER_INT,
    'postID'     => FILTER_SANITIZE_NUMBER_INT   
  );

  $clean = filter_input_array(INPUT_POST, $args) or die('invalid vars'); // POST args
  if(array_key_exists('action', $clean) and 
     array_key_exists('sentenceID', $clean) and 
     array_key_exists('tagID', $clean)      and 
     array_key_exists('postID', $clean)) { // POST request to submit a tag
    return $clean;
  } else {
    die('invalid tagpost arguments');
  }
} // end of validate_post_args() 

/**
 * inserts a sentence tag to the database
 *
 * @param Queries $qryObject database Queries object
 * @param int $annotatorID the id for the annotator
 * @param array $clean a cleaned array of args for sentencetag
 * @return void
 * @author Chipp
 */
function insert_sentencetag_to_db($qryObject, $annotatorID, $clean) {
  // $qryObject->insertSentenceTag( <$sentenceID>, <$tagID>, <$postID>, $annotatorID ); 
  $results = $qryObject->insertSentenceTag( $clean['sentenceID'], $clean['tagID'], $clean['postID'], $annotatorID ); 
  if($results) { // update the post's annotation tag count
    $results = $qryObject->updatePostAnnotation( $clean['postID'], $annotatorID ); 
  }
  echo json_encode(array('status' => $results ? "SUCCESS" : "ERROR",
                         'action' => $clean['action'],
                         'sentenceID' => $clean['sentenceID'],
                         'tagID' => $clean['tagID'], 
                         'postID' => $clean['postID']));
} // end of post_sentencetag_to_db

/**
 * delete specified sentencetag from the database
 *
 * @param Queries $qryObject database Queries object
 * @param int $annotatorID the id for the annotator
 * @param array $clean a cleaned array of args for sentencetag
 * @return void
 * @author Chipp
 */
function delete_sentencetag_from_db($qryObject, $annotatorID, $clean) {
  $results = $qryObject->deleteSentenceTag( $clean['sentenceID'], $clean['tagID'], $clean['postID'], $annotatorID ); 
  if($results) { // update the post's annotation tag count
    $results = $qryObject->updatePostAnnotation( $clean['postID'], $annotatorID ); 
  }
  echo json_encode(array('status' => $results ? "SUCCESS" : "ERROR", 
                         'action' => $clean['action'],
                         'sentenceID' => $clean['sentenceID'],
                         'tagID' => $clean['tagID'], 
                         'postID' => $clean['postID']));
} // end of delete_sentencetag_from_db

?>
