# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import RequestContext
from django.forms.util import ErrorList
from django.contrib import auth
from django.contrib.auth.decorators import login_required,permission_required

from models import *
from forms import *
from transfer import *
from tools.DataOper import *
import os, pexpect
from install.install import ServiceInstall
from shell.qsqService import Install
# Create your views here.
		
def logout(request):
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/account/loggedout/")	
	
def step1(request):
	if gl.STEP != 0:
		p = Cluster.objects.get(name=gl.CLUSTER)
		p.delete()
		gl.CLUSTER=''
		gl.STEP=0
		
	form = Step1Form(request.POST or None)	
	if form.is_valid():
		cd = form.cleaned_data
		clustername = cd['clustername']
		nodeslist = cd['nodes']
		
		gl.clustername = clustername
		hoststr=""
		u = user.objects.get(username='qsq')
		p = Cluster.objects.filter(name=clustername)
		if not len(p):
			p = Cluster(name=clustername,user=u,hosts="",component=1,hdfsHA=0)
			p.save()
			gl.CLUSTER=clustername
			gl.username="qsq"
			gl.STEP=1
			p = Cluster.objects.get(name=clustername)
			request.session["username"]='qsq'
			request.session["cluster"]=clustername
			
			hostip = Node().getIPfromHosts()
																																																																																																																																																				
			for node in nodeslist.split('\n'):
# 				print("%s" % node)
				if(node[0] != "\n"):
					hostlist = node.split(',')
					# 添加主机到数据库
					if hostip.has_key(hostlist[0]):
						hp = host(clusterid=p,hostname=hostlist[0],password=hostlist[1],ip=hostip[hostlist[0]],os='centos6.4',ssh_port='8020')
						hp.save()
						hoststr +=hostlist[0] +  ","
					else :
						print "cannot find the IP of " + hostlist[0] + "please make sure your hosts_file contain the hosts or check the hostname"
			p.hosts = hoststr[:-1]
			p.save()
		else:
			return HttpResponse("<p>用户已存在，请重新输入用户名</p>")
		
		hp = host.objects.filter(clusterid=p)
		if len(hp) == 0:
			return HttpResponse("不能获取主机名和密码，请安装第一步")
		for h in hp:
			foo = pexpect.spawn('scp /root/qsqClient.py %s:/root/' % h.hostname)
			foo.expect(['password: '])  
			foo.sendline(h.password)
			foo.expect(pexpect.EOF)				
		
		return HttpResponseRedirect('/qsq/step/02')
			
	t = get_template('step1.html')
	c = RequestContext(request,{"form":form})
	return HttpResponse(t.render(c))
					
