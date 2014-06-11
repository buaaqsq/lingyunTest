# -*- coding: utf-8 -*-
from django import forms
from models import user
from tools.DataOper import Node,ConfigurationData
from django.contrib.auth.forms import AuthenticationForm

class HbaseInitForm(forms.Form):
	rootdir = forms.CharField(widget=forms.TextInput(attrs={'value':'hdfs://{namenode}:9000/hbase','style':'margin:5px;',}))
	master = forms.CharField(widget=forms.TextInput(attrs={'value':'your_hostname','style':'margin:5px;',}))
	zookeeper_quorum = forms.CharField(widget=forms.TextInput(attrs={'value':'hostname1, hostname2, hostname3...','style':'margin:5px;',}))
	tmpdir = forms.CharField(widget=forms.TextInput(attrs={'value':'/tmp/hbase','style':'margin:5px;',}))
	mport = forms.CharField(widget=forms.TextInput(attrs={'value':'60000','style':'margin:5px;',}))
	rport = forms.CharField(widget=forms.TextInput(attrs={'value':'60020','style':'margin:5px;',}))
	miport = forms.CharField(widget=forms.TextInput(attrs={'value':'60010','style':'margin:5px;',}))

class newLoginForm(AuthenticationForm):
	password = forms.CharField(widget=forms.TextInput(attrs={'value':'password','style':'margin:5px;',}))
	username = forms.CharField(widget=forms.TextInput(attrs={'value':'username','style':'margin:5px;',}))

class LoginForm_(forms.ModelForm):
	
	class Meta:
		model = user    
	
	def __init__(self, *args, **kwargs):
		super(LoginForm_, self).__init__(*args, **kwargs)
	
	def clean_password(self):
		password = self.cleaned_data['password']
		if password == "":
			raise forms.ValidationError("价格必须大于零")
		return password
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if username=="":
			raise forms.ValidationError("价格必须大于零")
		return username
	
	def login(self):
		u = self.cleaned_data['username']
		pw = self.cleaned_data['password']
		p = user.objects.filter(username=u,password=pw)
		print p
		if p == None:
			raise forms.ValidationError("用户名或者密码错误")
		return pw
		
class Step1Form(forms.Form):
	clustername = forms.CharField(widget=forms.TextInput(attrs={'value':'mycluster','id':'cluster_name','style':'margin:5px;',}))
	nodes = forms.CharField(widget=forms.Textarea(attrs={'value':'hostname,password\nhostname,password','style':'margin:5px;',}))
	error_css_class = '填写格式错误'
	required_css_class = '此内容为集群运行关键内容，不能为空'
	
class Step2Form(forms.Form):
	CHOICE = (
			("1", "Hadoop  分布式计算基础框架，版本：2.2.0"), 
			("2", "Hbase  分布式的、面向列的开源数据库，版本：0.94.12"), 
			("3", "Hive  基于Hadoop的一个数据仓库工具，版本0.11.0"), 
			("4", "Pig  基于Hadoop的大规模数据分析平台，版本"), 
			("5", "Sqoop  Hadoop和关系型数据库中的数据相互转移的工具，版本"), 
			("6", "Ganglia  开源集群监视项目"), 
			("7", "Nagios  监视系统运行状态和网络信息的监视系统"), 
			("8", "Spark  内存计算框架"), 
			("9", "Phoniex  Hbase上的sql查询接口"))
	java_home = forms.CharField(widget=forms.TextInput(attrs={'value':'/usr/bin/java','style':'margin:5px;',}))
	compenent = forms.MultipleChoiceField(choices=CHOICE, widget=forms.CheckboxSelectMultiple(),initial=('1'))

class Step3Form(forms.Form):
	HA_CHOICE = (
			("0","HDFS不启用高可用性方案",),
			("1","HDFS启用QJM高可用性方案",),
			("2","HDFS启用NFS高科用性方案",),)
	
	ha = forms.ChoiceField(choices=HA_CHOICE, widget=forms.RadioSelect(),initial=('0'))

