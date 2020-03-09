import re
import traceback
# from jinja2 import Template
from jinja2 import Environment, FileSystemLoader, PackageLoader
e = Environment(loader=FileSystemLoader('/Users/williamgunnells/codechanges/raspberryweb/templates'))
# template=Template('Hello {{ name}}!')
from urllib.parse import urlparse


class Raspberry(object):
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
            print("start of delegate:::")
            print(x)
            self.start(self.status, self._headers)
        except:
            headers = [("Content-Type", "text/plain")]
            self.start("500 Internal Error", headers)
            x = "Internal Error:\n\n" + traceback.format_exc()

        # return value can be a string or a list. we should be able to
        # return an iter in both the cases.
        if isinstance(x, str):
            print("isinstance:::")
            print(x)
            return iter([x])
        else:
            print("isinstance else::::")
            print(type(x))
            return iter(x)

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            print("pattern:::::")
            print(m)
            if m:
                # pass the matched groups as args
                args = m.groups()
                print("args::::")
                print(args)
                func_name = method.lower() + "_" + name
                print("func_name:::::")
                print(func_name)
                func = getattr(self, func_name)
                print("func::::")
                print(func)
                return func(*args)

        return self.notfound()

    def web_input(self, key):
        data = urlparse(self.environ['QUERY_STRING'])
        item = data.get(key, [''])[0]  # (key,[]) return list same key
        return escape(item)

    def web_post(self):
        try:
            r_body_size = int(self.environ.get('CONTENT_LENGTH',0))
        except ValueError:
            r_body_size = 0
        request_body = self.environ['wsgi.input'].read(r_body_size)
        d = urlparse(request_body)
        return d

    def web_format(self, data, key):
        item = data.get(key, [''])[0]
        return escape(item)


class Application(Raspberry):
    thehtml="""
    <html><form method="post">
    <p>fname: <input type="text" name="fname">
    <p>lname: <input type="text" name="lname">
    <p><input type="submit" value="Submit"></form>
    </html>
    """

    urls = [
                ("/", "index"),
                ("/hello/(.*)", "hello"),
        ("/jinja/(.*)", "jinja"),
        ("/tmpl/(.*)", "tmpl"),
        ("/tmpl2/(.*)", "tmpl2"),
        ("/storage/(.*)", "storage"),
        ("/storage2/(.*)", "storage2"),
        ("/mypost/", "mypost"),
        ("/mypost2/", "mypost2")
    ]

    def get_index(self):
        return b"Main Page"

    def get_hello(self, name):
        return "Hello, %s!" % name

    def get_jinja(self, name):
        return str(template.render(name="John Doe"))

    def get_tmpl(self, name):
        r_template = e.get_template('mytemplate.html')
        return str(Rtemplate.render())

    def get_tmpl2(self, name):
        r_template = e.get_template('mytemp2.html')
        dict = {'name': 'will', 'last': 'gunn'}  # {{dict}} in template
        return str(Rtemplate.render(dict=dict))

    def get_storage(self, name):
        d = urlparse(self.environ['QUERY_STRING'])
        print(p)
        print("asdf: %s" % d.get('id', [''])[0])
        print("fort: %s" % d.get('foo', [''])[0] )
        return "Storage, %s" % name

    def get_storage_2(self, name):
        f = self.webinput('id')
        print(f)
        return "hello %s" % f

    def get_my_post(self):
        return self.thehtml

    def post_my_post(self):  # error if GET does not exist first
        try:
            r_body_size = int(self.environ.get('CONTENT_LENGTH',0))
        except ValueError:
            r_body_size = 0
        request_body = self.environ['wsgi.input'].read(r_body_size)
        d = urlparse(request_body)
        print(d)
        return "strange"

    def get_my_post_2(self):
        return self.thehtml

    def post_my_post_2(self):
        res = self.webpost()
        print(res)
        firstname = self.webformat(res, 'fname')
        lastname = self.webformat(res, 'lname')
        print(firstname)
        print(lastname)
        return "interesting"


if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8080, Application)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

