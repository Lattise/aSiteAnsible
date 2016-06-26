#  项目目录结构

- `cache` 缓存es、logstash等软件的安装包
- `docs` 项目文档
- `group_vars` 各个inventory组的变量声明
- `repos` 各个项目的代码库
- `roles` 各个角色
  - `config` 配置机器使用的角色
  - `deploy` 发布项目使用的角色
- `<proj>.yml` 项目使用的playbook
- `<proj>.py` 项目发布入口
- `hosts` ansible使用的inventory文件
- `requirements.txt` 项目依赖
