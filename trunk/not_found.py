#!/usr/bin/env python
#
# Copyright 2008 Greg Heidorn
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import logging
import os
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class PageNotFoundHandler(webapp.RequestHandler):
  def get(self):
    logging.info("bad request logged")
    logging.info(self.request.uri)
    path = os.path.join(os.path.dirname(__file__), '404.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/404', PageNotFoundHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
