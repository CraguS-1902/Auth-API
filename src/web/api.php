<?php
require "db/database.php";
$key = $_GET["key"];
$stmt = $odb->prepare("SELECT * FROM users WHERE auth_key=?");
$stmt->execute([ $key ]);
$value = $stmt->fetch();
?>

<html lang="en"><head>
    <meta charset="utf-8">
    <title>USER API</title>
    <meta name="description" content="Ani">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<section id="content">
    <div class="row">
        <div class="card" style="width: 38rem;">
        <?php
        if(!$value){
            echo "    <img style='width: 80px; height: 80px;' src='https://www.freeiconspng.com/thumbs/error-icon/error-icon-4.png' id='logoimage'>";
            echo "    <div id='text'>";
            echo "        <a>User not found</a>";
            echo "</div>";
            die();
        }
        ?>
            <img src="<?=$value["avatar_url"]?>" id="logoimage">
            <div id="text">
                <a><?=$value["name"]?></a>
        </div>
    </div>                                        
        </div>
    </section>
</body></html>

