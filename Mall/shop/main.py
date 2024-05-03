# import os
# import sys
#
# path = os.path.dirname(sys.path[0])
# print(path)
# if path and path not in sys.path:
#     sys.path.append(path)  # 将当前目录添加到系统环境变量中

from shop import create_app

app = create_app('develop')

if __name__ == '__main__':
    app.run(debug=True)
