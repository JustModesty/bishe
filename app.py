from flask import Flask, session, redirect, url_for, request, render_template
from flask_script import Manager

app = Flask(__name__)
# 这一句方便开发
app.config['DEBUG'] = True
manager = Manager(app)

# 主页，输入URL之后的页面，显示按钮《开始爬取》 《显示数据》 《清空数据》
@app.route('/')
def index():
    return render_template('index.html', title="欢迎使用")


# “开始爬取” 接口
@app.route('/start_spider')
def start_spider():
    return render_template('start_spider.html')


# “网站首页” 接口
@app.route('/gdut_index')
def gdut_index():
    return render_template('gdut_index.html')


# “清空数据” 接口
@app.route('/clear_data')
def clear_data():
    return render_template('clear_data.html')


# 方便开发，自动同步浏览器
@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url_delay=True)
    

if __name__ == '__main__':
    # 正常模式
    # app.run()

    # 调试模式
    # app.run(debug=True)

    # 方便开发，自动同步更新浏览器
    manager.run()
    