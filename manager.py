# -*- coding: utf-8 -*-
# from flask_script import Manager
# from app import create_app
#
#
# app = create_app()
#
# # 这一句方便开发
# manager = Manager(app)
#
#
# # 方便开发，自动同步浏览器
# @manager.command
# def dev():
#     from livereload import Server
#     live_server = Server(app.wsgi_app)
#     live_server.watch('**/*.*')
#     live_server.serve(open_url_delay=True)
#
#
# if __name__ == '__main__':
#     try:
#         manager.run()
#     except :
#         manager.run()

# ====================deletable=====================================================
from flask_script import Manager
from app import create_app


app = create_app()



if __name__ == '__main__':
    app.run(debug=True,threaded=True)