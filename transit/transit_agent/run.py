from .app import app
from .app import flask_config

def main(): 

    app.run(host=flask_config.HOST, 
            port=flask_config.PORT, 
            debug=flask_config.DEBUG)
    
if __name__ == "__main__": 
    main() 