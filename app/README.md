# app上传流程

注意，为保证兼容性，在这些操作之后，不要忘记将包上传到lb机器后再切换更新版本。

# 上传

````shell
./upload.py [type] [platform] [version] [file]
````

- `type`取值现在只能为`broker`
- `version`为版本,比如`v1.2.3`
- `platform`可以是`android`或者`ios`

file的下载地址将会是`https://o05q49bme.qnssl.com/app/<type>/version/<type>.(ipa|apk)`

比如:

- `https://o05q49bme.qnssl.com/app/broker/v1.2.3/broker.ipa`
- `https://o05q49bme.qnssl.com/app/broker/v1.2.3/broker.apk`

# 切换下载版本

由于上传到七牛的文件会遇到缓存问题，故我们需要做一次302跳转。

现在约定如下：

`app/broker/broker.ipa`总是302到最新的ios app,`app/broker/broker.apk`总是302到最新的android app

````shell
./checkout.py [type] [platfrom] [version]
````

将最新的下载地址指向到特定版本。