class NodeArrange(forms.Form):	
	namenode = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	resourmanager = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	zookeeper1 = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	zookeeper2 = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	zookeeper3 = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	def __init__(self, *args, **kwargs):
		super(NodeArrange, self).__init__(*args, **kwargs)
		NODES=Node().getNodesTuple()
		self.fields['namenode'].choices = NODES
		self.fields['resourmanager'].choices = NODES
		self.fields['zookeeper1'].choices = NODES
		self.fields['zookeeper2'].choices = NODES
		self.fields['zookeeper3'].choices = NODES
		services=Node().getServiceList()
		for s in services:
			self.fields[s]=forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
			self.fields[s].choices = NODES

#此form不再使用，仅供参考和充代码量
class NodeArrangeOld(forms.Form):
	namenode = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	resourmanager = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	hbasemaster = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	sparkmaster = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	gmated = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	hive = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	pig = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	phenix = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	zookeeper1 = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	zookeeper2 = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	zookeeper3 = forms.ChoiceField(widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	def __init__(self, *args, **kwargs):
		super(NodeArrange, self).__init__(*args, **kwargs)
		self.fields['namenode'].choices = Node().getNodesTuple()
		self.fields['resourmanager'].choices = Node().getNodesTuple()
		self.fields['hbasemaster'].choices = Node().getNodesTuple()
		self.fields['sparkmaster'].choices = Node().getNodesTuple()
		self.fields['gmated'].choices = Node().getNodesTuple()
		self.fields['hive'].choices = Node().getNodesTuple()
		self.fields['pig'].choices = Node().getNodesTuple()
		self.fields['phenix'].choices = Node().getNodesTuple()
		self.fields['zookeeper1'].choices = Node().getNodesTuple()
		self.fields['zookeeper2'].choices = Node().getNodesTuple()
		self.fields['zookeeper3'].choices = Node().getNodesTuple()


#此form不再使用，仅供参考和充代码量	
class NodeArrange_(forms.Form):
	NODES=()
	namenode = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	resourmanager = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	hbasemaster = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	sparkmaster = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	gmated = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	hive = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	pig = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	phenix = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	zookeeper1 = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	zookeeper2 = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))
	zookeeper3 = forms.ChoiceField(choices=NODES, widget=forms.Select(attrs={'onChange':"update()", 'style':'margin:5px;', }))

#此form不再使用，仅供参考和充代码量
class NodeArrangeForHA(NodeArrange):
	nodelist = []
	namenodeHa = forms.ChoiceField(choices=nodelist, widget=forms.Select(attrs={'style':'margin:5px;',}))
	
class NodeArrangeForQJM(NodeArrange):
	namenodeHa = forms.ChoiceField( widget=forms.Select(attrs={'style':'margin:5px;',})) 
	JournalNode1 = forms.ChoiceField( widget=forms.Select(attrs={'style':'margin:5px;',}))
	JournalNode2 = forms.ChoiceField( widget=forms.Select(attrs={'style':'margin:5px;',}))
	JournalNode3 = forms.ChoiceField( widget=forms.Select(attrs={'style':'margin:5px;',}))
	def __init__(self, *args, **kwargs):
		super(NodeArrangeForQJM, self).__init__(*args, **kwargs)
		self.fields['namenodeHa'].choices = Node().getNodesTuple()
		self.fields['JournalNode1'].choices = Node().getNodesTuple()
		self.fields['JournalNode2'].choices = Node().getNodesTuple()
		self.fields['JournalNode3'].choices = Node().getNodesTuple()

	
class NodeArrangeForNFS(NodeArrange):
	namenodeHa = forms.ChoiceField( widget=forms.Select(attrs={'style':'margin:5px;',})) 
	NFS1 = forms.ChoiceField( widget=forms.Select(attrs={'style':'margin:5px;',}))
	NFS2 = forms.ChoiceField( widget=forms.Select(attrs={'style':'margin:5px;',}))
	NFS3 = forms.ChoiceField( widget=forms.Select(attrs={'style':'margin:5px;',}))
	def __init__(self, *args, **kwargs):
		super(NodeArrangeForQJM, self).__init__(*args, **kwargs)
		self.fields['namenodeHa'].choices = Node().getNodesTuple()
		self.fields['NFS1'].choices = Node().getNodesTuple()
		self.fields['NFS2'].choices = Node().getNodesTuple()
		self.fields['NFS3'].choices = Node().getNodesTuple()	
	
