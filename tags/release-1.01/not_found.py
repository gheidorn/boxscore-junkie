#    This work is licensed under the Creative Commons Attribution 3.0 Unported License.
#    To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/ or 
#    send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, 
#    California, 94105, USA.
#    
#    not_found.py handles URIs that are not accounted for
#    
#    $Id$
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
