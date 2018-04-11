import os
import tornado.ioloop
import tornado.web
import tornado.log
import requests


from jinja2 import \
  Environment, PackageLoader, select_autoescape
  
ENV = Environment(
  loader=PackageLoader('OGdash', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))
    
class MainHandler(TemplateHandler):
  def get(self):
    oilPrice= requests.get('http://api.eia.gov/series/?api_key=c31bf5f6d00c2cd29d3f35c00a37af3c&series_id=PET.RWTC.D')
    op=oilPrice.json()['series'][0]['data'][0]
    natPrice= requests.get('http://api.eia.gov/series/?api_key=c31bf5f6d00c2cd29d3f35c00a37af3c&series_id=NG.RNGWHHD.D')
    np=natPrice.json()['series'][0]['data'][0]
    oilrig= requests.get('http://api.eia.gov/series/?api_key=c31bf5f6d00c2cd29d3f35c00a37af3c&series_id=TOTAL.OGNRPON.M')
    rc=oilrig.json()['series'][0]['data'][0]
    self.render_template("dashboard.html", {'np':"{0:.2f}".format(np[1]),'op':"{0:.2f}".format(op[1]),'rc':rc[1]})

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/static/(.*)", 
      tornado.web.StaticFileHandler, {'path': 'static'}),
  ], autoreload=True)
  
if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '8080')))
  tornado.ioloop.IOLoop.current().start()