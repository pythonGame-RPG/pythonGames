
/* 人型オブジェクト
Mはmaster_idを取得→boxが使える
DMはdangeon_idを取得→DMになれる
geneで世代を表現
 */
drop table dbo.character;
create table dbo.character (
	id int(10) not null auto_increment primary key,
	gene_id int(10) not null ,
	race_id int(10) not null ,
	name varchar(16) not null default "unknown",
	age int(4) not null default 0,
	birth datetime not null ,
	level int(10) not null default 0,
	class1 int(4) not null default 1,
	class2 int(4) not null default 0,
	class3 int(4) not null default 0,
	`rank` char(3) not null default '  G',
	HP int(10) not null default 1,
	MP int(10) not null default 1,
	state int(2) not null default 0,
	sta int(5) not null default 1,
	atk int(10) not null default 1,
	bit int(10) not null default 1,
	`int` int(10) not null default 1,
	def int(10) not null default 1,
	agi int(10) not null default 1,
	talent varchar(10),
	is_deleted tinyint(1) default 0,
	party1_id int(10) not null default 0,
	party2_id int(10) not null default 0,
	party3_id int(10) not null default 0,
	dangeon_id int(10) not null default 0,
	master_id int(10) not null default 0
)DEFAULT CHARACTER SET=utf8;


drop table python_lessons.race;
create table python_lessons.race (
	id int(10) not null auto_increment primary key,
	atk int(10),
	def int(10),
	bit int(10),
	int int(10),
	def int(10),
	agi int(10),
);

drop table python_lessons.player;
create table python_lessons.player (
	id int(10) not null auto_increment primary key,
	name varchar(8),
	level int(10),
	class_id int(10),
	HP int(10),
	MP int(10),
	atk int(10),
	def int(10),
	bit int(10),
	int int(10),
	def int(10),
	agi int(10),
	talent verchar(10),
);

drop table python_lessons.numeric;
create table python_lessons.numeric (
	id int(50) not null auto_increment primary key,
	group_id int(50),
	created datetime,
	created_by varchar(255)
);

drop table python_lessons.pattern;
create table python_lessons.pattern (
	id int(50) not null auto_increment primary key,
	group_id int(50),
	created datetime,
	created_by varchar(255)
);

drop table python_lessons.weapon;
create table python_lessons.weapon (
	id int(10) not null auto_increment primary key,
	group_id int(50),
	created datetime,
	created_by varchar(255)
);

drop table python_lessons.item;
create table python_lessons.item (
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

drop table python_lessons.probability;
create table python_lessons.probability (
	id int(10),
	dec decimal(4)
);

drop table python_lessons.class;
create table python_lessons.class (
	id int(10),
	follower_id int(50),
	follower_name varchar(255)
);

drop table python_lessons.magic;
create table python_lessons.magic (
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

drop table python_lessons.slill;
create table python_lessons.slill (
	topics_id int(50),
	topics_img varchar(255),
	created datetime
);

drop table python_lessons.talent;
create table python_lessons.talent (
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
drop table python_lessons.area;
create table python_lessons.area (
	caegory_id int(50),
	group_id int(50),
	category_img varchar(255)
);

drop table python_lessons.mstGeneral;
create table python_lessons.mstGeneral(
	caegory_id int(50),
	group_id int(50),
	category_img varchar(255)
);

drop table python_lessons.rank;
create table python_lessons.rank (
	id int(10),
	rank char(3),
	point int(14),
	st_date datetime,
);

/*
・DMのみIDを取得
・DPを利用して改装、商品購入
*/
drop table python_lessons.dangeon;
create table python_lessons.dangeon (
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
drop table python_lessons.object;
create table python_lessons.object (
	id int(10),
	people_id(10),
	rank char(3),
	point int(14),
	st_date datetime,
	create datetime,
	ob_id int(10)	
);

drop table python_lessons.master;
create table python_lessons.master (
	id int(1),
	master_rank char(3),
	master_point int(14),
);