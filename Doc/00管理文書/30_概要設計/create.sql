
/*DB規約*/
grant all on python_game. * to dbuser@localhost identified by 'root'

use python_game

/* キャラクタマスタ
↓以下は連携要素
・gene_id→遺伝マスタ
・race_id→種族マスタ
・dangeon_id→ダンジョンマスタ
・master_id→使役マスタ
・user_id→ユーザマスタ
 */

drop table IF EXISTS dbo.characters;
create table dbo.characters   (
	id int(10) not null auto_increment primary key,
	ins_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	ins_id varchar(10),
	upd_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	upd_id varchar(10),
	gene_id int(10) not null ,
	race_id int(10) not null ,
	grid_x int(10) not null,
	grid_y int(10) not null,
	sgrid_x tinyint,
	sgrid_y tinyint,
	name varchar(16) not null default "unknown",
	age int(4) not null default 0,
	birth datetime not null ,
	level int(10) not null default 0,
	class1 int(4) not null default 1,
	class2 int(4) not null default 0,
	class3 int(4) not null default 0,
	guild_rank char(3) not null default '  G',
	title int(4) not null default 0,
	state int(2) not null default 0,
	HP int(10) not null default 1,
	MP int(10) not null default 1,
	sta int(5) not null default 1,
	atk int(10) not null default 1,
	bit int(10) not null default 1,
	mag int(10) not null default 1,
	des int(10) not null default 1,
	agi int(10) not null default 1,
	talent1 int,
	talent2 int,
	talent3 int,
	party1_id int(10) not null default 0,
	party2_id int(10) not null default 0,
	party3_id int(10) not null default 0,
	dangeon_id int(10) not null default 0,
	master_id int(10) not null default 0,
	user_id varchar(20),
	is_user tinyint,
	is_deleted tinyint(1) default 0
)DEFAULT CHARACTER SET=utf8;

/* 遺伝子マスタ
 */
drop table IF EXISTS dbo.genes;
create table dbo.races (
	id int(10) not null auto_increment primary key,
	ins_date datetime,
	ins_id varchar(10),
	upd_date datetime,
	upd_id varchar(10),
	s_HP int(3) default 1,
	s_MP int(3) default 1,
	s_atk int(3) default 1,
	s_bit int(3) default 1,
	s_mag int(3) default 1,
	s_def int(3) default 1,
	s_agi int(3) default 1,
	total_sense int(3) default 7,
	g_RANK char(3) default 'E'
)
	
create table dbo.races (
	id int(10) not null auto_increment primary key,
	ins_date datetime,
	ins_id verchar(10),
	upd_date datetime,
	upd_id verchar(10),
	atk int(10),
	def int(10),
	bit int(10),
	int int(10),
	def int(10),
	agi int(10),
);

/* ユーザマスタ
↓以下は連携要素
・user_id→キャラクタマスタ
 */
drop table dbo.users;
create table dbo.users (
	id  int(10) not null auto_increment primary key,
	user_id varchar(20),
	password varchar(255),
	ins_date datetime,
	ins_id varchar(10),
	upd_date datetime,
	upd_id varchar(10),
	name varchar(16) not null,
	is_deleted tinyint default 0,
	is_admin tinyint default 0,
	is_sec tinyint default 0,
	is_save tinyint,
	play_time varchar(8) default 0,
	total_amount numeric(10,3)
);

drop table pythonGame.numeric;
create table pythonGame.numeric (
	id int(50) not null auto_increment primary key,
	group_id int(50),
	created datetime,
	created_by varchar(255)
);

drop table pythonGame.pattern;
create table pythonGame.pattern (
	id int(50) not null auto_increment primary key,
	group_id int(50),
	created datetime,
	created_by varchar(255)
);

drop table pythonGame.weapon;
create table pythonGame.weapon (
	id int(10) not null auto_increment primary key,
	group_id int(50),
	created datetime,
	created_by varchar(255)
);

drop table pythonGame.item;
create table pythonGame.item (
	id int not null auto_increment primary key,
	user_id int(10) not null auto_increment primary key,
	user_name varchar(255),
	body text,
	category_id int(50),
	del_flg int(1) default 0,
	koukai_flg int(1),
	post varchar(255),
	comment varchar(255)
);

drop table pythonGame.probability;
create table pythonGame.probability (
	id int(10),
	dec decimal(4)
);

drop table pythonGame.class;
create table pythonGame.class (
	id int(10),
	follower_id int(50),
	follower_name varchar(255)
);

drop table pythonGame.magic;
create table pythonGame.magic (
	id int not null auto_increment primary key,
	kubun int(1),
	category_id int(2),
	title text,
	body text,
	koukai_date datetime,
	start_date datetime,
	end_date datetime,
	created datetime,
	created_by varchar(255),
	modified datetime,
	modified_by varchar(255)
);

drop table pythonGame.skill;
create table pythonGame.skill (
	id int(10),
	skill_name varchar(50),
		HP int(10),
	MP int(10),
	state int(2),
	sta int(5)
	atk int(10),
	bit int(10),
	int int(10),
	def int(10),
	agi int(10),
	insdate datetime
);

drop table pythonGame.history;
create table pythonGame.history (
	killer_id int(10),
	killed_id int(10),
	turnNum int(10),
	same_flg int(1),
	upDown_flg int(1),
	del_flg int(1),
	insdate datetime
);

drop table pythonGame.talent;
create table pythonGame.talent (
	id int not null auto_increment primary key,
	kubun int(1),
	category_id int(2),
	title text,
	body text,
	koukai_date datetime,
	start_date datetime,
	end_date datetime,
	created datetime,
	created_by varchar(255),
	modified datetime,
	modified_by varchar(255)
);

/*
・大陸座標として考える
・縦横8x8として移動速度をシミュレート
*/
drop table pythonGame.area;
create table pythonGame.area (
	caegory_id int(50),
	group_id int(50),
	category_img varchar(255)
);

drop table pythonGame.mstGeneral;
create table pythonGame.mstGeneral(
	caegory_id int(50),
	group_id int(50),
	category_img varchar(255)
);

drop table pythonGame.rank;
create table pythonGame.rank (
	id int(10),
	rank char(3),
	point int(14),
	st_date datetime,
);

/*
・DMのみIDを取得
・DPを利用して改装、商品購入
*/
drop table pythonGame.dangeon;
create table pythonGame.dangeon (
	id int(10),
	rank char(3),
	point int(14),
	st_date datetime,
	create datetime,
	ob_id int(10)
);

/*
オブジェクト
・効果はアシスト、トラップ、ガチャ、配合
*/
drop table pythonGame.object;
create table pythonGame.object (
	id int(10),
	people_id(10),
	rank char(3),
	point int(14),
	st_date datetime,
	create datetime,
	ob_id int(10)	
);

drop table pythonGame.master;
create table pythonGame.master (
	id int(1),
	master_rank char(3),
	master_point int(14),
);