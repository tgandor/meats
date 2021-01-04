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
    unset($files[array_search('index.php', $files)]);
?><!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
<?php if(file_exists('bootstrap.min.css')): ?>
    <link rel="stylesheet" href="bootstrap.min.css">
<?php else: ?>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
<?php endif ?>

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

<?php if ($subfolders): ?>
            <div class="col-12">
                <h2>Subfolders</h2>
            </div>
    <?php foreach($subfolders as $i => $subfolder): ?>
            <div class="col-sm-6 col-md-4 col-lg-3 py-3 o-hidden">
                <h3><?php echo $i + 1; ?>.&nbsp;<a href="<?php echo $subfolder ?>"><?php echo $subfolder ?></a></h3>
            </div>
    <?php endforeach ?>
<?php endif ?>

<?php if ($files): ?>
            <div class="col-12">
                <h2>Files</h2>
            </div>
    <?php foreach($files as $i => $file): ?>
            <div class="col-sm-12 col-md-6 col-lg-4 o-hidden">
                <p><?php echo $i + 1; ?>.&nbsp;<a href="<?php echo $file ?>"><?php echo $file ?></a></p>
            </div>
    <?php endforeach ?>
<?php endif ?>

        </div>
    </div>
  </body>
</html>
