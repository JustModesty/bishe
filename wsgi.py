from app import create_app


application = create_app('production')

# 这一句方便开发
# manager = Manager(app)


if __name__ == '__main__':
    try:
        application.run()
    except :
        application.run()
