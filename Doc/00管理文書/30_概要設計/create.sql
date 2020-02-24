
/* 人型オブジェクト
Mはmaster_idを取得→boxが使える
DMはdangeon_idを取得→DMになれる
geneで世代を表現
 */
drop table pythonGame.people;
create table pythonGame.people (
	id int(10) not null auto_increment primary key,
	g_id int(10),
	gene int(4),
	name int(8),
	birth datetime,
	level int(10),
	class1 int(4),
	class2 int(4),
	class3 int(4),
	rank char(3),
	HP int(10),
	MP int(10),
	state int(2),
	sta int(5)
	atk int(10),
	def int(10),
	bit int(10),
	int int(10),
	def int(10),
	agi int(10),
	talent verchar(10),
	del_flg tinyint(1),
	serve1_id int(10),
	serve2_id int(10),
	serve3_id int(10),
	dangeon_id int(10),
	master_id int(10),
);

drop table pythonGame.race;
create table pythonGame.race (
	id int(10) not null auto_increment primary key,
	atk int(10),
	def int(10),
	bit int(10),
	int int(10),
	def int(10),
	agi int(10),
);

drop table pythonGame.player;
create table pythonGame.player (
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