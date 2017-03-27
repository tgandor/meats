<!DOCTYPE HTML>
<!--
	Fractal by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title><?php echo dirname($_SERVER['PHP_SELF']) ?> - Music Folder</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
		<!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
	</head>
	<body id="top">

		<!-- Header -->
			<header id="header">
				<div class="content">
					<h1><a href="#"><?php echo dirname($_SERVER['PHP_SELF']) ?></a></h1>
					<p>Listing music files in folder, choose your action:</p>
					<ul class="actions">
						<li><a href="#download" class="button special icon fa-download">Download</a></li>
						<li><a href="#listen" class="button icon fa-chevron-down scrolly">Listen</a></li>
					</ul>
					<p></p>
					<p>Layout is &quot;Fractal&quot;: Just a simple, single page responsive<br />
					template brought to you by <a href="http://html5up.net">HTML5 UP</a></p>
				</div>
				<div class="image phone"><div class="inner"><img src="images/screen.jpg" alt="" /></div></div>
			</header>

		<!-- One -->
			<section id="listen" class="wrapper style2 special">
				<header class="major">
					<h2>Music listing:</h2>
				</header>
				<div class="inner">
				<section>
					<div class="table-wrapper">
						<table>
							<thead>
								<tr>
									<th>Track #</th>
									<th>Filename</th>
									<th>Play</th>
								</tr>
							</thead>
							<tbody>
				<?php foreach(glob('*.mp3') as $i => $music_file): ?>
								<tr>
									<td><?php echo $i + 1; ?></td>
									<td><?php echo $music_file ?></td>
									<td>
										<audio controls>
											<source src="<?php echo $music_file ?>" type="audio/mpeg">
											<!-- <source src="<?php echo $music_file ?>.ogg" type="audio/ogg"> -->
											Your browser does not support the audio element.
										</audio>
									</td>
								</tr>
				<?php endforeach?>
							</tbody>
						</table>
					</div>
				</section>
				</div>
				<div class="content">
					<ul class="actions">
						<li><a href="#header" class="button icon fa-chevron-up scrolly">Back</a></li>
					</ul>
\				</div>
			</section>


		<!-- Two -->
			<section id="download" class="wrapper style2 special">
				<div class="inner">
				<header class="major">
					<h2>Download links:</h2>
				</header>

				<section>
					<div class="table-wrapper">
						<table class="alt">
							<thead>
								<tr>
									<th>Track #</th>
									<th>Filename</th>
								</tr>
							</thead>
							<tbody>
				<?php foreach(glob('*.mp3') as $i => $music_file): ?>
								<tr>
									<td><?php echo $i + 1; ?></td>
									<td><a href="<?php echo $music_file ?>"><?php echo $music_file ?></a></td>
								</tr>
				<?php endforeach?>

							</tbody>
						</table>
					</div>
				</section>
				</div>
				<div class="content">
					<ul class="actions">
						<li><a href="#header" class="button icon fa-chevron-up scrolly">Back</a></li>
					</ul>
\				</div>
			</section>

		<!-- Footer -->
			<footer id="footer">
				<ul class="icons">
					<li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>
					<li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
					<li><a href="#" class="icon fa-instagram"><span class="label">Instagram</span></a></li>
				</ul>
				<p class="copyright">&copy; Meats. Credits: <a href="http://html5up.net">HTML5 UP</a></p>
			</footer>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="assets/js/main.js"></script>

	</body>
</html>