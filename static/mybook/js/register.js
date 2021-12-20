$(function(){
	//5个提示框
	var error_name = true;
	var error_password = true;
	var error_check_password = true;
	var error_check = false;
	var error_vcode = true;
	var vcode='';

	$('#phone').blur(function() {
		check_phone();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});
	//获取验证码按钮
	$('#sendcode').click(function() {
		//error_name为假的时候说明手机号码格式 以及是否存在都验证完成
		//验证手机号码
		if (error_name){
			alert('请先确认手机号码的格式!')
			return;
		}
		//获取当前的手机号
        phone=$('#phone').val()
		//验证完成后 正确的话则发送ajax请求
		$.get('sendcoke',{'phone':phone},function (data){
			//判断短信是否发送成功
			if (data['code']==0){//成功
				alert(data['msg'])
				//短信发送成功后将按钮CD60S
				$('#sendcode').attr('disabled','disabled')
				$('#sendcode').text('获取验证码(60)')
				var time =60
				var in1=setInterval(function (){
					time-=1
					$('#sendcode').text('获取验证码('+time+')')
				},1000)
				setTimeout(function (){
				$('#sendcode').removeAttr("disabled");
				$('#sendcode').text('获取验证码')
				clearInterval(in1)
				},60000)
				//存储返回的验证码
				vcode=data['vcode']
			}else{//出错
				alert(data['msg'])
			}
		},'json')


	});

	//验证输入的短信验证码是否正确
	$('input[name=yzm]').blur(function (){
		if (vcode==''){
			$('#yzm').next().html('请先获取验证码!')
			$('#yzm').next().show();
		}else if($('#yzm').val()!=vcode){
			$('#yzm').next().html('验证码错误!')
			$('#yzm').next().show();
			error_vcode=true;
		}else {
			$('#yzm').next().html('OK!√√√√√√√√√√√√')
			$('#yzm').next().show();
			error_vcode=false;
		}
	})

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});

	//手机号码判断
	function check_phone(){
		//获取当前的手机号
        phone=$('#phone').val()
        //验证手机格式
        reg=/^1\d{10}$/
        if (!reg.test(phone)){
            $('#phone').next().html('手机号码格式不正确')
			$('#phone').next().show();
			error_name = true;
        }else{//手机格式正确的话
			//判断手机号码是否存在
			$.get("ckphone",{'phone':phone},function (data){
				//判断返回的结果
				if (data['code']==0){
					$('#phone').next().hide();
					error_name = false;
				}else{
					$('#phone').next().html(data['msg'])
					$('#phone').next().show();
					error_name = true;
				}
			},'json')

		}
	}

	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').next().html('密码最少8位，最长20位')
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}		
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}
	}


	$('form').submit(function() {
		check_phone();
		check_pwd();
		check_cpwd();

		if(error_name == false && error_password == false && error_check_password == false && error_check == false && error_vcode == false)
		{
			return true;
		}
		else
		{
			alert('请确认注册信息是否符合规则!')
			return false;
		}

	});

})