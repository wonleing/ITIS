# -*- coding:utf-8 -*- 
import cherrypy
import time,os
import sqlite3

class Index(object):
    def __init__(self):
        global logined
        logined=1

    @cherrypy.expose
    def index(self):
        return '''
        <form action="doLogin" method="post">
        <p>用户名</p>
        <input type="text" name="username" value="" size="15" maxlength="40"/>
        <p>密码</p>
        <input type="password" name="password" value="" size="10" maxlength="40"/>
        <p><input type="submit" value="登录"/><input type="reset" value="重置"/></p>
        </form>
        '''

    @cherrypy.expose
    def doLogin(self, username=None, password=None):
        cx = sqlite3.connect("db1")
        cu = cx.cursor()
        cu.execute("select count(*) from login where uname=\"%s\"" %username)
        count = cu.fetchall()[0][0]
        if (username != "") and count:
            cu.execute("select passwd from login where uname=\"%s\"" %username)
            passwd = cu.fetchall()[0][0]
            if passwd == password:
                global logined
                logined=1
                raise cherrypy.HTTPRedirect("Firstconf")
            else:
                raise cherrypy.HTTPRedirect("Loginfail")
        else:
            raise cherrypy.HTTPRedirect("Loginfail")

    @cherrypy.expose
    def Loginfail(self):
        time.sleep(3)
        raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Firstconf(object):
        global logined
        if logined:
            return '''
        <form action="confConfirm" method="post">
        <p>LDAP设置</p>
           数据库路径<input type="text" name="ldap_1" value="/var/lib/ldap" size="30" maxlength="40"/></br>
           公司域名<input type="text" name="ldap_2" value="itis.com" size="30" maxlength="40"/></br>
           邮件域名<input type="text" name="ldap_3" value="itis.com" size="30" maxlength="40"/></br>
           管理员用户名<input type="text" name="ldap_4" value="Manager" size="30" maxlength="40"/></br>
           管理员密码<input type="text" name="ldap_5" value="secret" size="30" maxlength="40"/></br>
        <p>数据库设置</p>
           数据库路径<input type="text" name="database_1" value="/var/lib/mysql" size="30" maxlength="40"/></br>
           管理员用户名<input type="text" name="database_2" value="root" size="30" maxlength="40"/></br>
           管理员密码<input type="text" name="database_3" value="secret" size="30" maxlength="40"/></br>
        <p>Apache设置</p>
           路径<input type="text" name="apache_1" value="/var/www" size="30" maxlength="40"/></br>
           端口<input type="text" name="apache_2" value="80" size="30" maxlength="40"/></br>
        <p>共享设置</p>
           共享目录<input type="text" name="share_1" value="/var/share" size="30" maxlength="40"/></br>
           共享名称<input type="text" name="share_2" value="share" size="30" maxlength="40"/></br>
        <p>Subversion设置</p>
           数据库路径<input type="text" name="svn_1" value="/var/www/svn" size="30" maxlength="40"/></br>
           镜像名称<input type="text" name="svn_2" value="repos" size="30" maxlength="40"/></br>
        <p>备份策略</p>
           每日备份脚本<input type="text" name="backup_1" value="" size="30" maxlength="40"/></br>
           每月备份脚本<input type="text" name="backup_2" value="" size="30" maxlength="40"/></br>
        <p><input type="submit" value="确定"/><input type="reset" value="恢复默认"/></p>
        </form>
        '''
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def confConfirm(self, ldap_1=None, ldap_2=None, ldap_3=None, ldap_4=None, ldap_5=None, database_1=None, database_2=None, database_3=None, apache_1=None, apache_2=None, share_1=None, share_2=None, svn_1=None, svn_2=None, backup_1=None, backup_2=None):
        global logined
        if ldap_1==None or ldap_2==None or ldap_3==None or ldap_4==None or ldap_5==None or database_1==None or database_2==None or database_3==None or apache_1==None or apache_2==None or share_1==None or  share_2==None or svn_1==None or svn_2==None:
            raise cherrypy.HTTPRedirect("Firstconf")
        if logined:
            f = open("server.conf", "w")
            f.write("ldap_path=%s\n" %ldap_1)
            f.write("ldap_com=%s\n" %ldap_2)
            f.write("ldap_mail=%s\n" %ldap_3)
            f.write("ldap_uname=%s\n" %ldap_4)
            f.write("ldap_passwd=%s\n" %ldap_5)
            f.write("database_path=%s\n" %database_1)
            f.write("database_uname=%s\n" %database_2)
            f.write("database_passwd=%s\n" %database_3)
            f.write("apache_path=%s\n" %apache_1)
            f.write("apache_port=%s\n" %apache_2)
            f.write("share_path=%s\n" %share_1)
            f.write("share_name=%s\n" %share_2)
            f.write("svn_path=%s\n" %svn_1)
            f.write("svn_repo=%s\n" %svn_2)
            f.write("backup_daily=%s\n" %backup_1)
            f.write("backup_monthly=%s\n" %backup_2)
            f.close()
            os.system("./serverconf.sh")
            return'''
            <html><body>
            <p>Server配置完毕！稍后配置自动生效</p></br></br></br>
            <p><a href="/Newproject">新建项目设置</a>
            <p><a href="/Application">进行应用设置</a>
            <p><a href="/Systemconf">进行系统设置</a>
            </body></html>
            '''
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Newproject(self):
        """TBD: use sqlite to store the data. But, what is this page used for???"""
        global logined
        if logined:
            return'''
            <html><body>
            <p>待建中...</p></br></br></br>
            <p><a href="/Firstconf">进行Server首次设置</a>
            <p><a href="/Application">进行应用设置</a>
            <p><a href="/Systemconf">进行系统设置</a>
            </body></html>
            '''
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Application(self):
        """TBD: use sqlite to store the data. Seems only store username and password?"""
        global logined
        if logined:
            return'''
            <html><body>
            <p>待建中...</p></br></br></br>
            <p><a href="/Firstconf">进行Server首次设置</a>
            <p><a href="/Newproject">新建项目设置</a>
            <p><a href="/Systemconf">进行系统设置</a>
            </body></html>
            '''
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Systemconf(self):
        """TBD: use sqlite or just files to store the data. But this page seems useless"""
        global logined
        if logined:
            return'''
            <html><body>
            <p>待建中...</p></br></br></br>
            <p><a href="/Firstconf">进行Server首次设置</a>
            <p><a href="/Newproject">新建项目设置</a>
            <p><a href="/Application">进行应用设置</a>
            </body></html>
            '''
        else:
            raise cherrypy.HTTPRedirect("index")


cherrypy.config.update('global.conf')
cherrypy.quickstart(Index())
