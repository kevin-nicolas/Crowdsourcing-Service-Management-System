<?php
	  require './config.php';	        
      // if($_POST){
        $link = mysqli_connect($host, $user, $password, $dbname);
        if(!$link){
        	display('数据库连接失败'.mysql_connect_error());
        }
        mysqli_set_charset($link, 'utf8');
        $fields=['working_hours1','working_hour2','working_area','professional_status','professional_direction','specific_professional','work_experience','education_experience','real_name','Id_card'];

        $data=[];
        foreach ($fields as $v) {
        	$data[$v] = isset($_POST[$v]) ? $_POST[$v] : '';      
        }
		
        // if (is_array($data['item_detail'])) {
        //   $data['item_detail'] = implode('，', $data['item_detail']);
        // }        
        foreach ($data as $k => $v) {
            $data[$k] = mysqli_real_escape_string($link, $v);
        }
        foreach ($fields as $v) {
          $result=mysqli_query($link,"UPDATE user SET {$v} = {$data[$v]} WHERE user = {$_SESSION['user']}");
        }
        // $sql_name=implode("`,`", $fields);
        // $sql_values=implode("','", $data);
       
        // if (!$result) {
        // 	echo "<script>alert('1');<script>";
        // }else{
        // 	echo "<script>alert('2');<script>";
        	
        // }
      // }
    //      display();  
    // function display($message=null){
    // 	require './html/xm1_1.html';
    // 	exit;
    // }  
	?>