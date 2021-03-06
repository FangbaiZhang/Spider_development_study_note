# Python爬虫开发与项目实战(学习笔记)

- This project is a study note of Spider Development ans Project Training.
- 本项目是爬虫开发与项目实战的学习笔记.

- 前面几章很多都是学习过的内容，快速浏览
- 参考书本和TLXY_study_note中的内容


# 1 第一章 回顾Python编程
- 案例放置在ch01之中

## 1.4 进程与线程

- 进程与线程的区别

- 进程：程序运行的一个状态
    - 包含地址空间，内存，数据栈
    - 每个进程有自己独立的运行环境
    - 多进程共享数据是一个问题

- 线程
    - 一个进程的独立运行片段，一个进程可以有多个线程
    - 轻量化的进程
    - 一个进程的多个线程共享数据和上下文运行环境
    - 共享互斥问题

- 多进程使用multiprocessing模块
- 多线程使用threading模块
    
 
### 1.4.1 多进程
- 使用multiprocessing模块创建多进程
    - 使用multiprocessing模块中的Process创建少量的多进程
    - 创建子进程，函数只需要执行函数的名称和执行函数的参数即可
    - 参考实例1.4.1 

- 大量进程，上千上万个进程使用multiprocessing模块中的Pool类
    - 创建进程池对象
    - Pool默认的进程数量是CPU的核数或者规定的进程数量
    - 如果池中的进程没有满，就会自动创建进程
    - 如果池中已满或者达到规定数量，进程就会等待，池中进程结束一个，才会创建新的进程 
    - 先创建Pool()实例，然后用apply_async()创建子进程
    - 进程池使用join()函数之前，需要先调用close()函数，然后所有任务就自动开始了，关闭某个进程
    - 相对于Process,不需要执行start()函数
    - 使用用close()之后，就不能再添加Process子进程了
    - 然后下一个进程在开始进程，具体参考实例
    - 参考实例1.4.2

- 进程之间的通信
    - 两个进程使用Pipe
    - 多个进程使用Queue
    - Queue实际就是一个安全队列
    - Queue提供了一个基本的FIFO容器,
    - Queue有两个方法Put和Get
    - put()方法向容器中存入数据，按顺序存入
    - get()方法从容器中取出数据，按循序取出
    - 参考实例1.4.3/1.4.4

- 队列补充知识：
    - queue.Queue()
    - 基本队列，先进先出
    - 参考1.4.3_1
    - LIFO队列，后进先出
    - 参考1.4.3_2

- multiprocessing.Queue()和queue.Queue()的区别
    - 参考：https://blog.csdn.net/u011318077/article/details/88089843
    - 参考：https://www.cnblogs.com/itogo/p/5635629.html
     
    
### 1.4.2 多线程
- threading模块
- 方法1：创建Thread实例
- 方法2：直接继承threading.Thread类
- 参考书中案例
- 参考TLXY_study_note中的高级语法，多线程

### 1.4.3 协程
- 可以使用yield生成器实现
- 推荐使用gevent包,用于请求访问多个网址或者网络请求
- 使用gevent.spawn和gevent.joinall方法添加启动多个协程
- 参考实例1.4.5

- 处理大量的网络请求和并发出处理
- gevent提供的池，对并发数进行管理限制
- 使用pool.map执行任务
- 参考实例1.4.6

### 1.4.4 分布式进程
- multiprocessing模块
- managers子模块支持把多个进程分布到多台机器上
- 可以写一个服务进程作为调度者，将任务分布到其它多个进程中，然后通过网络通信进行管理
- 比如爬取图片：一般一个进程负责抓取图片的地址，将地址放在Queue（容器）队列中
- 另外一个进程负责从Queue队列中取出链接地址进行图片下载和存储到到本地
- 上述爬取图片的过程就可以做成分布式，一台机器负责获取链接，另外一台机器负责下载存储
- 上述问题核心：将Queue队列暴露到网络中，让其他机器可以访问

- 分布式进程的步骤
    - 建立Queue队列,负责进程之间的通信，任务队列task_queue,结果队列result_queue
    - 把第一步中的两个队列在网络中注册,注册时候将队列重新命名
    - 创建一个Queuemanager(BaseManager)的实例manager，相当于一个服务器，给定IP地址、端口和验证码
    - 启动实例manager
    - 访问Queue对象，即创建网络中暴露重命名后的Queue实例
    - 创建任务到本地队列中，自动上传任务到网络队列中，分配给任务进程进行处理
    - 任务进程先从网络中任务队列中取出任务，然后执行，将执行结果放入到网络中的结果队列中
    - 服务进程从结果队列中取出结果，直到执行完所有任务和取出所有的结果，任务进程关闭，然后服务进行关闭

