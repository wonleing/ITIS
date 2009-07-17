drop table application;
create table application (appname varchar(20) primary key, dbname varchar(20), dbuser varchar(20), dbpwd varchar(20), adminuser varchar(20), adminpwd varchar(20), urlbase varchar(40));

--drop table project;
--create table project (

insert into application values ("MediaWiki", "mediawiki", "wikiuser", "secret", "sysop", "itis", NULL);
insert into application values ("Wordpress", "wordpress", "wordpress", "secret", "admin", "itis", NULL);
insert into application values ("Bugzilla", "bugs", "bugs", "secret", "admin", "itis", NULL);
insert into application values ("Sugarcrm", "sugacrm", "sugaruser", "secret", "admin", "itis", NULL);
insert into application values ("Dotproject", "dotproject", "dotproject", "secret", "admin", "itis", NULL);
insert into application values ("Orangehrm", "orangehrm", "orangehrm", "secret", "admin", "itis", NULL);
insert into application values ("Drupal", "drupal", "drupal", "secret", "admin", "itis", NULL);

