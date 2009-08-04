# -*- coding:utf-8 -*-
import cherrypy,os,pam,sqlite3,time
from genshi.template import TemplateLoader

class Index(object):
    def __init__(self):
        global logined,LANG
        logined=1
        LANG="en"

    @cherrypy.expose
    def index(self):
        global LANG
        if LANG=="cn":
            import language.cn as lang
        else:
            import language.en as lang
        data = {'login_title':lang.login_title.decode("utf-8"),
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
        if logined:
            global LANG,THEME
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'serverconf_title':lang.serverconf_title.decode("utf-8"),
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
        if logined:
            global LANG
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            cx = sqlite3.connect("db")
            cu = cx.cursor()
            cu.execute("select * from project")
            result = cu.fetchall()
            cu.execute("select appname from application")
            result2 = cu.fetchall()
            cx.close()
            data = {'pjs':result,
                    'items':result2,
                    'project_title':lang.project_title.decode("utf-8"),
                    'project_exist':lang.project_exist.decode("utf-8"),
                    'project_applist':lang.project_applist.decode("utf-8"),
                    'pj_text1':lang.pj_text1.decode("utf-8"),
                    'pj_text2':lang.pj_text2.decode("utf-8"),
                    'pj_text3':lang.pj_text3.decode("utf-8"),
                    'pj_text4':lang.pj_text4.decode("utf-8"),
                    'pj_text5':lang.pj_text5.decode("utf-8"),
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
    def doProject(self, newpj_1=None, newpj_2=None, newpj_3=None, newpj_4=None, applist=None):
        if newpj_1==None:
           raise cherrypy.HTTPRedirect("Statusfail")
        if logined:
            ctime = time.strftime("%F")
            cx = sqlite3.connect("db")
            cu = cx.cursor()
            cu.execute("insert into project values ('%s','%s','%s','%s','%s')" %(newpj_1, newpj_2, newpj_3, newpj_4, ctime))
            cx.commit()
            cx.close()
            for app in applist:
              if app=="ldap":
                os.system("sudo ./ldapadduser.sh %s %s" %(newpj_2, newpj_4))
              os.system("sudo ./createproject.sh %s %s" %(newpj_2, app))
            raise cherrypy.HTTPRedirect("Statussuccess")
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Application(self):
        if logined:
            global LANG
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            cx = sqlite3.connect("db")
            cu = cx.cursor()
            cu.execute("select * from application")
            result = cu.fetchall()
            cx.close()

            data = {'apps':result,
                    'application_title':lang.application_title.decode("utf-8"),
                    'app_text1':lang.app_text1.decode("utf-8"),
                    'app_text2':lang.app_text2.decode("utf-8"),
                    'app_text3':lang.app_text3.decode("utf-8"),
                    'app_text4':lang.app_text4.decode("utf-8"),
                    'app_text5':lang.app_text5.decode("utf-8"),
                    'app_text6':lang.app_text6.decode("utf-8"),
                    'app_text7':lang.app_text7.decode("utf-8"),
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
    def doApp(self, MediaWiki_1=None, MediaWiki_2=None, MediaWiki_3=None, MediaWiki_4=None, MediaWiki_5=None, MediaWiki_6=None, Wordpress_1=None, Wordpress_2=None, Wordpress_3=None, Wordpress_4=None, Wordpress_5=None, Wordpress_6=None, Bugzilla_1=None, Bugzilla_2=None, Bugzilla_3=None, Bugzilla_4=None, Bugzilla_5=None, Bugzilla_6=None, Sugarcrm_1=None, Sugarcrm_2=None, Sugarcrm_3=None, Sugarcrm_4=None, Sugarcrm_5=None, Sugarcrm_6=None, Dotproject_1=None, Dotproject_2=None, Dotproject_3=None, Dotproject_4=None, Dotproject_5=None, Dotproject_6=None, Orangehrm_1=None, Orangehrm_2=None, Orangehrm_3=None, Orangehrm_4=None, Orangehrm_5=None, Orangehrm_6=None, Drupal_1=None, Drupal_2=None, Drupal_3=None, Drupal_4=None, Drupal_5=None, Drupal_6=None):
        if MediaWiki_1==None or MediaWiki_2==None or MediaWiki_3==None or Wordpress_1==None or Wordpress_2==None or Wordpress_3==None or Bugzilla_1==None or Bugzilla_2==None or Bugzilla_3==None or Sugarcrm_1==None or Sugarcrm_2==None or Sugarcrm_3==None or Dotproject_1==None or Dotproject_2==None or Dotproject_3==None or Orangehrm_1==None or Orangehrm_2==None or Orangehrm_3==None or Drupal_1==None or Drupal_2==None or Drupal_3==None:
           raise cherrypy.HTTPRedirect("Statusfail")
        if logined:
            f = open("application.conf", "w")
            f.write("mw_dbname=%s\n" %MediaWiki_1)
            f.write("mw_dbuser=%s\n" %MediaWiki_2)
            f.write("mw_dbpwd=%s\n" %MediaWiki_3)
            f.write("mw_adminuser=%s\n" %MediaWiki_4)
            f.write("mw_adminpwd=%s\n" %MediaWiki_5)
            f.write("mw_urlbase=%s\n" %MediaWiki_6)
            f.write("wp_dbname=%s\n" %Wordpress_1)
            f.write("wp_dbuser=%s\n" %Wordpress_2)
            f.write("wp_dbpwd=%s\n" %Wordpress_3)
            f.write("wp_adminuser=%s\n" %Wordpress_4)
            f.write("wp_adminpwd=%s\n" %Wordpress_5)
            f.write("wp_urlbase=%s\n" %Wordpress_6)
            f.write("bz_dbname=%s\n" %Bugzilla_1)
            f.write("bz_dbuser=%s\n" %Bugzilla_2)
            f.write("bz_dbpwd=%s\n" %Bugzilla_3)
            f.write("bz_adminuser=%s\n" %Bugzilla_4)
            f.write("bz_adminpwd=%s\n" %Bugzilla_5)
            f.write("bz_urlbase=%s\n" %Bugzilla_6)
            f.write("sc_dbname=%s\n" %Sugarcrm_1)
            f.write("sc_dbuser=%s\n" %Sugarcrm_2)
            f.write("sc_dbpwd=%s\n" %Sugarcrm_3)
            f.write("sc_adminuser=%s\n" %Sugarcrm_4)
            f.write("sc_adminpwd=%s\n" %Sugarcrm_5)
            f.write("sc_urlbase=%s\n" %Sugarcrm_6)
            f.write("dp_dbname=%s\n" %Dotproject_1)
            f.write("dp_dbuser=%s\n" %Dotproject_2)
            f.write("dp_dbpwd=%s\n" %Dotproject_3)
            f.write("dp_adminuser=%s\n" %Dotproject_4)
            f.write("dp_adminpwd=%s\n" %Dotproject_5)
            f.write("dp_urlbase=%s\n" %Dotproject_6)
            f.write("oh_dbname=%s\n" %Orangehrm_1)
            f.write("oh_dbuser=%s\n" %Orangehrm_2)
            f.write("oh_dbpwd=%s\n" %Orangehrm_3)
            f.write("oh_adminuser=%s\n" %Orangehrm_4)
            f.write("oh_adminpwd=%s\n" %Orangehrm_5)
            f.write("oh_urlbase=%s\n" %Orangehrm_6)
            f.write("dr_dbname=%s\n" %Drupal_1)
            f.write("dr_dbuser=%s\n" %Drupal_2)
            f.write("dr_dbpwd=%s\n" %Drupal_3)
            f.write("dr_adminuser=%s\n" %Drupal_4)
            f.write("dr_adminpwd=%s\n" %Drupal_5)
            f.write("dr_urlbase=%s\n" %Drupal_6)
            f.close()
            os.system("sudo ./appconf.sh")
            raise cherrypy.HTTPRedirect("Statussuccess")
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Systemconf(self):
        if logined:
            global LANG
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'sysconf_title':lang.sysconf_title.decode("utf-8"),
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
        if language==None or theme==None:
           raise cherrypy.HTTPRedirect("Statusfail")
        if logined:
            global LANG
            LANG=language
            os.system("cp html/" + theme + " html/current.css")
            raise cherrypy.HTTPRedirect("Statussuccess")
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def Statussuccess(self):
        if logined:
            global LANG
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'status_title':lang.status_title_success.decode("utf-8"),
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
        if logined:
            global LANG
            if LANG=="cn":
                import language.cn as lang
            else:
                import language.en as lang
            data = {'status_title':lang.status_title_fail.decode("utf-8"),
                    'config_status':lang.config_status_fail.decode("utf-8"),
                    'link_serverconf':lang.link_serverconf.decode("utf-8"),
                    'link_newpro':lang.link_newpro.decode("utf-8"),
                    'link_appconf':lang.link_appconf.decode("utf-8"),
                    'link_sysconf':lang.link_sysconf.decode("utf-8")}
            return tl.load('confstatus.html').generate(**data).render()
        else:
            raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def currentcss(self):
        f=open("html/current.css", "r")
        return f.read()


if __name__ == '__main__':
    tl = TemplateLoader(['./html'])
    cherrypy.config.update('/etc/itis/global.conf')
    cherrypy.quickstart(Index())