- 先创建服务进程，再创建任务进程
- 参考实例1.4.7 1.4.8 运行正常
-
- 案例补充知识
- 知识补充1
    当我们在一台机器上写多进程程序时，创建的Queue可以直接拿来用，但是，在分布式多进程环境下，
    添加任务到Queue不可以直接对原始的task_queue进行操作，那样就绕过了QueueManager的封装，
    必须通过manager.get_task_queue()获得的Queue接口添加。
    然后，在另一台机器上启动任务进程（本机上启动也可以）

- 知识补充2
    其中task_queue和result_queue是两个队列，分别存放任务和结果。它们用来进行进程间通信，交换对象。
    因为是分布式的环境，放入queue中的数据需要等待Workers机器运算处理后再进行读取，
    QueueManager.register(‘get_task_queue’, callable=return_task_queue)
    QueueManager.register(‘get_result_queue’, callable=return_result_queue)
    这样就需要对queue用QueueManager进行封装放到网络中，这是通过上面的2行代码来实现的。
    我们给return_task_queue的网络调用接口取了一个名get_task_queue,
    而return_result_queue的名字是get_result_queue，
    方便区分对哪个queue进行操作。task.put(n)即是对task_queue进行写入数据，
    相当于分配任务。而result.get()即是等待workers机器处理后返回的结果。

- 知识补充3
    这个简单的Master/Worker模型有什么用？其实这就是一个简单但真正的分布式计算，把代码稍加改造，
    启动多个worker，就可以把任务分布到几台甚至几十台机器上，
    比如把计算n*n的代码换成发送邮件，就实现了邮件队列的异步发送。
    Queue对象存储在哪？注意到task_worker.py中根本没有创建Queue的代码，
    所以，Queue对象存储在taskManager.py进程中：
    参考图片分布式进程
    
    而Queue之所以能通过网络访问，就是通过QueueManager实现的。
    由于QueueManager管理的不止一个Queue，所以，要给每个Queue的网络调用接口起个名字，
    比如get_task_queue。taskWorker这里的QueueManager注册的名字必须和taskManager中的一样。
    对比上面的例子，可以看出Queue对象从另一个进程通过网络传递了过来。
    只不过这里的传递和网络通信由QueueManager完成。

    authkey有什么用？这是为了保证两台机器正常通信，不被其他机器恶意干扰。
    如果task_worker.py的authkey和taskManager.py的authkey不一致，肯定连接不上。
    
    参考文章：https://blog.csdn.net/u011318077/article/details/88094583 
    

    
## 1.5 网络编程
- TCP协议：服务器端与客户端要建立可靠的连接
- UDP协议：服务器端与客户端不需要建立连接
- 参考书本内容和TLXY_study_note中的高级语法，网络编程


# 2 第2章 Web前端基础
- 省略
- 参考书本内容和TLXY_study_note中的高级语法和Spider中的内容

# 3 第3章 初始网络爬虫
- 省略
- 参考书本内容和TLXY_study_note中的高级语法和Spider中的内容

# 4 第4章 HTML解析大法
- 省略
- TLXY_study_noteSpider中有详细的BS4使用教程和案例
- 参考书本内容和TLXY_study_note中的高级语法和Spider中的内容

# 5 第5章 数据存储
## 5.1 HTML正文抽取
### 5.1.1 HTML内容存储为JSON格式
- 参考实例5.1.1 
## 5.3 Email提醒
- Python发送邮件提醒
- 用途：爬虫自动爬取出现问题后可以自动发送提醒邮件
- 参考实例5.3

# 6 第6章 实战项目：基础爬虫
## 6.1 基础爬虫结构及运行流程
- 参考ch06中的实例
- HtmlParser解析器中，百度百科连接发生了变化进行了相应修改

# 7 第7章 实战项目：简单分布式爬虫
- 参考ch07中的实例
- NodeManager控制调度器，导入DataOutput和URLManager时候
    - 由于在同一个文件夹,并且添加了init文件，采用相对路径应该可以导入，但是导入出错
    - 将ch07文件加入系统路径，然后用绝对导入，可以解决问题
    - 参考博文：https://blog.csdn.net/u011318077/article/details/88061972
    
# 8 第8章 数据存储（数据库版）
- 参考书中内容
- 同时参考菜鸟教程：
- http://www.runoob.com/sqlite/sqlite-tutorial.html
- http://www.runoob.com/mongodb/mongodb-tutorial.html

