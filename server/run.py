import os
import sys


sys.path.append(os.getcwd())

framework = 'flask'
_host = '0.0.0.0'
_port = 8082

print('********************************************************')
print(' FRAMEWORK: ', framework)
print(' HOST: ', _host)
print(' PORT: ', _port)
print('********************************************************')


if framework == 'flask':
    from server.main_ import app

    app.run(host=_host, port=_port)

