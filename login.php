	<?php
	  // require './config.php';
	  // require './html/login.html';
      if($_POST){
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
        $query=mysqli_query($link,"select * from `user` where `name` ='{$data['name']}' and `password` ='{$data['password']}'");
        if(!mysqli_num_rows($query)){
        	
        	display("用户名或密码错误");
        }else{
        	$_SESSION['user'] = $data['name'];
        	header('Location:index.php');
        	exit;
        }
      }
      display();
      function display($message =null){
      	require './html/login.html';
      	exit;
      	
      }
	?>