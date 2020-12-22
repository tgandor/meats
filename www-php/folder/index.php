<?php
    $title = basename(dirname($_SERVER['PHP_SELF']));
    $crumbs = array();
    $path = '';
    foreach(explode('/', dirname($_SERVER['SCRIPT_NAME'])) as $dir)
    {
        $path .= "$dir/";
        $crumbs[$path] = $dir;
    }
    $subfolders = glob('*', GLOB_ONLYDIR);
    $files = array_values(array_diff(glob('*'), $subfolders));
?><!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">

    <style>
    .container {
        width: auto;
        max-width: 1600px;
        padding: 0 15px;
    }
    .o-hidden {
        overflow: hidden;
    }
    </style>

    <title><?php echo $title ?> - Folder listing</title>
  </head>

  <body>
    <div class="container">
        <div class="jumbotron d-none d-md-block">
            <h1><?php echo $title ?></h1>
            <p class="lead">Folder listing</p>
        </div>

        <div class="page-header d-block d-md-none">
            <h1><?php echo $title ?></h1>
        </div>

        <div class="row">
            <div class="col-12">
                <p>
                    Path:
                    <?php foreach($crumbs as $path => $dir): ?>
                    / <a href="<?php echo $path ?>"><?php echo $dir ?: '&#8962;'  ?></a>
                    <?php endforeach ?>
                </p>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <h2>Subfolders</h2>
            </div>
        <?php foreach($subfolders as $i => $subfolder): ?>
            <div class="col-sm-6 col-md-4 col-lg-3 py-3 o-hidden">
                <h3><?php echo $i + 1; ?>.&nbsp;<a href="<?php echo $subfolder ?>"><?php echo $subfolder ?></a></h3>
            </div>
        <?php endforeach ?>
            <div class="col-12">
                <h2>Files</h2>
            </div>
        <?php foreach($files as $i => $file): ?>
            <div class="col-sm-12 col-md-6 col-lg-4 o-hidden">
                <p><?php echo $i + 1; ?>.&nbsp;<a href="<?php echo $file ?>"><?php echo $file ?></a></p>
            </div>
        <?php endforeach ?>
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
  </body>
</html>
