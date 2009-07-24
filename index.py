# -*- coding:utf-8 -*-
import cherrypy,os,pam
from genshi.template import TemplateLoader

class Index(object):
    def __init__(self):
        global logined,LANG,THEME
        logined=1
        LANG="en"
        THEME="layout1.css"

    @cherrypy.expose
    def index(self):
        global LANG,THEME
        if LANG=="cn":
            import language.cn as lang
        else:
            import language.en as lang
        #return lang.login_title
        data = {'layout':THEME,
                'login_title':lang.login_title.decode("utf-8"),
                'uname':lang.username.decode("utf-8"),
                'passwd':lang.password.decode("utf-8"),
                'button_ok':lang.button_ok.decode("utf-8"),
                'button_cancel':lang.button_cancel.decode("utf-8")}
        return tl.load('login.html').generate(**data).render(encoding="UTF-8")

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
            global LANG,THEME
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'layout':THEME,
                    'serverconf_title':lang.serverconf_title.decode("utf-8"),
                    'ldap_setting':lang.ldap_setting.decode("utf-8"),
                    'ldap_path':lang.ldap_path.decode("utf-8"),
                    'ldap_com':lang.ldap_com.decode("utf-8"),
                    'ldap_mail':lang.ldap_mail.decode("utf-8"),
                    'ldap_user':lang.ldap_user.decode("utf-8"),
                    'ldap_pwd':lang.ldap_pwd.decode("utf-8"),
                    'db_setting':lang.db_setting.decode("utf-8"),
                    'db_path':lang.db_path.decode("utf-8"),
                    'db_user':lang.db_user.decode("utf-8"),
                    'db_pwd':lang.db_pwd.decode("utf-8"),
                    'apache_setting':lang.apache_setting.decode("utf-8"),
                    'apache_path':lang.apache_path.decode("utf-8"),
                    'apache_port':lang.apache_port.decode("utf-8"),
                    'share_setting':lang.share_setting.decode("utf-8"),
                    'share_path':lang.share_path.decode("utf-8"),
                    'share_name':lang.share_name.decode("utf-8"),
                    'svn_setting':lang.svn_setting.decode("utf-8"),
                    'svn_path':lang.svn_path.decode("utf-8"),
                    'svn_repo':lang.svn_repo.decode("utf-8"),
                    'backup_setting':lang.backup_setting.decode("utf-8"),
                    'backup_daily':lang.backup_daily.decode("utf-8"),
                    'backup_monthly':lang.backup_monthly.decode("utf-8"),
                    'button_ok':lang.button_ok.decode("utf-8"),
                    'button_cancel':lang.button_cancel.decode("utf-8"),
                    'link_serverconf':lang.link_serverconf.decode("utf-8"),
                    'link_newpro':lang.link_newpro.decode("utf-8"),
                    'link_appconf':lang.link_appconf.decode("utf-8"),
                    'link_sysconf':lang.link_sysconf.decode("utf-8")}
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
            global LANG,THEME
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'layout':THEME,
                    'button_ok':lang.button_ok.decode("utf-8"),
                    'button_cancel':lang.button_cancel.decode("utf-8"),
                    'link_serverconf':lang.link_serverconf.decode("utf-8"),
                    'link_newpro':lang.link_newpro.decode("utf-8"),
                    'link_appconf':lang.link_appconf.decode("utf-8"),
                    'link_sysconf':lang.link_sysconf.decode("utf-8")}
            return tl.load('newproject.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")


    @cherrypy.expose
    def Application(self):
        global logined
        if logined:
            global LANG,THEME
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'layout':THEME,
                    'button_ok':lang.button_ok.decode("utf-8"),
                    'button_cancel':lang.button_cancel.decode("utf-8"),
                    'link_serverconf':lang.link_serverconf.decode("utf-8"),
                    'link_newpro':lang.link_newpro.decode("utf-8"),
                    'link_appconf':lang.link_appconf.decode("utf-8"),
                    'link_sysconf':lang.link_sysconf.decode("utf-8")}
            return tl.load('application.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Systemconf(self):
        global logined
        if logined:
            global LANG,THEME
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'layout':THEME,
                    'sysconf_title':lang.sysconf_title.decode("utf-8"),
                    'sys_lang':lang.sys_lang.decode("utf-8"),
                    'sys_css':lang.sys_css.decode("utf-8"),
                    'css_type1':lang.css_type1.decode("utf-8"),
                    'css_type2':lang.css_type2.decode("utf-8"),
                    'button_ok':lang.button_ok.decode("utf-8"),
                    'button_cancel':lang.button_cancel.decode("utf-8"),
                    'link_serverconf':lang.link_serverconf.decode("utf-8"),
                    'link_newpro':lang.link_newpro.decode("utf-8"),
                    'link_appconf':lang.link_appconf.decode("utf-8"),
                    'link_sysconf':lang.link_sysconf.decode("utf-8")}
            return tl.load('systemconf.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")
        
    @cherrypy.expose
    def doSysconf(self, language=None, theme=None):
        if logined:
            global LANG,THEME
            LANG=language
            THEME=theme+".css"
            raise cherrypy.HTTPRedirect("Statussuccess")
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Statussuccess(self):
        global logined
        if logined:
            global LANG,THEME
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'layout':THEME,
                    'status_title':lang.status_title_success.decode("utf-8"),
                    'config_status':lang.config_status_success.decode("utf-8"),
                    'link_serverconf':lang.link_serverconf.decode("utf-8"),
                    'link_newpro':lang.link_newpro.decode("utf-8"),
                    'link_appconf':lang.link_appconf.decode("utf-8"),
                    'link_sysconf':lang.link_sysconf.decode("utf-8")}
            return tl.load('confstatus.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Statusfail(self):
        global logined
        if logined:
            global LANG,THEME
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'layout':THEME,
                    'status_title':lang.status_title_fail.decode("utf-8"),
                    'config_status':lang.config_status_fail.decode("utf-8"),
                    'link_serverconf':lang.link_serverconf.decode("utf-8"),
                    'link_newpro':lang.link_newpro.decode("utf-8"),
                    'link_appconf':lang.link_appconf.decode("utf-8"),
                    'link_sysconf':lang.link_sysconf.decode("utf-8")}
            return tl.load('confstatus.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")



if __name__ == '__main__':
    tl = TemplateLoader(['./html'])
    cherrypy.config.update('global.conf')
    cherrypy.quickstart(Index())
