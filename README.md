# YuanArithmetic

小猿口算各种脚本

### 目前主流方案有三种，会慢慢增加相应的代码

1. OCR+模拟正确答案
2. 劫持数据包+模拟正确答案
3. 劫持数据包+篡改正确答案
4. Frida调试
目前V2接口已经AES加密，除了Frida和OCR都已经暂时失效
解密办法暂时没有，想继续炸鱼可以移步(这个项目)[https://github.com/xmexg/xyks]

### 如何使用

1. Clone项目
2. 安装好Python环境
3. 安装对于文件夹下面的requirements.txt内所要求的包
4. 安装TrustMeAlready
5. 配置模拟器/实体机ADB与代理
6. 运行

### 其他说明

1. 如果没有特殊说明，所有屏幕分辨率为1080*1920