- MongoDB常用命令
    
    - 一个MongoDB数据库系统注册服务后，可使用以下命令启动
    - 启动MongoDB服务 net start MongoDB 管理员打开CMD窗口
    - 关闭MongoDB服务 net stop MongoDB
    
    - 注意，以上方式只是将数据库mongoDB文件夹注册成服务，
    - 新数据库需要再次注册，才能使用net start xxxname命令
    
    - 启动服务后，新打开一个CMD窗口，输入mongo启动shell调试窗口
    - 退出shell调试窗口：ctrl+c 或者exit
    - show dbs 查看所有的数据库
    - db 查看当前的数据库
    - use database_name 创建一个名称为database_name的数据库，如果本来就有，就直接切换到该数据库
    - 上面新建数据库，show dbs查看里面并没有，由于数据库是空的，所以不会显示
    - db.database_haha.insert({"name":"haha"}) 向数据库中插入数据
    - 再次查看，有了该数据库
    - db.dropDatabase()  删除当前数据库
    - db.python.insert({title: 'python',likes: 100})  插入python集合，数据是json格式
    - db.python.find() 查找文档。可以使用条件语句
    - 参考书中内容和ch08中的图片
    
    
    


# 9 第9章 动态网站抓取
- 9.2 动态网站采集需要分析网页请求中网络中的JS数据，比较复杂不推荐
- 9.3 PhantomJS已经不更新了，直接看9.4，推荐使用Selenium+Firefox/Chrome
    - 参考以前TLXY的动态HTML的笔记和实例
    - 参考我博文：https://blog.csdn.net/u011318077/article/details/86644430
    - 参考9.4中的实例
- 9.4 Selenium+Firefox操作浏览器，一些常用操作和查找方法
    - 参考实例
- 9.5 动态爬虫：爬去哪儿网

# 10 第10章 Web终端协议分析
- 网页登录POST分析
- 验证码问题
- 参考书本

# 11 第11章 终端协议分析
- PC客户端分析
- APP端抓包分析
- 两个工具：HTTP analyzer 和 Wireshark
- 关键通过抓包分析找到电脑客户端或者手机端的API接口，用于开始爬虫
- 实例：爬取酷我听书APP上的资源信息
- 看书和实例

# 12 第12-16章 看书和章节实例

## 16.2.2 scrapy-redis分布式爬虫
- scrapy-redis分布式爬虫
    - 参考书中类容和以下网址、最终看sht爬虫改造成分布式爬虫实例，爬虫内部都有备注
    - https://www.cnblogs.com/pythoner6833/p/9148937.html
    
    - redis启动步骤
    - 第一步：先CMD启动redis-server服务器端
    - 第二步：再打开一个CMD窗口，输入redis-cli,启动Redis客户端
    
    - 分布式爬虫，参考sht爬虫
        - 修改settings文件中的相关配制，主要是修改ITEM_PIPELINES和末尾中添加scrapy-redis相关的内容
        - 修改sht_spider主程序，主要是类继承改变，起始url设置变化，爬虫程序中设置键的名称
        - 先启动redis服务器，然后再打开一个CMD窗口，运行redis-cli,连接到服务器，
        - 然后进入到CMD窗口中设置键和值作为起始URL
        - 启动主程序，如果有新的URL，直接在服务器中设置，参考出ch16中的图片和pdf文件
        
        # 注意，改造成分布式爬虫后，传人URL，已经爬取过的ITEM会存储在本地服务器中
        # 可以在redis中输入keys * 查看所有的键
        # 使用flushall可以删除所有本地所有的键值数据
        # 删除数据后再次传入起始URL，然后启动爬虫，就可以开始爬取
        # 注意：分布式爬虫，redis服务器一直处于运行状态，爬虫不会自己结束，
        # 可以向服务器一直传入新的URL，然后爬虫会自动继续爬取新的URL，重复的会自动跳过
        
        - 爬取完成后，手动结束爬虫主程序即可
        
