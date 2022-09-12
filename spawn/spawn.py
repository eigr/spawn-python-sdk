"""
Licensed under the Apache License, Version 2.0.
"""
from flask import Flask
from routes.action import action_endpoint

from dataclasses import (dataclass, field)
import os

import logging


@dataclass
class Spawn:
    logging.basicConfig(
        format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s', level=logging.INFO)
    logging.root.setLevel(logging.NOTSET)

    __host = '127.0.0.1'
    __port = '8090'

    def host(self, address: str):
        """Set the Network Host address."""
        self.__host = address
        return self

    def port(self, port: str):
        """Set the Network Port address."""
        self.__port = port
        return self

    def start(self):
        """Start the user function and HTTP Server."""
        address = '{}:{}'.format(os.environ.get(
            'HOST', self.__host), os.environ.get('PORT', self.__port))

        logging.info('Starting Spawn on address %s', address)
        try:
            app = Flask(__name__)
            app.register_blueprint(action_endpoint)
            app.run(host=self.__host, port=self.__port, debug=True)
        except IOError as e:
            logging.error('Error on start Spawn %s', e.__cause__)
