<title> MP3.COM Archive.org Artist Database</title>
<body style="width:600px;">
<h1> MP3.COM Archive.org Artist Database</h1>
<?php
$file = fopen("filecount.txt", "r");

//Output lines until EOF is reached
while(! feof($file)) {
  $line = fgets($file);
  echo $line. " files parsed";
}

fclose($file);
?>
<h2>
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=a">a</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=b">b</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=c">c</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=d">d</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=e">e</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=f">f</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=g">g</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=h">h</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=i">i</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=j">j</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=k">k</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=l">l</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=m">m</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=n">n</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=o">o</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=p">p</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=q">q</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=r">r</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=s">s</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=t">t</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=u">u</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=v">v</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=w">w</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=x">x</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=y">y</a> |
<a style="padding-left: 5px;padding-right:5px;" href="https://secondsight.dev/mp3com/mp3letter.php?letter=z">z</a> |
</h2>
<form action="search.php" method="get">
  <label for="artist">Search artist name</label>
  <input type="text" name="artist">
  <input type="submit" value="Submit">
</form>
<form action="search1.php" method="get">
  <label for="artist">Search MP3.com url</label>
  <input type="text" name="artist">
  <input type="submit" value="Submit">
</form>

<?php
 $dir = 'sqlite:/home/coax/websites/secondsight/mp3com/mp3com.db';
 $dbh  = new PDO($dir, null, null, [PDO::SQLITE_ATTR_OPEN_FLAGS => PDO::SQLITE_OPEN_READONLY]) or die("cannot open the database");
 $query = "select * from dp_table order by dated desc limit 5000";
foreach ($dbh->query($query) as $row) {
echo '<div style="background-color:#f5f5f5;margin:2px;padding:1px;" class="track"><a style="color:#ad0000;" href="' . $row[0] . '">' . $row[0] . '</a><div class="artist" style="font-size:17px;background-color:#f5f5f5;padding:3px;">' . '<a href="mp3artist.php?artist=' . $row[3] .'&?artisturl=' . $row[4] . '">' . $row[3] . '</a>' . ' | ' . $row[4] . ' | ' . $row[5] . '</div></div><br>';
}
?>
</body>