def step2(request):
	form = Step2Form(request.POST or None)
	if form.is_valid():
		cd = form.cleaned_data
		compenent = cd['compenent']
		java_home = cd['java_home']
		JDK = request.REQUEST.getlist("autoInstall")
		p = Cluster.objects.get(name = gl.CLUSTER)
		#print("%s" % len(JDK))
		if len(JDK) != 0:
			p.javaPath = "/usr/local/java"
		else:
			p.javaPath = java_home
		component=""
		p = Cluster.objects.get(name=gl.CLUSTER)
		for c in compenent:
			component += c.encode()+","
			pcom = Component(cluster=p,name=gl.componentKV[c],version="")
			pcom.save()
		p.component = component[:-1]
		p.save()
		gl.STEP=2
	 #	print("%s%s%s" % (java_home,compenent,JDK))
		return HttpResponseRedirect('/qsq/step/03')
	
	t = get_template('step2.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))
	
def step3(request):
	form = Step3Form(request.POST or None)
	if form.is_valid():
		cd = form.cleaned_data
		ha = cd['ha']
		gl.ha = ha
		p = Cluster.objects.get(name = gl.CLUSTER) 
		p.hdfsHA=int(ha)
		p.save()
		gl.STEP=3
		#print("%s" % ha )
		return HttpResponseRedirect('/qsq/step/04')

	t = get_template('step3.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))

def step4(request):
	hosts = set(Node().getNodes())
	serverSet = Node().getServiceList()
	#print Node().getNodesTuple()
	t = get_template('step4.html')
	if gl.ha == "0":
		print("选择无HA安装")
		form = NodeArrange(request.POST or None)

	elif gl.ha == "1":
		print("选择启用QJM高可用性方案")
		form = NodeArrangeForQJM(request.POST or None)
		#t = get_template('step4HaQJM.html')
	elif gl.ha == "2":
		print("选择启用NFS高可用性方案")
		form = NodeArrangeForNFS(request.POST or None) 
		#t = get_template('step4HaNFS.html')
		
	if form.is_valid():
		cd = form.cleaned_data
		p = Cluster.objects.get(name = gl.CLUSTER) 
		for s in serverSet:
			srp = serviceRole.objects.get(name=s)
			hp = host.objects.get(hostname=cd[s],clusterid=p)
			hr = hostRole(cluster=p,hostid=hp,servicerole=srp)
			hr.save()
		
		gl.STEP=4
		return HttpResponseRedirect('/qsq/step/05')
	
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))

	
def step5(request):
	
	hosts = set(Node().getNodes())
	if request.method == 'POST':
		Datanode = request.REQUEST.getlist("DataNode")
		Nodemanager = request.REQUEST.getlist("Nodemanager")
		RegionServer = request.REQUEST.getlist("RegionServer")
		Worker = request.REQUEST.getlist("worker")
		
		print Datanode,Nodemanager,RegionServer,Worker
		p = Cluster.objects.get(name = gl.CLUSTER) 
		for regionserver in RegionServer:
			d = regionserver
			srp = serviceRole.objects.get(name="regionserver")			
			hp = host.objects.get(hostname=d,clusterid=p)
			hr = hostRole(cluster=p,hostid=hp,servicerole=srp)
			hr.save()
		for nodemanager in Nodemanager:
			d = nodemanager
			srp = serviceRole.objects.get(name="nodemanager")
			hp = host.objects.get(hostname=d,clusterid=p)
			hr = hostRole(cluster=p,hostid=hp,servicerole=srp)
			hr.save()
		for datanode in Datanode:
			d = datanode
			srp = serviceRole.objects.get(name="datanode")
			hp = host.objects.get(hostname=d)
			hr = hostRole(cluster=p,hostid=hp,servicerole=srp)
			hr.save()
			
		for worker in Worker:
			d = worker
			srp = serviceRole.objects.get(name="worker")
			hp = host.objects.get(hostname=d,clusterid=p)
			hr = hostRole(cluster=p,hostid=hp,servicerole=srp)
			hr.save()
		
		gl.STEP=5

# 		form = Step3Form(request.POST)
# 		if form.is_valid():		
		return HttpResponseRedirect('/qsq/step6hadoop')
	
	t = get_template('step5.html')
	c = RequestContext(request,{"hosts":hosts})
	return HttpResponse(t.render(c))
	
