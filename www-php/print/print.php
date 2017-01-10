<?php

session_start();

if (isset($_POST['to_print']))
{
    file_put_contents('/tmp/print.txt', wordwrap($_POST['to_print']));
    system('lp /tmp/print.txt');
    unlink('/tmp/print.txt');
    $_SESSION['last_printed'] = $_POST['to_print'];
    header("Location: $_SERVER[PHP_SELF]?printed=1");
    die;
}

$printed = isset($_GET['printed']);

?><!DOCTYPE html>
<html>
<head>
<title>Printing form</title>
</head>

<body>
<h1>Online printing form</h1>
<?php if($printed): ?>
<p style="color: blue">This has been just printed:</p>
<?php endif ?>
<form action="<?php echo $_SERVER['PHP_SELF'] ?>" method="post">
<div>
<button type="button" onclick="document.getElementById('to_print').select()">Select all</button>
</div>
<div>
<textarea rows="20" cols="80" id="to_print" name="to_print"><?php if (!$printed): ?>Enter or paste text to print...
<?php else: ?><?php echo $_SESSION['last_printed'] ?>
<?php endif ?>
</textarea>
</div>
<div>
<input type="submit" value="Print<?php if ($printed): ?> (again)<?php endif ?>" />
</div>
</form>
</body>

</html>
