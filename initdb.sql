drop table application;
create table application (appname varchar(20) primary key, dbname varchar(20), dbuser varchar(20), dbpwd varchar(20), adminuser varchar(20), adminpwd varchar(20), urlbase varchar(40));

drop table project;
create table project (pjname varchar(20) primary key, code varchar(20), description varchar(40), people varchar(40), ctime varchar(20));

insert into application values ("MediaWiki", "mediawiki", "wikiuser", "secret", "sysop", "itis", NULL);
insert into application values ("Wordpress", "wordpress", "wordpress", "secret", "admin", "itis", NULL);
insert into application values ("Bugzilla", "bugs", "bugs", "secret", "admin", "itis", NULL);
insert into application values ("Sugarcrm", "sugacrm", "sugaruser", "secret", "admin", "itis", NULL);
insert into application values ("Dotproject", "dotproject", "dotproject", "secret", "admin", "itis", NULL);
insert into application values ("Orangehrm", "orangehrm", "orangehrm", "secret", "admin", "itis", NULL);
insert into application values ("Drupal", "drupal", "drupal", "secret", "admin", "itis", NULL);

insert into project values ("itis", "itis", "Initial sample project", "Leon, Nie", "2009-07-29");
