//*****脚本作者  www.mymickey.org   ******如您使用后有什么BUG请到作者网站告知
//脚本排序算法www.overset.com//此算法经过www.mymickey.org稍加修改
//此脚本支持中文汉字排序、中英文混合排序、数据大小排序、文件名称类型排序、日期排序、价格排序、中文和数字排序;
//脚本表格排序使用方法文档载入后new tableListSort(arguments,arguments);
//接受两个参数：第一个参数为必须的，可以是字符串ID，也可以是table对象,
//第二个可选参数，此参数为一个对象，{data:index,fileType:index,fufn(){}}；
//对象有三个可选的属性，第一个和第二个为扩展排序的数据类型，第三个参数为排序后需要执行的函数；
//如果表格数据中有需要排序的数据大小，如1KB 1MB 1GB 这样的数据类型的话,可以{data:index};
//index为表格需排序的某一列的下标值，从0开始计数，如表格的第二列为1KB MB这样的数据类型，{data:2};
//对象的第二个属性{fileType:index},此扩展排序为文件类型，如xml,jpg,exe。index同样为列的下标值。
//对象的第三个属性为一个排序后需执行的函数{fn:function(){执行的代码}}。
//HTML代码中必须的元素为:table元素，table元素的第一行必须使用thead元素包含tr,tr中必须包含可点击排序的元素th;thead
//下一个sibling元素必须为tbody,tbody中需包含tr。table也可以包含caption。
//*****脚本作者  www.mymickey.org   ******如您使用后有什么BUG请到作者网站留言
//欢迎一起交流更好的排序算法:) 
//鼠标样式我在脚本里面加好了不需要CSS添加
var Class={
	create:function(){
		return function(){
			this.init.apply(this,arguments)
			}
		}
	}
function each(o,fn){
	for(var j=0,len=o.length;j<len;j++){
		fn(o[j],j)
		}
	}

Function.prototype.bind=function(){
	var method=this;
	var args=Array.prototype.slice.call(arguments);
	var object=args.shift();
	return function(){
		return method.apply(object,args.concat(Array.prototype.slice.call(arguments)))
		}
	}	
function $(elem,elem2){
	var arr=[];
	typeof elem=='string' ?arr.push(document.getElementById(elem)):arr.push(elem);
	elem2&&arr.push(arr[0].getElementsByTagName(elem2));
	(arr.length>1)&&(typeof elem=='object') &&(arr.shift());
	return arr.length!=2?arr[0]:arr[1];
	}
	
var tableListSort=Class.create()
tableListSort.prototype={
	init:function(tables,options){
		this.table=$(tables);//找到table元素
		this.th=$($(this.table,'thead')[0],'th');//找到th元素
		this.tbody=$(this.table,'tbody')[0];//找到tbody元素
		this.Row=$(this.tbody,'tr'); //找到tr元素
		this.rowArr=[];//tr塞入这个数组
		this.Index=null;
		this.options=options||{};
		this.finish=this.options.fn||function(){};
		this.dataIndex=Math.abs(this.options.data)||null;//提供比较数据类型的坐标。
		this.file=Math.abs(this.options.fileType)||null;//提供需要比较file类型坐标
		each(this.Row,function(o){this.rowArr.push(o)}.bind(this));//将tr对象列表载入进数组
		for(var i=0;this.th.length>i;i++){
			this.th[i].onclick=this.Sort.bind(this,i)//使用bind间接保持一个下标值(变量)，传递过去
			this.th[i].style.cursor='pointer';
			}
		this.re=/([-]{0,1}[0-9.]{1,})/g;// 替换的正则表达式
		this.dataIndex&&subData(this.Row,this.dataIndex,this.Row.length);
		},

	Sort:function(num){
		//var date1=new Date().getTime()//测试用于排序时间 如果想测试排序时间请讲注释去掉
		//另外的被点击 原先的被取消表示图标
		(this.Index!=null&&this.Index!=num)&&this.th[this.Index].setAttribute('sorted','');
		this.th[num].getAttribute('sorted')!='ed'?
		this.rowArr.sort(this.naturalSort.bind(this,num)):this.rowArr.reverse();
		//如果当前对象被点击过，使用reverse()对应的列直接反序,否则排序，因为使用的是预定义的sort()方法，所以如果要让执行排序的函数
		//知道需要排序的列的下标值的话，bind()传递num过去，this来调用;
		var frag=document.createDocumentFragment();//创建文档碎片
		each(this.rowArr,function(o){frag.appendChild(o)});//将排序后的数组插入文档碎片
		this.tbody.appendChild(frag);//碎片插入节点
		this.th[num].setAttribute('sorted','ed');
		//$('spans').innerHTML=(new Date().getTime())-date1;//测试用于排序时间 如果想测试排序时间请讲注释去掉
		this.finish(num);//排序后执行的函数
		this.Index=num;//被排序过的坐标值
		},
	naturalSort:function (num,a, b) {
		//判断是否是数据排序 如果是的话 查找属性
		var a=this.dataIndex!=num?a.cells[num].innerHTML:a.cells[num].getAttribute('data'),
		    b=this.dataIndex!=num?b.cells[num].innerHTML:b.cells[num].getAttribute('data');
		//num被bind方法传递过来的,找到需排序的单元格里面的内容
        var x = a.toString().toLowerCase() || '', y = b.toString().toLowerCase() || '',
                nC = String.fromCharCode(0),
                xN = x.replace(this.re, nC + '$1' + nC).split(nC),// 将字符串分裂成数组
                yN = y.replace(this.re, nC + '$1' + nC).split(nC),
                xD = (new Date(x)).getTime(), yD = (new Date(y)).getTime()
				xN = this.file!=num?xN:xN.reverse(),//如果有filetype则反序
				yN = this.file!=num?yN:yN.reverse()
				;
        if ( xD && yD && xD < yD )
                return -1;
        else if ( xD && yD && xD > yD )
                return 1;
        for ( var cLoc=0, numS = Math.max( xN.length, yN.length ); cLoc < numS; cLoc++ )
                if ( ( parseFloat( xN[cLoc] ) || xN[cLoc] ) < ( parseFloat( yN[cLoc] ) || yN[cLoc] ) )
				//不能转换为floatNumber直接进行字母比较，如'A'<'B' print//true
                        return -1;
                else if ( ( parseFloat( xN[cLoc] ) || xN[cLoc] ) > ( parseFloat( yN[cLoc] ) || yN[cLoc] ) )
                        return 1;
        return 0;
		}
	
	}       
function subData(o,i,len){//如果有数据大小排序给td添加一个自定属性给data//正则也是可以的判断的//mymickey没有在这里写正则
		for(var j=0;len>j;j++){
			if(o[j].cells[i].innerHTML.substring(o[j].cells[i].innerHTML.lastIndexOf('KB')).toLowerCase()=='kb'){
				o[j].cells[i].setAttribute('data',parseFloat(o[j].cells[i].innerHTML)*1024);
				}
			if(o[j].cells[i].innerHTML.substring(o[j].cells[i].innerHTML.lastIndexOf('MB')).toLowerCase()=='mb'){
				o[j].cells[i].setAttribute('data',parseFloat(o[j].cells[i].innerHTML)*1000000);
				}	
	   else if(o[j].cells[i].innerHTML.substring(o[j].cells[i].innerHTML.lastIndexOf('GB')).toLowerCase()=='gb'){
				o[j].cells[i].setAttribute('data',parseFloat(o[j].cells[i].innerHTML)*1000000000);
				}	
		  }
		}

