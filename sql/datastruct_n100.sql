-- @author wangcw
-- @copyright (c) 2024, redgreat
-- created : 2024-11-14 16:21:26
-- postgres表结构设计

-- 设置查询路径
alter role user_eadm set search_path to eadm, public;

--设置 本地时区
set time zone 'asia/shanghai';

-- 运动汇总信息表
drop table if exists workout_summary cascade;
create table workout_summary (
  id int,
  workout_id int,
  starts timestamptz,
  minutes int,
  ascent_accum decimal(10, 2),
  distance_accum decimal(10, 2),
  duration_active_accum decimal(10, 2),
  duration_paused_accum decimal(10, 2),
  duration_total_accum decimal(10, 2),
  speed_avg decimal(10, 2),
  created_at timestamptz,
  updated_at timestamptz
);

alter table workout_summary owner to user_eadm;
alter table workout_summary drop constraint if exists pk_workout_summary_id cascade;
alter table workout_summary add constraint pk_workout_summary_id primary key (id);

comment on column workout_summary.id is '自增主键';
comment on column workout_summary.workout_id is '运动信息主表id';
comment on column workout_summary.starts is '开始时间';
comment on column workout_summary.minutes is '总计时间(分钟)';
comment on column workout_summary.ascent_accum is '爬升(米)';
comment on column workout_summary.distance_accum is '总运动距离(米)';
comment on column workout_summary.duration_active_accum is '总活动时间(秒)';
comment on column workout_summary.duration_paused_accum is '总暂停时间(秒)';
comment on column workout_summary.duration_total_accum is '总运动时间(秒)';
comment on column workout_summary.speed_avg is '平均速度(米/秒)';
comment on column workout_summary.created_at is '创建时间';
comment on column workout_summary.updated_at is '更新时间';
comment on table workout_summary is '运动汇总信息表';

-- 健康详细信息表
drop table if exists workout_fits cascade;
create table workout_fits (
  id serial,
  workout_summary_id int,
  altitude decimal(10, 2),
  distance decimal(10, 2),
  enhanced_altitude decimal(10, 2),
  enhanced_speed decimal(10, 2),
  gps_accuracy int,
  grade decimal(10, 4),
  position_lat int,
  position_long int,
  speed decimal(10, 4),
  temperature decimal(10, 2),
  battery_soc decimal(10, 2),
  created_at timestamptz
);

alter table workout_fits owner to user_eadm;
alter table workout_fits drop constraint if exists pk_workout_fits_id cascade;
alter table workout_fits add constraint pk_workout_fits_id primary key (id);

comment on column workout_fits.id is '自增主键';
comment on column workout_fits.workout_summary_id is '运动汇总信息表id';
comment on column workout_fits.altitude is '海拔(米)';
comment on column workout_fits.distance is '总距离(米)';
comment on column workout_fits.enhanced_altitude is '最高海拔(米)';
comment on column workout_fits.enhanced_speed is '最高速度(米/秒)';
comment on column workout_fits.gps_accuracy is 'GPS信号质量';
comment on column workout_fits.grade is '等级(%)';
comment on column workout_fits.position_lat is '纬度';
comment on column workout_fits.position_long is '经度';
comment on column workout_fits.speed is '速度(米/秒)';
comment on column workout_fits.temperature is '温度(℃)';
comment on column workout_fits.battery_soc is '电池电量(%)';
comment on column workout_fits.created_at is '上传时间';
comment on table workout_fits is '健康详细信息表';

-- 健康信息导入记录
drop table if exists workout_imps cascade;
create table workout_imps (
  id serial,
  file_name varchar(100),
  insert_time timestamptz
);

alter table workout_imps owner to user_eadm;
alter table workout_imps drop constraint if exists pk_workout_imps_id cascade;
alter table workout_imps add constraint pk_workout_imps_id primary key (id);

comment on column workout_imps.id is '自增主键';
comment on column workout_imps.file_name is '文件名称';
comment on column workout_imps.insert_time is '数据写入时间';
comment on table workout_imps is '健康信息导入记录';

-- 健康信息表
drop table if exists workout_info cascade;
create table workout_info (
  id serial,
  starts timestamptz,
  minutes int,
  workout_type_id smallint,
  created_at timestamptz,
  updated_at timestamptz
);

alter table workout_info owner to user_eadm;
alter table workout_info drop constraint if exists pk_workout_info_id cascade;
alter table workout_info add constraint pk_workout_info_id primary key (id);

comment on column workout_info.id is '自增主键';
comment on column workout_info.starts is '开始时间';
comment on column workout_info.minutes is '持续时长';
comment on column workout_info.workout_type_id is '锻炼数据类型Id';
comment on column workout_info.created_at is '创建时间';
comment on column workout_info.updated_at is '更新时间';
comment on table workout_info is '健康信息表';