class Step5Form(forms.Form):
	node_CHOICE = (
			("datanode","",),
			("nodemanager","",),
			("HRegionServer","",),
			("zookeeper","",),
			("SparkWorker","",),
			)
	compenent = forms.MultipleChoiceField(choices=node_CHOICE, widget=forms.CheckboxSelectMultiple(),initial=('1'))

class HdfsForm(forms.Form):
		def __init__(self, *args, **kwargs):
			super(HdfsForm, self).__init__(*args, **kwargs)
			hdfssite=ConfigurationData().getInitConf("hadoop2.2.0", "0", "hdfs-site.xml")
			for s in hdfssite:
				self.fields[s.name]=forms.CharField(widget=forms.TextInput(attrs={'value':s.value,'style':'margin:5px;',}))
				self.fields[s.name].help_text=s.description
				self.fields[s.name].value=s.value
class CoreForm(forms.Form):
		def __init__(self, *args, **kwargs):
			super(CoreForm, self).__init__(*args, **kwargs)
			coresite=ConfigurationData().getInitConf("hadoop2.2.0", "0", "core-site.xml")
			for s in coresite:
				self.fields[s.name]=forms.CharField(widget=forms.TextInput(attrs={'value':s.value,'style':'margin:5px;',}))
				self.fields[s.name].help_text=s.description

class YarnForm(forms.Form):
		def __init__(self, *args, **kwargs):
			super(YarnForm, self).__init__(*args, **kwargs)
			yarnsite=ConfigurationData().getInitConf("hadoop2.2.0", "0", "yarn-site.xml")
			for s in yarnsite:
				self.fields[s.name]=forms.CharField(widget=forms.TextInput(attrs={'value':s.value,'style':'margin:5px;',}))
				self.fields[s.name].help_text=s.description
class MapredForm(forms.Form):
		def __init__(self, *args, **kwargs):
			super(MapredForm, self).__init__(*args, **kwargs)
			mapredsite=ConfigurationData().getInitConf("hadoop2.2.0", "0", "mapred-site.xml")
			for s in mapredsite:
				self.fields[s.name]=forms.CharField(widget=forms.TextInput(attrs={'value':s.value,'style':'margin:5px;',}))
				self.fields[s.name].help_text=s.description
class HbaseForm(forms.Form):
		def __init__(self, *args, **kwargs):
			super(HbaseForm, self).__init__(*args, **kwargs)
			hbasesite=ConfigurationData().getInitConf("hbase", "0", "hbase-site.xml")
			for s in hbasesite:
				self.fields[s.name]=forms.CharField(widget=forms.TextInput(attrs={'value':s.value,'style':'margin:5px;',}))
				self.fields[s.name].help_text=s.description
class HiveForm(forms.Form):
		def __init__(self, *args, **kwargs):
			super(HiveForm, self).__init__(*args, **kwargs)
			hivesite=ConfigurationData().getInitConf("hive", "0", "hive-site.xml")
			for s in hivesite:
				self.fields[s.name]=forms.CharField(widget=forms.TextInput(attrs={'value':s.value,'style':'margin:5px;',}))
				self.fields[s.name].help_text=s.description
				
class HadoopEnvForm(forms.Form):
		def __init__(self, *args, **kwargs):
			super(HadoopEnvForm, self).__init__(*args, **kwargs)
			hivesite=ConfigurationData().getInitConf("hadoop2.2.0", "0", "hadoop-env.sh")
			for s in hivesite:
				self.fields[s.name]=forms.CharField(widget=forms.TextInput(attrs={'value':s.value,'style':'margin:5px;',}))
				self.fields[s.name].help_text=s.description

class configurationForm(forms.Form):	
	coreForm = CoreForm
	hdfsForm = HdfsForm
	yarnForm = YarnForm
	hadoopEnvForm=HadoopEnvForm
	mapredForm=MapredForm				

class Hadoop2Form(forms.Form):
	def __init__(self, *args, **kwargs):
		super(Hadoop2Form, self).__init__(*args, **kwargs)	
		hadoopconf=ConfigurationData().getComConf("hadoop2.2.0", "0")
		for s in hadoopconf:
			self.fields[s.name]=forms.CharField(widget=forms.TextInput(attrs={'value':s.value,'style':'margin:5px;',}))
												
