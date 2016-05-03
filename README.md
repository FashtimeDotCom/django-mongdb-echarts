项目需求：数据可视化，多维度展示（目前是一期）

接口人：罗俊仁

开发者：高远

上生产注意事项：

- 手动更新不方便放到GIT上的保密信息
- 检查requirement.txt是否满足
- 检查生产的配置
    - 新APP是否安装
    - STATIC_URL是否和nginx静态文件配置一致
    - collectstatic的时候STATIC_ROOT是否和STATIC_URL一致
    - wsgi.py中的setting配置是否为settings.production
    
在生产操作记得指定配置文件：
```
python manage.py migrate --setting "settings.production"
etc.
```