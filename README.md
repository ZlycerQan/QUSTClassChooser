# QUSTClassChooser
QUST Class Chooser


本脚本会在经过`fliter`和`kcgs`筛选后的课程中查询有余量的课程并依次尝试选课。

选课成功会退出脚本，否则继续尝试

在`config.json`中配置

`base_url`: 服务器地址

`su`: 学号

`cookie`: 登录cookie

`filter`: 搜索框

`kcgs`: 课程归属，请务必配置完整且准确的名称

`page_interval`: 通过`[点击查看更多]`获取更多课程的时间间隔，单位毫秒

`if_rand`: 随机刷新时间间隔，0为关闭，1为开启，若为1，则必须配置`randl`, `randr`，若为0，则必须配置`interval`

`interval`: 固定刷新时间间隔，单位毫秒

`randl`: 随机间隔的下边界，单位毫秒

`randr`: 随机间隔的上边界，单位毫秒

>注意：
使用者须自行检查`config.json`中的参数是否正确 

> **脚本使用导致的后果由脚本使用者自行承担** 