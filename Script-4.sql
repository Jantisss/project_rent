DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE IF NOT EXISTS "users" (
	"id" SERIAL PRIMARY KEY,
	"tel_number" varchar(11) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "cars" (
	"vin_code" varchar(20) NOT NULL,
	"car_reg_plate" varchar(9) NOT NULL,
	"status_id" bigint NOT NULL,
	"id" SERIAL NOT NULL,
	"model_id" bigint NOT NULL,
	"date_available" DATE,
	"cost_day" INT,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "orders" (
	"orders_id" SERIAL NOT NULL,
	"car_id" bigint NOT NULL,
	"sum" bigint NOT NULL,
	"user_id" bigint NOT NULL,
	"orders_status_id" bigint NOT NULL,
	"office_id" bigint NOT NULL,
	"date_time_reg" timestamp NOT NULL,
	"date_start" DATE NOT NULL,
	"date_end" DATE CHECK("date_start" <= "date_end"),
	PRIMARY KEY ("orders_id")
);

CREATE TABLE IF NOT EXISTS "status_table_car" (
	"status_id" SERIAL NOT NULL,
	"status_name" varchar(100) NOT NULL,
	PRIMARY KEY ("status_id")
);

CREATE TABLE IF NOT EXISTS "status_table_order" (
	"status_id" SERIAL NOT NULL,
	"status_name" varchar(100) NOT NULL,
	PRIMARY KEY ("status_id")
);

CREATE TABLE IF NOT EXISTS "models" (
	"id" SERIAL NOT NULL,
	"name_models" varchar(1000) NOT NULL,
	"brands_id" int NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "brands" (
	"id" SERIAL NOT NULL,
	"name" varchar(100) NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "status_table_office" (
	"status_id" SERIAL NOT NULL,
	"status_name" varchar(100) NOT NULL,
	PRIMARY KEY ("status_id")
);

CREATE TABLE IF NOT EXISTS "office" (
	"adress" varchar(1000),
	"name" varchar(1000) not NULL,
	"office_status_id" int NOT NULL,
	"id" SERIAL NOT NULL,
	"index" bigint,
	PRIMARY KEY ("id")
);


ALTER TABLE "cars" ADD CONSTRAINT "cars_fk2" FOREIGN KEY ("status_id") REFERENCES "status_table_car"("status_id");

ALTER TABLE "cars" ADD CONSTRAINT "cars_fk4" FOREIGN KEY ("model_id") REFERENCES "models"("id");
ALTER TABLE "orders" ADD CONSTRAINT "orders_fk1" FOREIGN KEY ("car_id") REFERENCES "cars"("id");

ALTER TABLE "orders" ADD CONSTRAINT "orders_fk2" FOREIGN KEY ("user_id") REFERENCES "users"("id");

ALTER TABLE "orders" ADD CONSTRAINT "orders_fk3" FOREIGN KEY ("orders_status_id") REFERENCES "status_table_order"("status_id");

ALTER TABLE "orders" ADD CONSTRAINT "orders_fk4" FOREIGN KEY ("office_id") REFERENCES "office"("id");

ALTER TABLE "models" ADD CONSTRAINT "models_fk1" FOREIGN KEY ("brands_id") REFERENCES "brands"("id");

ALTER TABLE "office" ADD CONSTRAINT "office_fk1" FOREIGN KEY ("office_status_id") REFERENCES "status_table_office"("status_id");
