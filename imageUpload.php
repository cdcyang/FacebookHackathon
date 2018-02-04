<?php
if(isset($_POST['submit'])) {

    $files = glob('uploads/*.*');
    foreach($files as $file) {
        if(is_file($file)) {
            unlink($file);
        }
    }

    $url = "www.kieranbrown.me/facebook/uploads/";
    $error = 0;
    //print_r($FILES['imageToUpload']);
    $upload_dir = getcwd() . "\\uploads\\";
    $fileName = $_FILES['imageToUpload']['name'];
    $uploaded_file = $upload_dir . $fileName;
    $pythonDirectory = "/uploads/".$fileName;

    if(file_exists($uploaded_file)) {
        $error = 1;
    }

    if($_FILE["imageToUpload"]["size"] > 2500000) {
        $error = 1;
    }

    if (move_uploaded_file($_FILES['imageToUpload']['tmp_name'], $uploaded_file) && $error == 0) {
        echo "<script>console.log('File uploaded')</script>";
        ?>
        <html>
        <head>
            <script src="js/jquery-3.3.1.min.js"></script>
            <script>
                function getAjax() {
                    $.ajax({
                        type: "GET",
                        url: "http://127.0.0.1:5000/",
                        crossOrigin: true,
                        data: {
                            file: "<?= $pythonDirectory ?>"
                        },
                        success: function (output) {
                            var caption;
                            var hashtags = new Array(10);

                            caption = output['caption'];
                            for(int i = 0; i < output['hashtag'].length; i++) {
                                hashtags[i] = output['hashtag'][i];
                            }

                            var hashtagOutput = "";
                            hashtags.forEach(function(val) {
                                hashtagOutput += val;
                            })

                            console.log("caption":  + caption)
                            console.log("hashtags: " + hashtagOutput)
                        }
                    });
                }

                var output = getAjax();

            </script>
        </head>
        </html>
        <?php
    } else {
        echo "<script>console.log('File not uploaded')</script>";
    }
    ?>
<?php
} else {
    echo "error";
}
?>
