# -*- coding:utf-8 -*- 
import cherrypy,os,pam,sysconfig
from genshi.template import TemplateLoader

class Index(object):
    def __init__(self):
        global logined
        logined=1

    @cherrypy.expose
    def index(self):
        if sysconfig.LANG=="cn":
            import language.cn as lang
        else:
            import language.en as lang
        data = {'login_title':lang.login_title,
                'uname':lang.username,
                'passwd':lang.password,
                'button_ok':lang.button_ok,
                'button_cancel':lang.button_cancel}
        return tl.load('login.html').generate(**data).render()

    @cherrypy.expose
    def doLogin(self, username=None, password=None):
        result = pam.authenticate(username=username, password=password, service='login')
        if result:
            global logined
            logined=1
            raise cherrypy.HTTPRedirect("Serverconfig")
        else:
            raise cherrypy.HTTPRedirect("index")


    @cherrypy.expose
    def Serverconfig(object):
        global logined
        if logined:
            if sysconfig.LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'serverconf_title':lang.serverconf_title,
                    'ldap_setting':lang.ldap_setting,
                    'ldap_path':lang.ldap_path,
                    'ldap_com':lang.ldap_com,
                    'ldap_mail':lang.ldap_mail,
                    'ldap_user':lang.ldap_user,
                    'ldap_pwd':lang.ldap_pwd,
                    'db_setting':lang.db_setting,
                    'db_path':lang.db_path,
                    'db_user':lang.db_user,
                    'db_pwd':lang.db_pwd,
                    'apache_setting':lang.apache_setting,
                    'apache_path':lang.apache_path,
                    'apache_port':lang.apache_port,
                    'share_setting':lang.share_setting,
                    'share_path':lang.share_path,
                    'share_name':lang.share_name,
                    'svn_setting':lang.svn_setting,
                    'svn_path':lang.svn_path,
                    'svn_repo':lang.svn_repo,
                    'backup_setting':lang.backup_setting,
                    'backup_daily':lang.backup_daily,
                    'backup_monthly':lang.backup_monthly,
                    'button_ok':lang.button_ok,
                    'button_cancel':lang.button_cancel,
                    'link_serverconf':lang.link_serverconf,
                    'link_newpro':lang.link_newpro,
                    'link_appconf':lang.link_appconf,
                    'link_sysconf':lang.link_sysconf}
            return tl.load('serverconfig.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def doConfig(self, ldap_1=None, ldap_2=None, ldap_3=None, ldap_4=None, ldap_5=None, database_1=None, database_2=None, database_3=None, apache_1=None, apache_2=None, share_1=None, share_2=None, svn_1=None, svn_2=None, backup_1=None, backup_2=None):
        global logined
        if ldap_1==None or ldap_2==None or ldap_3==None or ldap_4==None or ldap_5==None or database_1==None or database_2==None or database_3==None or apache_1==None or apache_2==None or share_1==None or  share_2==None or svn_1==None or svn_2==None:
            raise cherrypy.HTTPRedirect("Statusfail")
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
            os.system("sudo ./serverconf.sh")
            raise cherrypy.HTTPRedirect("Statussuccess")
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Newproject(self):
        global logined
        if logined:
            if sysconfig.LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {
                    'button_ok':lang.button_ok,
                    'button_cancel':lang.button_cancel,
                    'link_serverconf':lang.link_serverconf,
                    'link_newpro':lang.link_newpro,
                    'link_appconf':lang.link_appconf,
                    'link_sysconf':lang.link_sysconf}
            return tl.load('newproject.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")


    @cherrypy.expose
    def Application(self):
        global logined
        if logined:
            if sysconfig.LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {
                    'button_ok':lang.button_ok,
                    'button_cancel':lang.button_cancel,
                    'link_serverconf':lang.link_serverconf,
                    'link_newpro':lang.link_newpro,
                    'link_appconf':lang.link_appconf,
                    'link_sysconf':lang.link_sysconf}
            return tl.load('application.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Systemconf(self):
        global logined
        if logined:
            if sysconfig.LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {
                    'button_ok':lang.button_ok,
                    'button_cancel':lang.button_cancel,
                    'link_serverconf':lang.link_serverconf,
                    'link_newpro':lang.link_newpro,
                    'link_appconf':lang.link_appconf,
                    'link_sysconf':lang.link_sysconf}
            return tl.load('systemconf.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")
        
    @cherrypy.expose
    def doSysconf(language=None, theme=None):
        if logined:
            sysconfig.update({'LANG': language, 'THEME': theme})
            raise cherrypy.HTTPRedirect("Statussuccess")
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Statussuccess(self):
        global logined
        if logined:
            if sysconfig.LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'status_title':lang.status_title_success,
                    'config_status':lang.config_status_success,
                    'link_serverconf':lang.link_serverconf,
                    'link_newpro':lang.link_newpro,
                    'link_appconf':lang.link_appconf,
                    'link_sysconf':lang.link_sysconf}
            return tl.load('confstatus.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Statusfail(self):
        global logined
        if logined:
            if sysconfig.LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'status_title':lang.status_title_fail,
                    'config_status':lang.config_status_fail,
                    'link_serverconf':lang.link_serverconf,
                    'link_newpro':lang.link_newpro,
                    'link_appconf':lang.link_appconf,
                    'link_sysconf':lang.link_sysconf}
            return tl.load('confstatus.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")



if __name__ == '__main__':
    tl = TemplateLoader(['./html'])
    cherrypy.config.update('global.conf')
    cherrypy.quickstart(Index())
