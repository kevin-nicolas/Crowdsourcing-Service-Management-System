<?php
	  require './config.php';	        
      if($_POST){
        $link = mysqli_connect($host, $user, $password, $dbname);
        if(!$link){
        	display('数据库连接失败'.mysql_connect_error());
        }
        mysqli_set_charset($link, 'utf8');
        $fields=['item_name','item_type','item_detail','position_requirements','skill','security_level','cycle','desired_continuation_type','regional','contact_name','email','phone_number','manager_account'];

        $data=[];
        foreach ($fields as $v) {
        	$data[$v] = isset($_POST[$v]) ? $_POST[$v] : '';      
        }
		$data['manager_account']=$_SESSION['user'];
        if (is_array($data['item_detail'])) {
          $data['item_detail'] = implode('，', $data['item_detail']);
        }        
        foreach ($data as $k => $v) {
            $data[$k] = mysqli_real_escape_string($link, $v);
        }
        
        $sql_name=implode("`,`", $fields);
        $sql_values=implode("','", $data);
        $result=mysqli_query($link,"insert into item (`$sql_name`) values ('$sql_values')");
        if (!$result) {
        	echo "<script>alert('1');<script>";
        }else{
        	echo "<script>alert('2');<script>";
        	
        }
      }
         display();  
    function display($message=null){
    	require './html/xm1_1.html';
    	exit;
    }  
	?>