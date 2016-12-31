<h1> Pliki do pobrania </h1>

<?php foreach ( glob('*.*') as $fn ): ?>
	<? if($fn != 'index.php'):?>
		<a href="<?=urlencode($fn)?>"><?=htmlspecialchars($fn)?></a> <br />
	<? endif; ?>
<?php endforeach; ?>

