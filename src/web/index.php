<?php
$config_file = file_get_contents("db/config.json");
$config = json_decode($config_file, true);
error_reporting(E_ERROR | E_PARSE);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
ini_set('max_execution_time', 300);


define('OAUTH2_CLIENT_ID', $config["oauth2_client_id"]);
define('OAUTH2_CLIENT_SECRET', $config["oauth2_client_secret"]);

$authorizeURL = 'https://discord.com/api/oauth2/authorize';
$tokenURL = 'https://discord.com/api/oauth2/token';
$apiURLBase = 'https://discord.com/api/users/@me';
$revokeURL = 'https://discord.com/api/oauth2/token/revoke';

session_start();

if($_GET['action'] == 'logout') {
    session_destroy();
    unset($_SESSION['access_token']);
    header('Location: ' . $_SERVER['PHP_SELF']);
    die();
}

if(get('action') == 'login') {
  $params = array(
    'client_id' => OAUTH2_CLIENT_ID,
    'redirect_uri' => $config["redirect_uri"],
    'response_type' => 'code',
    'scope' => 'identify guilds'
  );

  header('Location: https://discord.com/api/oauth2/authorize' . '?' . http_build_query($params));
  die();
}







function join_guild($bot_token,$user_id, $server_id){
  $bot = array(
    "Authorization: Bot $bot_token",                                                                          
    'Content-Type: application/json');                                                                       
  $url = "https://discord.com/api/v9/guilds/$server_id/members/$user_id";
  $myArr = array("access_token" => $_SESSION['access_token']);
  $data_string = json_encode($myArr);
  $ch = curl_init($url);                                                                     
  curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");                                                                    
  curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);                                                                  
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);                                                                      
  curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    "Authorization: Bot $bot_token",                                                                          
    'Content-Type: application/json')
  );                                                                                                                 

  $exec = curl_exec($ch);
  return;
}

if($_GET["action"] == "join"){
  die();
}

if(get('code')) {
  $_SESSION["code"] = get('code');
  $token = apiRequest($tokenURL, array(
    "grant_type" => "authorization_code",
    'client_id' => OAUTH2_CLIENT_ID,
    'client_secret' => OAUTH2_CLIENT_SECRET,
    'redirect_uri' => $config["redirect_uri"],
    'code' => get('code')
  ));
  
  $logout_token = $token->access_token;
  $_SESSION['access_token'] = $token->access_token;


  header('Location: ' . $_SERVER['PHP_SELF']);
}


if($_GET["action"] == "code"){
  $params = array(
    'client_id' => OAUTH2_CLIENT_ID,
    'redirect_uri' => $config["redirect_uri"],
    'response_type' => 'code',
    'scope' => 'identify guilds guilds.join'
  );

  header('Location: https://discord.com/api/guilds/?' . http_build_query($params));
  die();
}
if($_SESSION['access_token']) {
    $user = apiRequest($apiURLBase);

    require "db/database.php";
    $stmt = $odb->prepare("SELECT * FROM users WHERE discord_id=?");
    $stmt->execute([ $user->id ]);
    $value = $stmt->fetch();

    function generateRandomString($length = 6) {
        $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $charactersLength = strlen($characters);
        $randomString = '';
        for ($i = 0; $i < $length; $i++) {
            $randomString .= $characters[rand(0, $charactersLength - 1)];
        }
        return $randomString;
    }

?>

    <html lang="en"><head>
        <meta charset="utf-8">
        <title>Auth API</title>
        <meta name="description" content="Ani">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="assets/css/style.css">
    </head>
    <body>
    <section id="content">
        <div class="row">
            <div class="card" style="height: 78px;">
                <img src="https://cdn.discordapp.com/avatars/<?=$user->id?>/<?=$user->avatar?>.png?size=80" style="bottom: 95px;" id="logoimage">
                <div id="text">
                    
                    <a><?=$user->username?></a>
                    <br>
                    
            </div>
            <?php
            $code = generateRandomString();
            if(!$value["auth_key"]){
                $avatar = "https://cdn.discordapp.com/avatars/".$user->id."/".$user->avatar.".png?size=80";
                $sql = "INSERT INTO users (name, auth_key, avatar_url, discord_id, dc_code) VALUES (?,?,?,?,?)";
                $stmt= $odb->prepare($sql);
                $stmt->execute([$user->username, $code, $avatar, $user->id, $_SESSION["code"]]);
                echo "<a>Your Key:<a style='color: #fff; font-weight: bold; float:left'>".$code."</a></a>";
                join_guild($config['BotToken'],$user->id,$config['server_id']);

            } else {
                join_guild($config['BotToken'],$user->id,$config['server_id']);
                echo "<a>Your Key:<a style='color: #fff; font-weight: bold; float:left'>".$value["auth_key"]."</a></a>";
                
            }
            ?>
                <button type="button" onclick="window.location.href='?action=logout'" id="b" class="btn btn-default btn-sm">
                <span class="glyphicon glyphicon-log-out"></span> Log out
                </button>
        </div>                                        
            </div>
        </section>
    </body></html>
<?php
} else {
    $params = array(
        'client_id' => OAUTH2_CLIENT_ID,
        'redirect_uri' => $config["redirect_uri"],
        'response_type' => 'code',
        'scope' => 'identify guilds guilds.join'
      );
    
      header('Location: https://discord.com/api/oauth2/authorize' . '?' . http_build_query($params));
      die();
}



function apiRequest($url, $post=FALSE, $headers=array()) {
  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);

  $response = curl_exec($ch);


  if($post)
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post));

  $headers[] = 'Accept: application/json';

  if(session('access_token'))
    $headers[] = 'Authorization: Bearer ' . session('access_token');

  curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

  $response = curl_exec($ch);
  return json_decode($response);
}

function logout($url, $data=array()) {
    $ch = curl_init($url);
    curl_setopt_array($ch, array(
        CURLOPT_POST => TRUE,
        CURLOPT_RETURNTRANSFER => TRUE,
        CURLOPT_IPRESOLVE => CURL_IPRESOLVE_V4,
        CURLOPT_HTTPHEADER => array('Content-Type: application/x-www-form-urlencoded'),
        CURLOPT_POSTFIELDS => http_build_query($data),
    ));
    $response = curl_exec($ch);
    return json_decode($response);
}

function get($key, $default=NULL) {
  return array_key_exists($key, $_GET) ? $_GET[$key] : $default;
}

function session($key, $default=NULL) {
  return array_key_exists($key, $_SESSION) ? $_SESSION[$key] : $default;
}

?>