from controller import app
import cherrypy
import signal

# host = 'localhost'
host = '0.0.0.0'
port = 80

def stop_server(*args, **kwargs):
    cherrypy.server.stop()


cherrypy.tree.graft(app, '/')

signal.signal(signal.SIGINT,  stop_server)
cherrypy.config.update({
    "server.socket_host": host,
    "server.socket_port": port,
    "server.thread_pool": 30,
#cherrypy.server.ssl_module = 'builtin'
    "tools.encode.on": True
})
cherrypy.server.ssl_certificate = ".ssl-keys/cert.pem"
cherrypy.server.ssl_private_key = ".ssl-keys/privkey.pem"
cherrypy.server.start()



    
