<?php
    $version = "v1.1-ii-2025.07.09";
    $title = basename(dirname($_SERVER['PHP_SELF']));
    if (empty($title)) {
        $title = 'Image Index';
    }
    // jpg and png
    $files = glob('*.[JjPp][PpNn][Gg]');
    natsort($files);
    $subfolders = glob('*', GLOB_ONLYDIR);
    $crumbs = array();
    $path = '';
    foreach(explode('/', dirname($_SERVER['SCRIPT_NAME'])) as $dir)
    {
        $path .= "$dir/";
        $crumbs[$path] = $dir;
    }
    $bs = 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css';
    if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/bootstrap.min.css'))
        $bs = '/bootstrap.min.css';
    elseif (file_exists('bootstrap.min.css'))
        $bs = 'bootstrap.min.css';
?><!doctype html>
<html lang="en">
  <head>
    <title><?php echo $title ?> - Image Index</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="<?php echo $bs ?>"
        integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4"
        crossorigin="anonymous">

    <style>
    .container {
        width: auto;
        max-width: 1280px;
        padding: 0 15px;
    }
    </style>
  </head>

  <body>
    <div class="container">
        <div class="jumbotron d-none d-md-block">
            <h1><?php echo $title ?></h1>
            <p class="lead" title="<?php echo $version ?>">Pictures in folder.</p>
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
<?php foreach($files as $i => $img): ?>
            <div class="col-sm-12 col-md-6 col-lg-4 py-3">
                <p><?php echo $i + 1 ?>. <a href="<?php echo $img ?>"><?php echo $img ?></a></p>
                <a href="<?php echo $img ?>">
                    <img src="<?php echo $img ?>" style="width: 100%;" alt="<?php echo $img ?>" title="<?php echo $img ?>" loading="lazy">
                </a>
            </div>
<?php endforeach ?>

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

<?php if(count($files) > 10): ?>
            <div class="col-12">
                <p>
                    Path:
<?php foreach($crumbs as $path => $dir): ?>
                    / <a href="<?php echo $path ?>"><?php echo $dir ?: '&#8962;'  ?></a>
<?php endforeach ?>
                </p>
            </div>
<?php endif ?>
        </div>
    </div>
  </body>
</html>
