from __future__ import print_function, absolute_import
  
import sys
import collections
import re
import os
from flask import Flask, redirect, make_response, Response, render_template, request, send_from_directory
import uuid
import httpretty
import requests
import os.path
import pandas as pd
import simplejson
import json
import codecs
app = Flask(__name__)

@app.route("/")
def main():
    return 'NARCIS test web application'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
