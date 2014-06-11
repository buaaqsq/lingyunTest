
struct NodeInfo{
1:required string cpu,
2:required string mem,
3:required string disk,
4:required string os,
5:optional string load,
6:required string ip,
}

struct HostInformation{
1:required string cpu_info,
2:required i16 cpu_num,
3:required double cpu_speed,
4:required double disk_total,
5:required double mem_total,
6:required string machine_type,
7:required string os_name,
8:required string boottime,//启动时间
9:required i64 mtu,//最大网络传输量
10:required double swap_total,//最大交换内存
}

struct Percentage{
1:required double load_one,  //一分钟平均负荷
2:required double load_five, //五分钟平均负荷
3:required double load_fifteen, //十五分钟平均负荷
4:required double cpu_intr, //cpu参与IO中断的时间所占百分比
5:required double cpu_sintr,//cpu参与IO软中断的时间所占百分比
6:required double cpu_idle,//cpu空闲，系统没有显著磁盘IO请求的时间所占百分比
7:optional double cpu_aidle,//自启动开始CPU空闲时间所占百分比
8:required double cpu_nice,//以user level、nice level运行时的CPU占用率
9:required double cpu_user,//以user level运行时CPU占用率
10:required double cpu_system,//以system level运行时CPU占用率
11:required double cpu_wio,//CPU空闲或者系统有显著磁盘IO请求的时间所占百分比
12:required double part_max_used,//所有分区已经占用的百分比
13:optional double mem_used,//内存利用率
}

struct HostMoniter{
1:required Percentage percentage,
2:required double disk_free,//磁盘剩余空间
3:required i16 proc_run,//正在运行进程个数
4:required double mem_cached,//缓存容量
5:required double mem_free,//可用内存容量
6:required string mem_buffers,//缓冲内存容量
7:required string mem_shared,//共享内存容量
8:required string proc_total,//进程总数
9:required string swap_free,//可用交换内存容量
10:required double pkts_out,//每秒发出的包数
11:required double pkts_in,//每秒收到的包数
12:required double bytes_in,//每秒收到的字节数
13:required double bytes_out,//每秒发出的字节数
}

exception InvalidOperation {
  1: i32 what,
  2: string why
}

service collect{
void ping(),
string seyHello(1:string word),
string getNodeInfo(1:NodeInfo ni),
string getHostInformation(1:HostInformation hi),
string getHostMoniter(1:HostMoniter hm),
}