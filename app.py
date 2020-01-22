#app.py

from blueprints import app, manager
from flask_restful import Api
import logging , sys                                      
from logging.handlers import RotatingFileHandler 
from werkzeug.contrib.cache import SimpleCache

from flask_cors import CORS


CORS(app)


cache = SimpleCache()


api = Api(app, catch_all_404s=True)       


if __name__ == '__main__':
    
    try:
       if sys.argv[1] == 'db':
           manager.run()
    except Exception as e:
        
        logging.getLogger().setLevel(logging.INFO)
        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")                    
        #app root path nya sudah pindah ke satu folder dgn '__init__.py'
        log_handler = RotatingFileHandler("%s/%s" % (app.root_path, '../storage/log/myapp.log'), maxBytes=10000, backupCount=10)
        # log_handler.setLevel(logging.INFO)                
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)

        app.run(debug=False, host='0.0.0.0', port=5000)     #debug=False, mematikan fitur debug, sehingga log error bisa menangkap semua error
    

#ini sebuah komentar