def step6hadoop(request):
	coreForm = CoreForm(request.POST or None)
	hdfsForm = HdfsForm(request.POST or None)
	yarnForm = YarnForm(request.POST or None)
	hadoopEnvForm=HadoopEnvForm(request.POST or None)
	mapredForm=MapredForm(request.POST or None)
	if coreForm.is_valid() and hdfsForm.is_valid() and yarnForm.is_valid() and hadoopEnvForm.is_valid() and mapredForm.is_valid():
		p = Cluster.objects.get(name=gl.CLUSTER)
		comp = Component.objects.get(name="Hadoop",cluster=p)
		coreForm_data=coreForm.cleaned_data
		for a in coreForm_data:
			cfg = Configuration(component=comp,name=a,value=coreForm_data[a],file="core-site.xml",level=0)
			cfg.save()
		
		hdfsForm_data=hdfsForm.cleaned_data
		for b in hdfsForm_data:
			cfg = Configuration(component=comp,name=b,value=hdfsForm_data[b],file="hdfs-site.xml",level=0)
			cfg.save()
		
		yarnForm_data=yarnForm.cleaned_data
		for c in yarnForm_data:
			cfg = Configuration(component=comp,name=c,value=yarnForm_data[c],file="yarn-site.xml",level=0)
			cfg.save()
		
		hadoopEnvForm_data=hadoopEnvForm.cleaned_data
		for d in hadoopEnvForm_data:
			cfg = Configuration(component=comp,name=d,value=hadoopEnvForm_data[d],file="hadoop-env.sh",level=0)
			cfg.save()
			
		defaultsetting = DefaultSetting.objects.filter(file="hadoop-env.sh",level=1)
		for s in defaultsetting:
			cfg = Configuration(component=s.component,name=s.name,value=s.value,file=s.file,level=s.level,default=s.value)
			cfg.save()
		
		mapredForm_data=mapredForm.cleaned_data
		for c in mapredForm_data:
			cfg = Configuration(component=comp,name=c,value=mapredForm_data[c],file="mapred-site.xml",level=0)
			cfg.save()
			
		return HttpResponseRedirect('/qsq/install')
		
	
	t = get_template('step6hadoop.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))

def step6hbase(request):
	
	form = HbaseForm(request.POST or None)
	if form.is_valid():
		p = Cluster.objects.get(name=gl.CLUSTER)
		comp = Component.objects.get(name="Hbase",cluster=p)
		cd = form.cleaned_data
		for c in cd:
			print(c + ':' + cd[c])
			cfg = Configuration(component=comp,name=c.replace('_','.'),value=cd[c],default="//",file="11",level=0)
			cfg.save()
		gl.STEP=6	
		return HttpResponseRedirect('/qsq/step6hive')
	
	t = get_template('step6hbase.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))


def step6hive(request):
	
	form = HiveForm(request.POST or None)
	if form.is_valid():
		p = Cluster.objects.get(name=gl.CLUSTER)
		comp = Component.objects.get(name="Hive",cluster=p)
		cd = form.cleaned_data
		for c in cd:
			print(c + ':' + cd[c])
			cfg = Configuration(component=comp,name=c.replace('_','.'),value=cd[c],default="//",file="11",level=0)
			cfg.save()
		gl.STEP=6
		return HttpResponseRedirect('/qsq/step6spark')
	
	t = get_template('step6hive.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))


def step6spark(request):
	
	form = SparkForm(request.POST or None)
	if form.is_valid():
		p = Cluster.objects.get(name=gl.CLUSTER)
		comp = Component.objects.get(name="Spark",cluster=p)
		cd = form.cleaned_data
		for c in cd:
			print(c + ':' + cd[c])
			cfg = Configuration(component=comp,name=c.replace('_','.'),value=cd[c],default="//",file="11",level=0)
			cfg.save()
		gl.STEP=6
		return HttpResponseRedirect('/qsq/review')

	t = get_template('step6spark.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))	
	
def snapshot(request):
	form = SparkForm(request.POST or None)
	if form.is_valid():
		return HttpResponseRedirect('snapshot.html')
	
	t = get_template('snapshot.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))	
	
def dashboard(request):
	form = SparkForm(request.POST or None)
	if form.is_valid():
		return HttpResponseRedirect('dashboard.html')
	
	t = get_template('dashboard.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))

def heatmaps(request):
	form = SparkForm(request.POST or None)
	if form.is_valid():
		return HttpResponseRedirect('heatmaps.html')
	
	t = get_template('heatmaps.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))
	
	
def hosts(request):
	
	p = Cluster.objects.get(name=gl.CLUSTER)
	hp = host.objects.filter(clusterid=p)
	
	form = SparkForm(request.POST or None)
	if form.is_valid():
		return HttpResponseRedirect('hosts.html')
	
	t = get_template('hosts.html')
	c = RequestContext(request,{"hosts":hp})
	return HttpResponse(t.render(c))
		
def services(request):
	form = SparkForm(request.POST or None)
	if form.is_valid():
		return HttpResponseRedirect('services.html')
	
	t = get_template('services.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))

def getJobs(request):
	form = SparkForm(request.POST or None)
	if form.is_valid():
		return HttpResponseRedirect('jobs.html')
	
	t = get_template('jobs.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))
	
def getReview(request):
	
	info = {}
	info["name"] = name=gl.CLUSTER
	p = Cluster.objects.get(name=gl.CLUSTER)
	hp = host.objects.filter(clusterid=p)
	info["hostnum"]=len(hp)
	rp = review.objects.filter(cluster=p)
	services={}
	for r in rp:
		if not info.has_key(r.parentservice):
			info[r.parentservice]=[]
		if r.hostnum == 1:
			services[r.servicename]=r.hosts
		else:
			services[r.servicename]=str(r.hostnum) + "\n" + r.hosts
		
	form = SparkForm(request.POST or None)
	if form.is_valid():
		return HttpResponseRedirect('review.html')
	
	t = get_template('review.html')
	c = RequestContext(request,{"info":info,"services":services})
	return HttpResponse(t.render(c))

def index(request):
	form = SparkForm(request.POST or None)
	if form.is_valid():
		u = form.cleaned_data['username']
		pw = form.cleaned_data['password']
		p = user.objects.filter(username=u,password=pw)
		print p
		if len(p) != 0:
			return HttpResponseRedirect('/qsq/step/01')
	
	t = get_template('login.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))


def test(request):
	coreForm = CoreForm(request.POST or None)
	hdfsForm = HdfsForm(request.POST or None)
	yarnForm = YarnForm(request.POST or None)
	hadoopEnvForm=HadoopEnvForm(request.POST or None)
	mapredForm=MapredForm(request.POST or None)
	if coreForm.is_valid() and hdfsForm.is_valid() and yarnForm.is_valid() and hadoopEnvForm.is_valid() and mapredForm.is_valid():
		p = Cluster.objects.get(name=gl.CLUSTER)
		comp = Component.objects.get(name="Hadoop",cluster=p)
		coreForm_data=coreForm.cleaned_data
		for a in coreForm_data:
			cfg = Configuration(component=comp,name=a,value=coreForm_data[a],file="core-site.xml",level=0)
			cfg.save()
		
		hdfsForm_data=hdfsForm.cleaned_data
		for b in hdfsForm_data:
			cfg = Configuration(component=comp,name=b,value=hdfsForm_data[b],file="hdfs-site.xml",level=0)
			cfg.save()
		
		yarnForm_data=yarnForm.cleaned_data
		for c in yarnForm_data:
			cfg = Configuration(component=comp,name=c,value=yarnForm_data[c],file="yarn-site.xml",level=0)
			cfg.save()
		
		hadoopEnvForm_data=hadoopEnvForm.cleaned_data
		for d in hadoopEnvForm_data:
			cfg = Configuration(component=comp,name=d,value=hadoopEnvForm_data[d],file="hadoop-env.sh",level=0)
			cfg.save()
		
		mapredForm_data=mapredForm.cleaned_data
		for c in mapredForm_data:
			cfg = Configuration(component=comp,name=c,value=mapredForm_data[c],file="mapred-site.xml",level=0)
			cfg.save()
		
	t = get_template('step6hadoop.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))

#测试用
def initHbaseConf(request):
	#获取form，如果是get则生成form
	form = SparkForm(request.POST or None)

	t = get_template('hbaseParam.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))

def stepError(request):
	t = get_template('stepError.html')
	c = RequestContext(request)
	return HttpResponse(t.render(c))

@login_required 	
def getStep(request,step):
	if gl.STEP < int(step)-1:return stepError(request)
	if step == "01" : return step1(request)
	elif step == "02" : return step2(request)
	elif step == "03" : return step3(request)
	elif step == "04" : return step4(request)
	elif step == "05" : return step5(request)

def install(request):
	if ServiceInstall().hadoopInstaller(gl.CLUSTER):
		return HttpResponse("there are some error")
	Install().step1()
	p = Cluster.objects.get(name=gl.CLUSTER)
	hp = host.objects.filter(clusterid=p)
	if len(hp) == 0:
		return HttpResponse("不能获取主机名和密码，请安装第一步")
	for h in hp:
		foo = pexpect.spawn("ssh %s 'python qsqClient.py'" % h.hostname)
		foo.expect(['password: '])  
		foo.sendline(h.password)
		foo.expect(pexpect.EOF)
	
	return HttpResponse("hahaha")
	
if "__main__" == __name__:
	install
	
