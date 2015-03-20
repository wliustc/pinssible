CREATE TABLE `amazon_item` (
  `asin` varchar(32) NOT NULL,
  `title` varchar(256) DEFAULT NULL,
  `category` varchar(256) DEFAULT NULL,
  `brand` varchar(64) DEFAULT NULL,
  `shipping` varchar(16) DEFAULT NULL,
  `star` float DEFAULT NULL,
  `views` int(11) DEFAULT NULL,
  `feature` text,
  `description` text,
  `details` text,
  `weight` int(11) DEFAULT NULL,
  `length` int(11) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `sales_rank` int(11) DEFAULT NULL,
  `list_price` float DEFAULT NULL,
  `sale_price` float DEFAULT NULL,
  `comments` text,
  `fetch_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `detailed_comments` text,
  `image_small` varchar(256) DEFAULT NULL,
  `image_big` varchar(256) DEFAULT NULL,
  `image_list` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`asin`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


 CREATE TABLE `camel_item` (
  `asin` varchar(64) NOT NULL,
  `is_best` tinyint(4) DEFAULT NULL,
  `sale_price` float DEFAULT NULL,
  `list_price` float DEFAULT NULL,
  `fetch_day` int(11) DEFAULT NULL,
  PRIMARY KEY (`asin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8