class Hadoop2Form_(forms.Form):
	
	hadoop_tmp_dir = forms.CharField(widget=forms.TextInput(attrs={'value':'/hadoop/tmp','style':'margin:5px;',}))
	fs_defaultFS = forms.CharField(widget=forms.TextInput(attrs={'style':'margin:5px;',}),error_messages={'required': '不能为空'})
	
	dfs_namenode_name_dir = forms.CharField(widget=forms.TextInput(attrs={'value':'$hadoop.tmp.dir/name','style':'margin:5px;',}))
	dfs_namenode_data_dir = forms.CharField(widget=forms.TextInput(attrs={'value':'$hadoop.tmp.dir/data','style':'margin:5px;',}))
	dfs_webhdfs_enabled = forms.ChoiceField(choices=(("True","True",),("False","False",)), widget=forms.Select(attrs={'style':'margin:5px;',}))
	dfs_permissions = forms.ChoiceField(choices=(("True","True",),("False","False",)), widget=forms.Select(attrs={'style':'margin:5px;',}))
	dfs_replication = forms.CharField(widget=forms.TextInput(attrs={'value':'2','style':'margin:5px;',}))
	
	yarn_nodemanager_auxservices = forms.CharField(widget=forms.TextInput(attrs={'value':'mapreduce_shuffle','style':'margin:5px;',}))
	yarn_nodemanager_auxservices_mapreduce_shuffle_class = forms.CharField(widget=forms.TextInput(attrs={'value':'org.apache.hadoop.mapred.ShuffleHandler','style':'margin:5px;',}))
	yarn_resourcemanager_address = forms.CharField(widget=forms.TextInput(attrs={'value':'$hostname:8032','style':'margin:5px;',}))
	yarn_resourcemanager_hostname = forms.CharField(widget=forms.TextInput(attrs={'value':'$hostname','style':'margin:5px;',}))
	
class HbaseForm_(forms.Form):
	
	rootdir = forms.CharField(widget=forms.TextInput(attrs={'value':'hdfs://{namenode}:9000/hbase','style':'margin:5px;',}))
	master = forms.CharField(widget=forms.TextInput(attrs={'value':'your_hostname','style':'margin:5px;',}))
	zookeeper_quorum = forms.CharField(widget=forms.TextInput(attrs={'value':'hostname1, hostname2, hostname3...','style':'margin:5px;',}))
	tmpdir = forms.CharField(widget=forms.TextInput(attrs={'value':'/tmp/hbase','style':'margin:5px;',}))
	mport = forms.CharField(widget=forms.TextInput(attrs={'value':'60000','style':'margin:5px;',}))
	rport = forms.CharField(widget=forms.TextInput(attrs={'value':'60020','style':'margin:5px;',}))
	miport = forms.CharField(widget=forms.TextInput(attrs={'value':'60010','style':'margin:5px;',}))
	
class HiveForm_(forms.Form):
	hive_local = forms.ChoiceField(choices=(("True","True",),("False","False",)),widget=forms.Select(attrs={'style':'margin:5px;',}))
	hive_jdoURL = forms.CharField(widget=forms.TextInput(attrs={'value':'jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true','style':'margin:5px;',}))
	hive_driver = forms.CharField(widget=forms.TextInput(attrs={'value':'com.mysql.jdbc.Driver','style':'margin:5px;',}))
	hive_username = forms.CharField(widget=forms.TextInput(attrs={'value':'hive','style':'margin:5px;',}))
	hive_passwd = forms.CharField(widget=forms.TextInput(attrs={'value':'hive','style':'margin:5px;',}))	
	
class SparkForm(forms.Form):
		
	Spark_local_dir = forms.CharField(widget=forms.TextInput(attrs={'value':'/hadoop2/spark/tmp','style':'margin:5px;',}))
	Spark_executor_memory = forms.CharField(widget=forms.TextInput(attrs={'value':'512m','style':'margin:5px;',}))
	Spark_serializer = forms.CharField(widget=forms.TextInput(attrs={'value':'spark.JavaSerializer','style':'margin:5px;',}))
	Spark_kryo_registrator = forms.CharField(widget=forms.TextInput(attrs={'value':'()','style':'margin:5px;',}))
	Spark_cores_max = forms.CharField(widget=forms.TextInput(attrs={'value':'(infinite)','style':'margin:5px;',}))
	
	
	
	
	
	
	
	
