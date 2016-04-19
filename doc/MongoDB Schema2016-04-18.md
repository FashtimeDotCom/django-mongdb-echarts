# MongoDB Schema

##数据库

udb

##collections

t_db_instance

##Replicaset

172.17.10.34:27017
172.17.10.35:27017
172.17.10.36:27017

###账户

UserName: ucloud
Password: ucloudreadonly

## 字段

|  Parameter name | Type   | Description  | Required  |
|---|---|---|---|
| Region | String   | 机房名称 | Yes  |
| AzGroup | String | 可用区名称   | Yes  |
| DBId | String   | UDB实例Id  | Yes  |
| VirutalIP | String   | UDB实例的IP | No  |
| InstanceMode | String   | UDB实例模式:<br /> HA - 高可用<br /> Normal - 普通版<br /> | Yes  |
| ClusterId | String   | UDB实例集群Id, 如果DB实例为高可用UDB实例的组成DB实例, 方有此字段 | No  |
| Role  | String  | DB角色:<br /> master - 主<br />slave - 从<br />unknown - 未知<br />  | Yes  |
| SrcDBId | String   | 如果UDB实例为从库，该字段标识为主库的DBId  | No  |
| State  | String  | DB实例当前状态:<br /> Init - 初始化<br /> Fail - 安装失败<br /> Starting - 启动中<br /> Running - 运行中<br /> Shutdown - 关闭中<br /> Shutoff - 已关闭<br /> Delete - 已删除<br />  Upgrading - 升级中<br /> Promoting - 提升为独立库运行中<br /> Recovering - 恢复中<br /> Recover fail - 恢复失败<br />| Yes  |
| DBClass  | String | DB分类: <br /> MySQL<br /> MongoDB<br /> | Yes  |
| DBType  | String | DB版本: <br /> MySQL-5.1<br /> MySQL-5.5<br />MySQL-5.6<br />MongoDB-2.4<br />MongoDB-2.6<br /> Percona-5.5<br /> Percona-5.6<br /> | Yes  |
| CreateTime  | ISODate  | 创建时间  | Yes  |
| ModifyTime | ISODate  |  变更(删除)时间 | Yes  |
| CreateWeek  |  Integer | 当年创建周数  | Yes  |
| ModifyWeek | Integer  |  当年变更(删除)周数 | Yes  |
| CreateMonth  | Integer  | 当年创建月份  | Yes  |
| ModifyMonth | Integer  |  当年变更(删除)月份 | Yes  |
| DiskType| String  | 磁盘类型: <br />Normal - 普通硬盘<br />SATA-SSD - SATA型SSD<br />PCIE-SSD - PCIE型SSD  | Yes  |
| DiskSpace  | Integer  | 磁盘空间(GB)  | Yes  |
| MemoryLimit  | Integer  | 内存限制(MB)  | Yes  |
| Industry  | String  | 行业  | Yes  |
| Manager  | String  | 客户经理  | Yes  |
| CompanyName  | String  | 客户公司名  | Yes  |
| CompanyId  | Integer  | 客户公司Id  | Yes  |
| InnerMark | String | 是否为内部用户资源:<br /> Yes - 内部用户<br /> No - 外部用户<br /> unknown - 没有获取到用户信息<br /> | Yes |





