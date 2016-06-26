# 项目上线操作流程

*本文档以安个家主项目为例说明上线流程，其他系统上线除了入口文件不同以外，其他类似*

安个家主项目位于<https://git.corp.angejia.com/service/angejia/>

项目上线入口在`angejia.py`文件中

用法: `angejia.py [-B] [-F] [-D] [version]`

选项:

`-B, --backend-only` 仅仅上线后端代码

`-F, --fire` 仅仅执行fire操作

`-D, --deploy` 仅仅执行deploy操作

* 若deploy参数和fire参数都没有指定,则执行deploy和fire操作
* 若没有version参数,则脚本会提示输入版本号
* 操作之前,请执行`. venv/bin/activate`

## 例子

* 对于小版本上线(没有todo)

可直接执行`python angejia.py v1.2.3`. (若仅仅为后端上线,则可以添加`-B`参数)

* 对于大版本上线(有todo)

首先执行`python angejia.py -D v1.2.3`,执行deploy操作.

执行todo

然后执行`python angejia.py -F v1.2.3`,执行fire操作.