# 16.2 MongoDB复制（副本集）（版本V4.0.7)图文教程
- 参考文章：
    - [MongoDB副本集（一）](https://blog.csdn.net/u014785687/article/details/54170724)
    - [MongoDB 复制（副本集）-菜鸟教程](http://www.runoob.com/mongodb/mongodb-replication.html)
    - [MongoDB 副本集的原理、搭建、应用](https://www.cnblogs.com/zhoujinyi/p/3554010.html)
- 注意：图片放在ch16文件夹之中

- 参考书中：P198和P399相关内容和标注

- MongoDB服务器的启动方式：
    - P198中MongoDB有三种启动方式：
    - 第一种：CMD窗口命令行启动，启动命令详细参数参考书中箭头指向的表格
    - 第二种：启动命令做成批处理文件
    - 第三种：MongoDB注册成一个服务，然后使用CMD窗口直接执行net start mongodb(注意mongodb为数据库文件夹名称)
    - 推荐直接使用第一种方法，如果只有一个经常使用的数据库，推荐第三种方法
    - 副本集三个服务器启动推荐直接使用第一种方法

- 什么是副本集？
    - 副本集是一组服务器，其中有一个主服务器(primary),用于处理客户端请求；
    - 还有多个备份服务器(secondary),用于保存主服务器的数据副本。
    - 如果主服务器崩溃了，备份服务器会自动将其中一个成员升级为新的主服务器。 
    - 使用复制功能时，如果有一台服务器宕机了，仍然可以从副本集的其他服务器上访问数据。
    - 如果服务器上的数据损坏或者不可访问，可以从副本集的某个成员中创建一份新的数据副本。

- 副本集中数据同步过程：
    - Primary节点写入数据，Secondary通过读取Primary的oplog得到复制信息，
    - 开始复制数据并且将复制信息写入到自己的oplog。如果某个操作失败，则备份节点停止从当前数据源复制数据。
    - 如果某个备份节点由于某些原因挂掉了，当重新启动后，就会自动从oplog的最后一个操作开始同步，
    - 同步完成后，将信息写入自己的oplog，由于复制操作是先复制数据，复制完成后再写入oplog，
    - 有可能相同的操作会同步两份，不过MongoDB在设计之初就考虑到这个问题，将oplog的同一个操作执行多次，
    - 与执行一次的效果是一样的。
    - 简单的说就是：
        当Primary节点完成数据操作后，Secondary会做出一系列的动作保证数据的同步：
        1：检查自己local库的oplog.rs集合找出最近的时间戳。
        2：检查Primary节点local库oplog.rs集合，找出大于此时间戳的记录。
        3：将找到的记录插入到自己的oplog.rs集合中，并执行这些操作。

- 副本集的实现过程
- 副本集创建步骤：

- 第一步：创建数据存储的文件夹
    - 在H盘下新建三个文件夹作为存储数据的文件夹，文件夹名称：mongo1、mongo2、mongo3
    - 每个文件夹内部创建一个data文件夹，然后data文件夹里面创建一个db文件夹
    - 参考图片：1601-数据文件夹创建，注意我的图片中data中已经有数据，是因为我的副本集已经创建过了
    - 你们第一次创建，data里面只有db文件夹
    - 参考图片：1601
    
- 第二步：启动MongoDB服务器（每次都要启动这三个服务器）
    - 打开第一个CMD窗口，执行以下命令，启动第一个mongodb服务器
    - mongod --port 1111 --dbpath H:\mongo1\data --replSet test --logappend
    - 打开第二个CMD窗口，执行以下命令，启动第二个mongodb服务器
    - mongod --port 2222 --dbpath H:\mongo2\data --replSet test --logappend
    - 打开第三个CMD窗口，执行以下命令，启动第三个mongodb服务器
    - mongod --port 3333 --dbpath H:\mongo3\data --replSet test --logappend
    - 第一个mongodb服务器启动成功后会显示一些系统版本之类的信息
    - 第二个和第三个mongodb服务器启动后，CMD窗口最后一句命令中会显示port接口和等待连接的信息
    - 参考图片：1602-启动三个MongoDB服务器
    
- 第三步：连接MongoDB服务器，启动mongodb的shell调试窗口
    - 打开第四个CMD窗口，执行以下命令，连接到一个mongodb服务器
    - mongo --port 1111
    - 此处是连接到1111端口的服务器（连接其他端口也可以）
    - 每次启动mongodb服务器，主服务器可能会不一样，如果连接的是主服务器
    - 开始连接到mongodb服务器，不一定是主服务器，但是shell操作过程中，
    - 一般会变成服务器，只有主服务器才能进行写入操作
    - shell调试的前缀会变成：test:PRIMARY>,可以参考之后的图片中内容
    - 参考图片：1603-连接MongoDB服务器启动mongo调试窗口
    
- 第四步：初始化副本集
    - 创建一个配置文件，在配置文件中列出每一个成员，
    - 让他们每个人都知道知道彼此的存在(第二次启动及以后就不需要再配置)
    - 先使用一个空的数据库test（自带的默认数据库）,注意：第二步启动服务器--replSet后面的名称(test)是副本集的名称
    - 然后再输入配置文件，然后初始化配置文件
    - 具体命令依次如下,没输入依次命令，按下Enter(config_test会转变为swconfig_test)：
    - use test
    - config_test={"_id":"test","members":[{"_id":0,host:"127.0.0.1:1111"},{"_id":1,host:"127.0.0.1:2222"},{"_id":2,host:"127.0.0.1:3333"}]}
    - rs.initiate(config_test)
    - 参考图片：1604-初始化副本集
    - 注意：其中的”_id”值就是第二步中每一个服务器启动时副本集的名字--replSet后面的名称，(“test”)，这个名称要保持一致。 
    - 将这个配置文件发送给其中一个副本集成员，然后该成员会负责将配置文件传播给其他成员，
    - 如果副本集中已经有一个有数据的成员，那就必须将配置对象发送给这个拥有数据的成员，
    - 如果拥有数据的成员不止一个，那么就无法初始化副本集，因此我们开始第一步就是建立的三个空文件夹，保证里面没有数据。

- 第五步：查看副本集状态
    - rs.status()
    - 参考图片1605/1606/1607-查看副本集状态
    - 图片中可以发现，在查看状态之前还是显示为test:SECONDARY> 
    - 查看状态之后已经变成了主服务器，test:PRIMARY>
    
- 第六步：再次登录副本集
    - 先执行exit,退出shell调试模式，然后关闭四个CMD窗口
    - 分别打开三个CMD窗口，执行第二步中的三个命令，启动MongoDB服务器副本集    
    - 注意：启动第一个服务器后，CMD窗口会不断的显示连接port2222和3333接口，
    - 但由于还未启动，一直未连接成功，都启动后，就会显示正常
    - 参考图片：1608/1609
    - 启动后，打开第四个CMD窗口，连接主服务器1111，执行以下命令
    - mongo --port 1111
    - 第二次启动，可以直接查看状态信息，不需要在设置配置文件。 
    - 以此运行以下命令，查看主服务器和备份服务器（主从节点）的相关信息： 
    - use test
    - db.isMaster()
    - 查看主副节点信息也可以执行：rs.config()
    - 参考图片：1610
    
- 第七步：检查主副节点数据是否同步
    - 第六步已经再次登录了副本集，主节点写入数据，然后主节点查看数据，依次执行以下命令 
    - use test
    - db.testdb.insert({"test1":"Felix"})
    - show tables
    - db.testdb.find()
    - 退出主节点，然后登陆一个副节点，先查看数据是否复制过来,会出现错误提示
    - mongodb默认是从主节点读写数据的，副本节点不允许读，读取数据，需要设置标识
    - 注意，每个副节点都需要设置标识才能读取数据，设置标识命令如下
    - db.getMongo().setSlaveOk()
    - 对于不是副本集中的备份节点（可能之前被删除了，它的前缀变成 test:other），是不能查询到写入的数据.
    - 不能对备份节点执行写入操作，备份节点只能通过复制功能写入数据，不接受客户端的写入请求
    - 参考图片：1611/1612/1613

- 第八步：副本集添加和删减成员
    - 副本集创建后，主节点窗口下，执行以下命令可以添加成员
    - rs.add("127.0.0.1:4444")
    - 删除成员
    - rs.remove("127.0.0.1:4444")
    - 然后运行以下命令之一查看主副节点信息
    - rs.config()
    - db.isMaster()
    - 参考图片：1614
    
- 第九步：修改副节点配置信息
    - 为了修改副本集成员，采用rs.config()可以创建新的配置文档，
    - 然后调用rs.reconfig()方法，将刚刚的第三个副节点的接口修改，以此执行以下命令
    - var config=rs.config()
    - config.members[3].host="127.0.0.1:5555"
    - rs.reconfig(config)
    - 参考图片：1615
    
- yunqi书院
    - 连接到主服务器
    - show dbs 显示说有数据库
    - use yunqi 使用yunqi数据库
    - show tables 显示里面所有的数据集

    - 运行结果如下   
    test:PRIMARY> show dbs
    admin   0.000GB
    config  0.000GB
    local   0.001GB
    test    0.000GB
    yunqi   0.001GB
    test:PRIMARY> use yunqi
    switched to db yunqi
    test:PRIMARY> show tables
    bookInfo
    bookhot
    test:PRIMARY>
     
    
    


    



    







