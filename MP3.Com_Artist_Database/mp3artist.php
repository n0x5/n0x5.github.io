<?php
 $dir = 'sqlite:/home/coax/websites/secondsight/mp3com/mp3com.db';
 $dbh  = new PDO($dir, null, null, [PDO::SQLITE_ATTR_OPEN_FLAGS => PDO::SQLITE_OPEN_READONLY]) or die("cannot open the database");
$artist2 = $_GET["artist"];
$artist =  str_replace(' ', '%', $artist2);

$artisturl2 = $_GET["artisturl"];
$artisturl =  str_replace(' ', '%', $artisturl2);
 $query = "select * from dp_table where artist like '" . $artist . "' order by dated desc";
foreach ($dbh->query($query) as $row) {
echo '<div style="background-color:#f5f5f5;margin:2px;padding:1px;" class="track"><a href="' . $row[0] . '">' . $row[0] . '</a><div class="artist" style="font-size:17px;background-color:#f5f5f5;padding:3px;">' . $row[3] . ' | ' . $row[4] . '</div></div><br>';
}
?>