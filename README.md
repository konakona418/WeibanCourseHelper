# 安全微伴课程一键学习

>
> Takedown Email: 参见本人主页。
> 考虑到本人的反骚扰策略，不保证一定看得到邮件。
>

## 简介

一键学习安全微伴所有课程，拯救你的假期！

如果你想要一键考试满分，请使用成熟的项目，参见：[安全微伴考试助手](https://github.com/kmoonn/Weiban-Tool)。

## 现有功能

登录方面，支持使用账号密码登录，也支持直接输入 token。

自动学习方面，目前已经支持单账号一键学习，异步实现，效率更高。

## 使用方法

1. clone 此项目
2. 在项目目录下执行 `pip install -r requirements.txt`
3. 修改 `config.ini` 中常量为合适值（一般只需要修改要进行的任务数）
4. 在项目目录下执行 `python main.py`
5. 选择模式，若选择了输入账号密码，则会弹出一个显示验证码的 PyTk 窗口，关闭窗口前不要输入内容
6. 关闭窗口，按照提示继续输入
7. 程序自动扫描进行中的学习任务，自动完成

## TODO
- [x] 异步获取课程列表
- [x] 不基于 Python 文件的配置文件
- [x] 账号信息存储
- [ ] 多账号支持
- [ ] GUI

## 致谢
- 结束学习 API jQuery 字符串格式基于 [pooneyy/weiban-tool](https://github.com/pooneyy/weiban-tool/blob/9922cd34b3b85af89490c65bad924a3c94e3aa7c/Utils.py#L198) 的相关代码
- 结束学习延时时长数据一部分参考了 [pooneyy/weiban-tool](https://github.com/pooneyy/weiban-tool/)
- 部分时间戳特殊要求与传递关系受 [Coaixy/weiban-tool](https://github.com/Coaixy/weiban-tool) 启发
