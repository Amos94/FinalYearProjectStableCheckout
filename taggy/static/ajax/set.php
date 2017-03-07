<?php
  //-----
  // sassign.php
  // created: 20-jun-2011/sklar
  //
  // lets user assign through sets
  //-----

// make sure we have a valid session
session_start();
if ( ! isset( $_SESSION['userid'] ) ||
     ! isset( $_SESSION['username'] ) ||
     ! isset( $_SESSION['usertype'] )) {
  echo "SESSION ERROR<br />";
  echo "<a href=\"index.php\">please connect again.</a>";
}
else {
  // initialize connection to database
  $thisdirname = dirname(__FILE__);
  require_once( $thisdirname . '/../globals.php' );
  require_once( $thisdirname . '/../Connection.php' );
  require_once( $thisdirname . '/../Queries.php' );
  $connectionObject = new Connection( $db_host, $db_user, $db_pass, $db_name );
  $db = $connectionObject->createDBObject();
  $qryObject = new Queries( $db );
  
  // POST Handler
  if( $_SERVER['REQUEST_METHOD'] == 'POST' ) { 
    $clean = validate_post_args();
    try {      
      if( isset($clean['action']) &&
          isset($clean['annotatorID']) &&
          isset($clean['setID']) ) {
        switch($clean['action']) {
          case 'INSERT':
            if( !$qryObject->insertAnnotatorsSets( $clean['annotatorID'], $clean['setID'] ) ) {
              throw new Exception('Unable to insert annotatorID: ' . $clean['annotatorID'] . ' setID: ' . $clean['setID']); 
            }
            echo json_encode(array('status' => "SUCCESS",
                                   'action' => $clean['action'],
                                   'annotatorID' => $clean['annotatorID'],
                                   'setID' => $clean['setID'],
                                   'msg' => "Successfully assigned set " . $clean['setID']));
          break;
          case 'DELETE':
            if( !$qryObject->deleteAnnotatorsSets( $clean['annotatorID'], $clean['setID'] ) ) {
              throw new Exception('Unable to delete annotatorID: ' . $clean['annotatorID'] . ' setID: ' . $clean['setID']); 
            }
            echo json_encode(array('status' => "SUCCESS",
                                   'action' => $clean['action'],
                                   'annotatorID' => $clean['annotatorID'],
                                   'setID' => $clean['setID'],
                                   'msg' => "Successfully unassigned annotator " . $clean['annotatorID']));
          break;
        } // switch action
      } // valid args      
    }
    catch (Exception $e) { // catch Error
      echo json_encode(array('status' => "ERROR",
                             'action' => $clean['action'],
                             'annotatorID' => $clean['annotatorID'],
                             'setID' => $clean['setID'],
                             'msg' => $e->getMessage()));
    }
  } // end of POST handler
} // end of valid sesssion

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
    'annotatorID' => FILTER_SANITIZE_NUMBER_INT,
    'setID'       => FILTER_SANITIZE_NUMBER_INT,
    'action'      => FILTER_SANITIZE_STRING,
  );

  $clean = filter_input_array(INPUT_POST, $args) or die('invalid vars'); // POST args
  return $clean;
} // end of validate_post_args()

?>
