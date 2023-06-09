
	<?php
	  require './config.php';

      if($_POST){echo "用户名或密码错误";
        $link=mysqli_connect($host,$user,$password,$dbname);
        if(!$link){
           display ('数据库连接失败。' . mysqli_connect_error());
        }
        mysqli_set_charset($link, 'utf8');
        $fields=['name','password'];
        $data=[];
        foreach ($fields as $k) {
            $data[$k]= isset($_POST[$k])?$_POST[$k]:'';
        }
        foreach ($data as $k => $v) {
            $data[$k]=mysqli_real_escape_string($link,$v);
        }
        $query=mysqli_query($link,"select * from `user` where `user_account` ='{$data['name']}' and `user_password` ='{$data['password']}'");
        if(!mysqli_num_rows($query)){
            
    
        }else{
            $_SESSION['user'] = $data['name'];
            header('Location:./faceRecognition.php');
            exit;
        }
      }
      display();
      function display($message =null){
        require './html/login.html';
        exit;
        
      }
	  


// $token = '24.cc3d42bee5bafc3ac5a4b240d3b9bc10.2592000.1594299144.282335-20278086';
// $url = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/get?access_token=' . $token;
// $bodys = "{\"user_id\":\"user1\",\"group_id\":\"group1\"}";
// $res = request_post($url, $bodys);

// var_dump($res);
// function request_post($url = '', $param = '')
// {
//     if (empty($url) || empty($param)) {
//         return false;
//     }

//     $postUrl = $url;
//     $curlPost = $param;
//     // 初始化curl
//     $curl = curl_init();
//     curl_setopt($curl, CURLOPT_URL, $postUrl);
//     curl_setopt($curl, CURLOPT_HEADER, 0);
//     // 要求结果为字符串且输出到屏幕上
//     curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
//     curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
//     // post提交方式
//     curl_setopt($curl, CURLOPT_POST, 1);
//     curl_setopt($curl, CURLOPT_POSTFIELDS, $curlPost);
//     // 运行curl
//     $data = curl_exec($curl);
//     curl_close($curl);

//     return $data;
// }  
?>
