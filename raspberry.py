import re
import traceback
from jinja2 import Template 
from jinja2 import Environment, FileSystemLoader, PackageLoader
e = Environment(loader=FileSystemLoader('/home/knoppix/raspberryweb/templates')) 
#template=Template('Hello {{ name}}!')
from cgi import parse_qs,escape

class Raspberry:
    """raspberry web framwork.
    example:
	class application(Raspberry):
            urls = [
                ("/", "index"),
                ("/hello/(.*)","hello"),
		("/jinja/(.*)","jinja"),
		("/tmpl/(.*)","tmpl"), 
		("/tmpl2/(.*)","tmpl2")
            ]
            def GET_index(self):
                return "Main Page" 
	    def GET_hello(self, name):
                return "Hello, %s!" % name
	    def GET_jinja(self,name):
		return str(template.render(name="John Doe")) 
	    def GET_tmpl(self,name):
		Rtemplate=e.get_template('mytemplate.html")
		return str(Rtemplate.render())
	    def GET_tmpl2(self,name):
		Rtemplate=e.get_template('mytemp2.html')
		dict={'name':'will','last':'gunn'} #{{dict}} in template
		return str(Rtemplate.render(dict=dict)) 
	    
template/

mytemp2.html
{% if dict %}
<p>{{dict}}
<p>{{dict.name}}
<p>{{dict.will}}
{%endif%}



    """
        
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self.status = "200 OK"
        self._headers = []
            
    def header(self, name, value):
        self._headers.append((name, value))
            
    def __iter__(self):
        try:
            x = self.delegate()
            self.start(self.status, self._headers)
        except:
            headers = [("Content-Type", "text/plain")]
            self.start("500 Internal Error", headers)
            x = "Internal Error:\n\n" + traceback.format_exc()
            
        # return value can be a string or a list. we should be able to 
        # return an iter in both the cases.
        if isinstance(x, str):
            return iter([x])
        else:
            return iter(x)

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
            
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups() 
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(*args)
                    
        return self.notfound()

class application(Raspberry):
	urls = [
                ("/", "index"),
                ("/hello/(.*)","hello"), 
		("/jinja/(.*)","jinja"), 
		("/tmpl/(.*)","tmpl"), 
		("/tmpl2/(.*)","tmpl2"),
		("/storage/(.*)","storage")
	]

	def GET_index(self):
		return "Main Page" 
	def GET_hello(self, name):
                return "Hello, %s!" % name
	def GET_jinja(self,name):
		return str(template.render(name="John Doe"))
	def GET_tmpl(self,name):
		Rtemplate=e.get_template('mytemplate.html')
		return str(Rtemplate.render())
	def GET_tmpl2(self,name):
		Rtemplate=e.get_template('mytemp2.html')
		dict={'name':'will','last':'gunn'} #{{dict}} in template
		return str(Rtemplate.render(dict=dict)) 
	def GET_storage(self,name):
		d=parse_qs(self.environ['QUERY_STRING'])
		print d
		print "asdf: %s" % d.get('id',[''])[0] 
		print "fort: %s" % d.get('foo',[''])[0] 
		return "Storage, %s" % name 


if __name__ == '__main__':
	from wsgiref import simple_server
	httpd = simple_server.make_server('192.168.1.126', 8080, application)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

