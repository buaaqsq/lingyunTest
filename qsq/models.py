 # -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

class user(models.Model):
	username = models.CharField(max_length=50, blank='false') 
	password = models.CharField(max_length=50, blank='false') 
	Email = models.EmailField(blank='false')
	role = models.CharField(max_length=50, blank='false') 

	def __unicode__(self):
		return self.username

class Cluster(models.Model):
	name = models.CharField(max_length=50,unique=True,verbose_name='name')
	user = models.ForeignKey(user)
	time = models.DateTimeField(auto_now='true')
	component = models.CharField(max_length=50, null=True, blank=True)
	hdfsHA = models.IntegerField(blank=True)
	hosts = models.TextField(null=True, blank=True)
	javaPath = models.CharField(max_length=50, null=True, blank=True)
	def __unicode__(self):
		return self.name

class Component(models.Model):
	cluster = models.ForeignKey(Cluster, blank='false', related_name='cluid')
	name = models.CharField(max_length=50, verbose_name='name')
	cominfo = models.TextField(blank='true')
	description = models.CharField(max_length=100, verbose_name="description", null=True, blank=True)
	version = models.CharField(max_length=50, verbose_name='version')
	confdir = models.CharField(max_length=100, verbose_name="description", null=True, blank=True)
	logdir = models.CharField(max_length=100, verbose_name="description", null=True, blank=True)
	tmpdir = models.CharField(max_length=100, verbose_name="description", null=True, blank=True)
	path = models.CharField(max_length=100, verbose_name="description", null=True, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "component"
		verbose_name_plural = verbose_name


class Configuration(models.Model):
	component = models.ForeignKey(Component, blank='false')
	name = models.CharField(max_length=200, verbose_name='configuration')  
	default = models.CharField(max_length=200, verbose_name='default', null=True, blank=True)    
	value = models.CharField(max_length=200, verbose_name='value')   
	description = models.CharField(max_length=200, verbose_name='description', null=True, blank=True) 
	file = models.CharField(max_length=200, verbose_name='file')
	level = models.CharField(max_length=200, verbose_name='level')

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "configuration"
		verbose_name_plural = verbose_name

class DefaultSetting(models.Model):
	name = models.CharField(max_length=200, verbose_name='name')      
	value = models.CharField(max_length=500, verbose_name='value')   
	description = models.TextField( verbose_name='description') 
	file = models.CharField(max_length=200, verbose_name='file')
	component = models.CharField(max_length=200)
	level = models.CharField(max_length=200, verbose_name='level')
	def __unicode__(self):
		return self.name

class jobInfo(models.Model):
	clusterid = models.ForeignKey(Cluster)
	jobID = models.CharField(max_length=100)
	user = models.CharField(max_length=50)
	name = models.CharField(max_length=100)
	applicationType = models.CharField(max_length=100)
	queue = models.CharField(max_length=50)
	starttime = models.DateTimeField(auto_now='true')
	finishTime = models.DateTimeField(auto_now='true')
	state = models.CharField(max_length=50)
	finalStatus = models.CharField(max_length=50)	
	def __unicode__(self):
		return self.jobID

class host(models.Model):
	clusterid = models.ForeignKey(Cluster)
	hostname = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	ip = models.IPAddressField()
	rack = models.CharField(max_length=10, null=True, blank=True)
	ssh_port = models.IntegerField(blank=True)
	ssh_user = models.CharField(max_length=20, null=True, blank=True)
	ssh_pass = models.CharField(max_length=100, null=True, blank=True)
	os = models.CharField(max_length=20)
	create_time = models.DateField(auto_now='true')
	CPU = models.CharField(max_length=20, null=True, blank=True)
	# CPUNum = models.IntegerField(blank=True)
	mem = models.CharField(max_length=20, null=True, blank=True)
	disk = models.CharField(max_length=20, null=True, blank=True)

	def __unicode__(self):
		return self.hostname

class nodeMainInfo(models.Model):
	hostId = models.ForeignKey(host)
	cpu_info = models.CharField(max_length=100)
	cpu_num = models.IntegerField(blank=True)
	cpu_speed = models.CharField(max_length=100)
	disk_total = models.IntegerField(blank=True)
	mem_total = models.CharField(max_length=100)
	machine_total = models.CharField(max_length=100)
	os_name = models.CharField(max_length=100)
	boottime = models.DateField()
	mtu = models.CharField(max_length=100)
	swap_total = models.CharField(max_length=100)
	time = models.DateField(auto_now='true')
	def __unicode__(self):
		return self.hostId+self.time

class nodeRealtimePercentage(models.Model):
	hostId = models.ForeignKey(host)
	load_one = models.FloatField()
	load_five = models.FloatField()
	load_fifteen = models.FloatField()
	cpu_intr = models.FloatField()
	cpu_sintr = models.FloatField()
	cpu_idle = models.FloatField()
	cpu_aidle = models.FloatField()
	cpu_nice = models.FloatField()
	cpu_user = models.FloatField()
	cpu_system = models.FloatField()
	cpu_wio = models.FloatField()
	part_max_used = models.FloatField()
	mem_used = models.FloatField()
	time = models.DateField(auto_now='true')
	def __unicode__(self):
		return self.hostId+self.time
	
class nodeRealtimeInfo(models.Model):
	hostId = models.ForeignKey(nodeRealtimePercentage)
	disk_free = models.IntegerField()
	proc_run = models.IntegerField()
	mem_cached = models.IntegerField()
	mem_free = models.IntegerField()
	mem_buffers = models.IntegerField()
	mem_shared = models.IntegerField()
	proc_total = models.IntegerField()
	swap_free = models.IntegerField()
	pkts_out = models.IntegerField()
	pkts_in = models.IntegerField()
	bytes_in = models.IntegerField()
	bytes_out = models.IntegerField()
	time = models.DateField(auto_now='true')
	def __unicode__(self):
		return self.hostId+self.time

class serviceRole(models.Model):
	name = models.CharField(max_length=20, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	def __unicode__(self):
		return self.name

class hostRole(models.Model):
	cluster = models.ForeignKey(Cluster, blank='false')
	hostid = models.ForeignKey(host)
	servicerole = models.ForeignKey(serviceRole)
	
class nodesStorage(models.Model):
	role = models.ForeignKey(hostRole, verbose_name='roleID')
	is_formatted = models.BooleanField(blank=True)
	nn_storage = models.TextField(null=True, blank=True)
	dn_storage = models.TextField(null=True, blank=True)
	local_storage = models.TextField(null=True, blank=True)
	system_storage = models.TextField(null=True, blank=True)
	
	def __unicode__(self):
		return self.roleID

class service(models.Model):
	rold = models.ForeignKey(hostRole, verbose_name='roleID')
	port = models.IntegerField()
	pid = models.IntegerField()
	starttime = models.DateTimeField(auto_now='true')
	def __unicode__(self):
		return self.pid

	
class review(models.Model):
	cluster = models.ForeignKey(Cluster)
	servicename = models.CharField(max_length=100)
	hostnum = models.IntegerField()
	hosts = models.TextField(null=True, blank=True)
	parentservice = models.CharField(max_length=100)
	def __unicode__(self):
		return self.servicename



# 以下为other的数据库，仅供参考
	
class settings(models.Model):
	name = models.CharField(max_length=100, verbose_name='name')
	value = models.TextField(blank='false')
	description = models.TextField(blank='false')
  	filename = models.CharField(max_length=100)
	level = models.IntegerField(blank='false')
	def __unicode__(self):
		return self.name
	
class nodes_settings(models.Model):
	filename = models.CharField(max_length=225, blank='false')
	content = models.TextField(blank='false')
	create_time = models.DateField(auto_now='true', blank='false')
	ip = models.IPAddressField(blank='false')

	def __unicode__(self):
		return self.ip	


class nodes_hbase_role(models.Model):
	ip = models.IPAddressField(blank='false')
	is_master = models.BooleanField(blank='false')
	is_regionserver = models.BooleanField(blank='false')
	is_zookeeper = models.BooleanField(blank='false')
	
	def __unicode__(self):
		return self.ip

class nodes_hive_role(models.Model):
	ip = models.IPAddressField(blank='false')
	is_hcatalog = models.BooleanField(blank='false')
	
	def __unicode__(self):
		return self.ip

class hive_settings(models.Model):
	name = models.CharField(max_length=100, blank='false') 
	value = models.CharField(max_length=100, blank='false')
	description = models.TextField(blank='false')
	filename = models.CharField(max_length=100, blank='false')
	level = models.IntegerField(blank='false')
	
	def __unicode__(self):
		return self.name

class hbase_settings(models.Model):
	name = models.CharField(max_length=100, blank='false') 
	value = models.CharField(max_length=100, blank='false')
	description = models.TextField(blank='false')
	filename = models.CharField(max_length=100, blank='false')
	level = models.IntegerField(blank='false')	
	
	def __unicode__(self):
		return self.name

class nodes_hbase_settings(models.Model):
	filename = models.CharField(max_length=225, blank='false')
	content = models.TextField(blank='false')
	create_time = models.DateField(auto_now='true', blank='false')
	ip = models.IPAddressField(blank='false')

	def __unicode__(self):
		return self.ip

class nodes_hive_settings(models.Model):
	filename = models.CharField(max_length=225, blank='false')
	content = models.TextField(blank='false')
	create_time = models.DateField(auto_now='true', blank='false')
	ip = models.IPAddressField(blank='false')

	def __unicode__(self):
		return self.ip

admin.site.register(Configuration)
admin.site.register(Component)
admin.site.register(user)
admin.site.register(serviceRole)
admin.site.register(DefaultSetting)
admin.site.register(host)
admin.site.register(hostRole)
admin.site.register(service)
admin.site.register(nodesStorage)
admin.site.register(Cluster)
admin.site.register(review)
# admin.site.register(settings)
# admin.site.register(nodes_settings)
# admin.site.register(nodes_hbase_role)
# admin.site.register(nodes_hive_role)
# admin.site.register(hive_settings)
# admin.site.register(hbase_settings)
# admin.site.register(nodes_hbase_settings)
# admin.site.register(nodes_hive_settings)


