# 云服务器部署Django简单站点（炒鸡详细）
项目背景是测试车辆每日都需要由驾驶员手写日报并由工程师录入Excel表格，过程繁琐。
决定仅使用Django自带Admin管理系统及MySQL数据库来构建数据库，
并使用WeChat的接口通过AutoReply来自动获取数据，完成数据端到端的生成，
免去了繁杂的中间环节。这里简要记录一下站点在云服务器上的部署过程，
方便自己也方便他人使用。
***  
### 1. 部署环境与工具
* 腾讯云服务器
* Ubuntu 18.04.1 LTS
* Django 3.0.3
* Python 3.6.9
* Git
* Uwsgi
* Nginx
***
### 2. 部署Django Web并测试
#### 2.1 Python版本
Python无需安装，只需要查看版本是否满足自己的需求。Ubuntu 18.04.1
自带了Python2与Python3，在调用命令时也使用Python与Python3来区分，
如果想让Python命令自动调用3.X版本的Python解释器，可以执行以下命令。
下方的命令并未删除原有的版本，因为系统底层很多依赖于该原生版本。我们
只是删除了Python link并将Python3 link连接到Pyhton link上（好绕口）。
```
python --version
python3 --version
sudo rm -rf /usr/bin/python
sudo ln -s /usr/bin/python3  /usr/bin/python
```
修改完link后再查看版本：
```
python --version
python3 --version
```
#### 2.2 安装Pip
炒鸡简单直观：
```
sudo apt-get install python3-pip
pip3 --version
```
#### 2.3 安装并建立虚拟环境
虚拟环境有利于包的管理，这里选用Virtualenv，当然也可以用Conda什么的。  
安装并建立连接：  
```
pip3 install virtualenv #我这里遇到点问题,之前部署都没问题的
sudo apt install virtualenv #采用的这种
```  
可以使用ubuntu用户而非root，这样使用```cd ~```命令时可以回到
```/home/ubuntu/```目录下，麻烦是安装删除命令要加上```sudo``` 
不在意这点的可以直接使用root用户```sudo su```。下面建立并启动虚拟环境：
```
cd /home/ubuntu/
mkdir VMSProject
cd VMSProject #以上三步环境调整，根据自己情况定
virtualenv -p /usr/bin/python3 django_env #指定虚拟环境的python版本
ls #check established
source django_env/bin/activate #activate env
```
#### 2.4 安装git下载Web应用
安装（下面的操作均以root用户在env下操作）：
 ```
 apt-get install git
 ```
 我跟django_env平行建立了一个mysite文件夹，下载网站([仓库地址](https://github.com/zsqzsq1993/VehicleManagement))：
 ```
 cd mysite
 git init
 git remote add origin https://github.com/zsqzsq1993/VehicleManagement.git
 git pull origin master
 ls #check all files download
 ```
 #### 2.5 安装依赖包
 在本地开发的Pycharm项目中，可以采用以下两种方法来生成依赖包的目录文件：
 * 有使用虚拟环境的：
 ```
 pip freeze>requirment.txt
 ```
 * 未使用虚拟环境的或只想记录导入了的包（推荐）：
 ```
 pip install pipreqs
 pipreqs 
 ```
下面安装之前在本地生成的requirements.txt：
```
pip3 install -r requirements.txt
```
#### 2.6 安装MySQL
MySQL版本还挺多的，这里选用还比较新的MySQL 8.0版本。这个版本暂时还无法从pip或apt上直接得到。
因此，先用wget下载储存库软件包到本地：
```
wget -c https://dev.mysql.com/get/mysql-apt-config_0.8.10-1_all.deb

```
然后安装：
```
sudo dpkg -i mysql-apt-config_0.8.10-1_all.deb
```
会出现一个简陋的画面，选取默认的ok，enter，然后就会报大概是这样的错误：
```
W: GPG 错误：http://repo.mysql.com/apt/ubuntu bionic InRelease: 下列签名无效： EXPKEYSIG 8C718D3B5072E1F5 MySQL Release
Engineering <mysql-build@oss.oracle.com>
E: 仓库 “http://repo.mysql.com/apt/ubuntu bionic InRelease” 没有数字签名。
N: 无法安全地用该源进行更新，所以默认禁用该源。
N: 参见 apt-secure(8) 手册以了解仓库创建和用户配置方面的细节。
W: GPG 错误：http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 Release: 下列签名无效： EXPKEYSIG 58712A2291FA4AD5
MongoDB 3.6 Release Signing Key <packaging@mongodb.com>
E: 仓库 “http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 Release” 没有数字签名。
N: 无法安全地用该源进行更新，所以默认禁用该源。
N: 参见 apt-secure(8) 手册以了解仓库创建和用户配置方面的细节。
```
可以通过缺少哪个key，添加哪个key来解决：
```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8C718D3B5072E1F5
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 58712A2291FA4AD5
```
更新apt储存库并开始安装，时间还挺久的(大概20min)，比pip直接安装时间久了很多，估计是更加完整。
使用pip安装方法安装的版本里并不带mysqlclient或pymysql之类的连接MySQL和Python的包，需要手动安装。
```
sudo apt update
sudo apt-get install mysql-server
```
然后就是进入数据库，创建一个非root用户并设置密码；
建立django所需要的数据库，库名要与setting.py中对应；
并赋予新设用户处理该库的所有权限：
```
mysql -u root -p #接着输入密码
create database VMS default character set utf8 collate utf8_general_ci;
create user zsqzsq1993 identified by 'zsqzsq1993';
grant all privileges on *.* to zsqzsq1993;
flush privileges;
```
#### 2.7 启动并简单测试你的Web应用
还是需要安装mysqlclient，用来连接mysql与python。
总结就是废了一大把劲从官网安装MySQL不如直接从apt直接安装。
安装mysqlclient，在这之前还要安装一大堆依赖库：
```
sudo apt-get install libmysqld-dev
##sudo apt-get install libmysqlclient-dev
apt-get install build-essential python3-dev libssl-dev libffi-dev libxml2 libxml2-dev libxslt1-dev zlib1g-dev
pip3 install mysqlclient
```
一切准备就绪！准备测试啦。注意ip地址留0.0.0.0:80意思是运行
任何ip地址通过该主机的80号端口来传入请求。
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80
```
如果通过互联网访问，后端能显示联通正常就说明没有问题啦！
接下来就要思考如何使用Uwsgi和Nginx来进行网站管理。
其实我也不清楚为何runserver不适合用做生产环境。
Any way, Let's continue...
***
### 3. Uwsgi
```
pip3 install uwsgi
uwsgi --http :8888 --chdir /home/ubuntu/VMSProject/mysite --home /home/ubuntu/VMSProject/django_env --module VehicleManagement.wsgi:application
```
To be continued...
