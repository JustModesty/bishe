use gdutnews;

drop table if exists `gdut_schoolnews`;
CREATE TABLE IF NOT EXISTS `gdut_schoolnews`(
   `id` INT UNSIGNED AUTO_INCREMENT primary key,
   `link` VARCHAR(500) NOT NULL,
   `title` VARCHAR(500) NOT NULL,
   `src` VARCHAR(500),
   `date` VARCHAR(500)
)ENGINE=InnoDB;

select * from gdut_schoolnews;
