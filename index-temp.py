# -*- coding:utf-8 -*- 
import cherrypy
import os,imp,sqlite3
from string import Template

class Index(object):
    def __init__(self):
        global logined
        logined=1
        global LANG
        LANG='en'

    @cherrypy.expose
    def index(self):
        if LANG=="Chinese":
            import language.cn as lang
        else:
            import language.en as lang
        f1=open("html/login.template", "r")
        s = Template(f1.read())
        return s.substitute(login_title=lang.login_title, login_name=lang.login_name, login_password=lang.login_password, button_ok=lang.button_ok, button_cancel=lang.button_cancel, link_registry=lang.link_registry)
        f1.close()

    @cherrypy.expose
    def doLogin(self, username=None, password=None):
        cx = sqlite3.connect("db1")
        cu = cx.cursor()
        cu.execute("select count(*) from user where name=\"%s\"" %username)
        count = cu.fetchall()[0][0]
        if (username != "") and count:
            cu.execute("select passwd from user where name=\"%s\"" %username)
            passwd = cu.fetchall()[0][0]
            if passwd == password:
                global logined
                logined=1
                raise cherrypy.HTTPRedirect("Testmain")
            else:
                raise cherrypy.HTTPRedirect("Registry")
        else:
            raise cherrypy.HTTPRedirect("Registry")

    @cherrypy.expose
    def Testmain(self):
      global logined
      if logined:
        if LANG=="Chinese":
            import language.cn as lang
        else:
            import language.en as lang
        nodeliststring=""
        packageliststring=""
        f1=open("html/testmain.template", "r")
        s = Template(f1.read())
        return s.substitute(test_title=lang.test_title, test_addnode=lang.test_addnode, test_nodename=lang.test_nodename, test_nodepw=lang.test_nodepw, test_starttest=lang.test_starttest, test_package=lang.test_package, test_nodelist=nodeliststring, test_packagelist=packageliststring,  button_ok=lang.button_ok, link_status=lang.link_status)
        f1.close()
      else:
        raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def doTest(self, machinename=None, testtype=None):
      global logined
      if logined:
        os.system("scp -r scripts %s:~/" %machinename)
        if testtype=="kernel":
            os.system("ssh %s 'cd ~/scripts/kerneltest; ./testall &'" %machinename)
            return "Kernel test started successfully"
        elif testtype=="regression":
            os.system("ssh %s 'cd ~/scripts/regressiontest; ./testall &'" %machinename)
            return "Regression test started successfully"
        elif testtype=="all":
            os.system("ssh %s 'cd ~/scripts; ./runall &'" %machinename)
            return "Regression and Kernel test started successfully"
        else:
            return "Test type error"
      else:
        raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Teststatus(self):
      global logined
      if logined:
        if LANG=="Chinese":
            import language.cn as lang
        else:
            import language.en as lang
        cx = sqlite3.connect("db1")
        cu = cx.cursor()
        cu.execute("select * from job where status !=\"done\"")
        result = cu.fetchall()
        formstring="<table border=\"6\">"
        for record in result:
            formstring += "<tr><td>" + str(record[0]) + "</td><td>" + record[1] + "</td><td>" + record[2] + "</td><td>" + record[3] + "</td><td>" + record[4] + "</td></tr>"
        formstring += "</table>"
        f1=open("html/teststatus.template", "r")
        s = Template(f1.read())
        return s.substitute(status_title=lang.status_title, status_result=formstring, link_testmain=lang.link_testmain)
        f1.close()
      else:
        raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Registry(self):
        if LANG=="Chinese":
            import language.cn as lang
        else:
            import language.en as lang
        f1=open("html/registry.template", "r")
        s = Template(f1.read())
        return s.substitute(login_name=lang.login_name, login_password=lang.login_password, registry_title=lang.registry_title, registry_confirm=lang.registry_confirm, button_ok=lang.button_ok, button_cancel=lang.button_cancel)
        f1.close()

    @cherrypy.expose
    def doRegistry(self, username=None, password=None, password2=None):
        cx = sqlite3.connect("db1")
        cu = cx.cursor()
        cu.execute("select count(*) from user where name=\"%s\"" %username)
        count = cu.fetchall()[0][0]
        if (username != "") and (count == 0) and (password==password2):
            cu.execute("insert into user values ('%s', '%s')" %(username, password))
            cx.commit()
            global logined
            logined=1
            raise cherrypy.HTTPRedirect("Testmain")
        else:
            raise cherrypy.HTTPRedirect("Registry")

    @cherrypy.expose
    def Addnode(self):
        if LANG=="Chinese":
            import language.cn as lang
        else:
            import language.en as lang
        f1=open("html/addnode.template", "r")
        s = Template(f1.read())
        return s.substitute(login_name=lang.login_name, login_password=lang.login_password, registry_title=lang.registry_title, registry_confirm=lang.registry_confirm, button_ok=lang.button_ok, button_cancel=lang.button_cancel)
        f1.close()

cherrypy.config.update('global.conf')
cherrypy.quickstart(Index())
