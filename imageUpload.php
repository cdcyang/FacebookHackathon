<?php
if(!isset($_FILES)){
    $error = 0;
    $upload_dir = "uploads/";
    $fileName = $_FILES['imageToUpload']['name'];
    $uploaded_file = $upload_dir.$fileName;
    if(move_uploaded_file($_FILES['imageToUpload']['tmp_name'],$uploaded_file)){
//insert file information into db table
        //$mysql_insert = "INSERT INTO uploads (file_name, upload_time)VALUES('".$fileName."','".date("Y-m-d H:i:s")."')";
        //mysqli_query($conn, $mysql_insert) or die("database error:". mysqli_error($conn));
    }
}
?>