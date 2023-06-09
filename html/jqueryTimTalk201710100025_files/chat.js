  //获取好友网名
  $('.conLeft li').on('click',function(){
		$(this).addClass('bg').siblings().removeClass('bg');
		var intername=$(this).children('.liRight').children('.intername').text();
		$('.headName').text(intername);
		$('.newsList').html('');
	})
  //发送消息
	$('.sendBtn').on('click',function(){
		var news=$('#dope').val();
		if(news==''){
			alert('不能为空');
		}else{
			$('#dope').val('');
		var str='';
		str+='<li>'+
				'<div class="nesHead"><img src="jqueryTimTalk201710100025_files/6.jpg"/></div>'+
				'<div class="news"><img class="jiao" src="jqueryTimTalk201710100025_files/talk.jpg">'+news+'</div>'+
			'</li>';
		$('.newsList').append(str);
		setTimeout(answers,1000); 
		$('.conLeft').find('li.bg').children('.liRight').children('.infor').text(news);
		//将滚动条始终保持在底部
		$('.RightCont').scrollTop($('.RightCont')[0].scrollHeight );
	}
	
	})
	//随机产生一条回复
	function answers(){
		var arr=["嗯。。。尽量在室内采集吧"];
		var aa=Math.floor((Math.random()*arr.length));
		var answer='';
		answer+='<li>'+
					'<div class="answerHead"><img src="jqueryTimTalk201710100025_files/xm1.jpg"/></div>'+
					'<div class="answers"><img class="jiao" src="jqueryTimTalk201710100025_files/TIM图片20170926103645_03_02.jpg">'+arr[aa]+'</div>'+
				'</li>';
		$('.newsList').append(answer);	
		$('.RightCont').scrollTop($('.RightCont')[0].scrollHeight );
	//历史消息的展现与隐藏
	var newlen=$('.newsList li').length;
	var lis=$('.newsList li:last').index();
	var maxlen=newlen-5;
	console.log(lis);
			if(newlen%10>5){
				$('.ChatRecord').show();
				$('.newsList li:lt('+maxlen+')').hide();
			}
	}
	//表情包的展现与隐藏
	$('.ExP').on('click',function(){
		if($('.emjon').css('display')=='none'){
			$('.emjon').show();
		}else{
			$('.emjon').hide();
		}
	})
	
	//发送表情
	$('.emjon li').on('click',function(){
		var imgSrc=$(this).children('img').attr('src');
		var str="";
		str+='<li>'+
				'<div class="nesHead"><img src="jqueryTimTalk201710100025_filess/6.jpg"/></div>'+
				'<div class="news"><img class="jiao" src="jqueryTimTalk201710100025_files/talk.jpg"><img class="Expr" src="'+imgSrc+'"></div>'+
			'</li>';
		$('.newsList').append(str);
		setTimeout(answers,1000);
		$('.emjon').hide();
		$('.RightCont').scrollTop($('.RightCont')[0].scrollHeight );
	})
	//展开历史消息
	$('.RightCont').on('click','.ChatRecord',function(){
		$('.newsList li:eq(0),li:gt(0)').show();
		$('.ChatRecord').hide();
	})
	
	