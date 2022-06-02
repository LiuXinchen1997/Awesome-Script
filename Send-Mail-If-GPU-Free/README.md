# Send-Mail-If-GPU-Free

1. 本脚本基于163邮箱，运行前需要先开启163邮箱的POP3/SMTP服务，并修改如下代码，其中`password`表示开启POP3/SMTP服务时客户端提供的授权码，不是163邮箱的登录密码。

    ```Python
    sender = "<your_163_email_address>"
    recver = "<your_163_email_address>"
    password = "<your_password>"
    ```

2. GPU使用信息的获取依赖正则表达式的匹配，因此如果脚本运行有问题，可能需要适当修改正则规则以适配你的环境。