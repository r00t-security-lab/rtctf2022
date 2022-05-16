<?php
error_reporting (0);
$link = new mysqli('localhost','root','root','kano','3306');
// mysqli_set_charset($link, 'utf8');
if ($link->connect_error) {
    die("连接失败: " . $link->connect_error);
}
$ranking = "kano_rank";//排行榜表名
