<form action="search.php" method="get">
  <label for="artist">Search MP3.com URL</label>
  <input type="text" name="artist">
  <input type="submit" value="Submit">
</form>



<?php
 $dir = 'sqlite:/home/coax/websites/secondsight/mp3com/mp3com.db';
 $dbh  = new PDO($dir, null, null, [PDO::SQLITE_ATTR_OPEN_FLAGS => PDO::SQLITE_OPEN_READONLY]) or die("cannot open the database");
$artist2 = $_GET["artist"];
$artist =  str_replace(' ', '%', $artist2);

 $query = "select * from dp_table where comment like '%" . $artist . "%' order by dated desc";
foreach ($dbh->query($query) as $row) {
echo '<div style="background-color:#f5f5f5;margin:2px;padding:1px;" class="track"><a style="color:#ad0000;" href="' . $row[0] . '">' . $row[0] . '</a><div class="artist" style="font-size:17px;background-color:#f5f5f5;padding:3px;">' . '<a href="mp3artist.php?artist=' . $row[3] .'&?artisturl=' . $row[4] . '">' . $row[3] . '</a>' . ' | ' . $row[4] . ' | ' . $row[5] . '</div></div><br>';
}
?>
