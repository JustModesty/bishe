# bishe
# 正常模式下的启动方式
```
python app.py
```

## 调试模式的启动方式(Web页面自动刷新，方便开发)
```
python manage.py dev
```

## 自动抓取Mysql数据库,并在/app/models.py创建ORM的命令
```
flask-sqlacodegen 'mysql+pymysql://帐号:密码@127.0.0.1/数据库名' --outfile "app/models.py" --flask
``` 