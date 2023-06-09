<?php
// 接受图片信息并且保存
header("Access-Control-Allow-Origin:*");
$imge=$_POST["img"];
$s3=explode(',', $imge, 2);
$img2=$s3[1];
$img2= str_replace(PHP_EOL, '', $img2);
// var_dump($img2);
function imgToBase64($img_file) {

    $img_base64 = '';
    if (file_exists($img_file)) {
        $app_img_file = $img_file; // 图片路径
        $img_info = getimagesize($app_img_file); // 取得图片的大小，类型等

        //echo '<pre>' . print_r($img_info, true) . '</pre><br>';
        $fp = fopen($app_img_file, "r"); // 图片是否可读权限

        if ($fp) {
            $filesize = filesize($app_img_file);
            $content = fread($fp, $filesize);
            $file_content = chunk_split(base64_encode($content)); // base64编码
            switch ($img_info[2]) {           //判读图片类型
                case 1: $img_type = "gif";
                    break;
                case 2: $img_type = "jpg";
                    break;
                case 3: $img_type = "png";
                    break;
            }
          // $img_base64 = 'data:image/' . $img_type . ';base64,' . $file_content;//
            $img_base64 =$file_content;//合成图片的base64编码

        }
        fclose($fp);
    }

    return $img_base64; //返回图片的base64
}


//调用使用的方法
$img_dir = dirname(__FILE__) . '/images/1.jpg';
$img_base64 = imgToBase64($img_dir);
// echo '<img src="' . $img_base64 . '">';       //图片形式展示
// echo '<hr>';
// print_r(explode(',', $img_base64, 2));
// $s=explode(',', $img_base64, 2);
// $img1=$s[1];
//echo $s[0];
//echo $s[1];
//echo $img_base64;
$img_base64= str_replace(PHP_EOL, '', $img_base64);
// var_dump($img_base64);

function request_post($url = '', $param = '')
{
    if (empty($url) || empty($param)) {
        return false;
    }

    $postUrl = $url;
    $curlPost = $param;
    // 初始化curl
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $postUrl);
    curl_setopt($curl, CURLOPT_HEADER, 0);
    // 要求结果为字符串且输出到屏幕上
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    // post提交方式
    curl_setopt($curl, CURLOPT_POST, 1);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $curlPost);
    // 运行curl
    $data = curl_exec($curl);
    curl_close($curl);

    return $data;
}

$token = '24.cc3d42bee5bafc3ac5a4b240d3b9bc10.2592000.1594299144.282335-20278086';
$url = 'https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=' . $token;

$bodys = "[{\"image\": \"{$img_base64}\", \"image_type\": \"BASE64\", \"face_type\": \"LIVE\", \"quality_control\": \"LOW\"},
 {\"image\": \"{$img2}\", \"image_type\": \"BASE64\", \"face_type\": \"IDCARD\", \"quality_control\": \"LOW\"}]";
$res = request_post($url, $bodys);
// var_dump($bodys);
// var_dump($res);
$s2=json_decode($res,true);
// var_dump($s2);
if($s2['result']['score']>80){
	// $result=1; 
    $list=1;
    echo json_encode($list);
}else{
	// $result=0;
    $list=0;
    echo json_encode($list);
};

?>