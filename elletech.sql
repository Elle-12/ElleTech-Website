-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 20, 2025 at 05:07 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `elletech`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `payment_method` varchar(50) NOT NULL,
  `added_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `user_id`, `product_id`, `quantity`, `payment_method`, `added_at`) VALUES
(40, 1, 15, 1, 'Cash on Delivery', '2025-11-17 05:20:19'),
(41, 1, 21, 1, 'Cash on Delivery', '2025-11-17 06:19:14');

-- --------------------------------------------------------

--
-- Table structure for table `chats`
--

CREATE TABLE `chats` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_read` tinyint(1) DEFAULT 0,
  `message_type` enum('text','image','file') DEFAULT 'text',
  `file_path` varchar(500) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `chats`
--

INSERT INTO `chats` (`id`, `sender_id`, `receiver_id`, `message`, `created_at`, `is_read`, `message_type`, `file_path`, `updated_at`) VALUES
(1, 5, 1, 'hello po', '2025-11-19 12:34:20', 1, 'text', NULL, '2025-11-19 17:43:00'),
(2, 5, 1, 'hayup kaba', '2025-11-19 12:34:57', 1, 'text', NULL, '2025-11-19 17:43:00'),
(3, 17, 1, 'hello po', '2025-11-19 16:23:13', 1, 'text', NULL, '2025-11-19 17:43:35'),
(4, 17, 1, 'wala lng', '2025-11-19 19:43:49', 0, 'text', NULL, '2025-11-19 19:43:49'),
(5, 5, 1, 'wala lng', '2025-11-20 03:26:02', 0, 'text', NULL, '2025-11-20 03:26:02');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `is_read` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `sender_id`, `receiver_id`, `message`, `timestamp`, `is_read`) VALUES
(1, 5, 1, 'aegasb', '2025-11-17 14:52:49', 0),
(2, 5, 1, 'hiiii', '2025-11-17 14:53:03', 0),
(3, 17, 1, 'hello?', '2025-11-17 18:43:54', 0),
(4, 5, 1, 'ano tooo', '2025-11-18 17:34:05', 0);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `original_price` decimal(10,2) DEFAULT 0.00,
  `discount_applied` decimal(5,4) DEFAULT 0.0000,
  `total_price` decimal(10,2) NOT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `payment_method` varchar(50) DEFAULT NULL,
  `payment_status` enum('paid','unpaid') DEFAULT 'unpaid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `product_id`, `quantity`, `original_price`, `discount_applied`, `total_price`, `status`, `order_date`, `payment_method`, `payment_status`) VALUES
(1, 2, 2, 1, 0.00, 0.0000, 0.00, 'delivered', '2025-10-30 09:27:24', NULL, 'paid'),
(2, 2, 2, 1, 0.00, 0.0000, 0.00, 'shipped', '2025-10-30 09:27:37', NULL, 'unpaid'),
(3, 2, 2, 1, 0.00, 0.0000, 792.00, 'delivered', '2025-10-30 09:34:53', NULL, 'paid'),
(4, 2, 2, 2, 0.00, 0.0000, 1584.00, 'Pending', '2025-10-30 09:35:01', NULL, 'unpaid'),
(5, 1, 3, 1, 0.00, 0.0000, 5999.00, 'Pending', '2025-10-30 10:30:27', NULL, 'unpaid'),
(6, 1, 3, 1, 0.00, 0.0000, 5999.00, 'Pending', '2025-11-03 09:11:09', NULL, 'unpaid'),
(7, 1, 3, 3, 0.00, 0.0000, 17997.00, 'Pending', '2025-11-03 09:11:18', NULL, 'unpaid'),
(8, 2, 3, 5, 0.00, 0.0000, 29995.00, 'shipped', '2025-11-03 09:17:54', NULL, 'unpaid'),
(9, 1, 3, 3, 0.00, 0.0000, 17997.00, 'pending', '2025-11-03 10:08:21', NULL, 'paid'),
(10, 4, 15, 1, 0.00, 0.0000, 9212.00, 'Pending', '2025-11-09 13:11:49', 'PayMaya', 'paid'),
(11, 4, 14, 1, 0.00, 0.0000, 6788.00, 'Pending', '2025-11-09 13:42:49', 'PayMaya', 'paid'),
(12, 4, 14, 1, 0.00, 0.0000, 6788.00, 'delivered', '2025-11-09 13:44:04', 'GCash', 'unpaid'),
(13, 1, 13, 1, 0.00, 0.0000, 34221.00, 'delivered', '2025-11-09 14:11:43', 'Cash on Delivery', 'paid'),
(14, 4, 14, 1, 0.00, 0.0000, 6788.00, 'Pending', '2025-11-10 13:17:32', 'Cash on Delivery', 'unpaid'),
(15, 4, 14, 1, 0.00, 0.0000, 6788.00, 'Pending', '2025-11-10 13:33:44', 'Cash on Delivery', 'unpaid'),
(16, 4, 15, 1, 0.00, 0.0000, 9212.00, 'Pending', '2025-11-10 16:11:23', 'PayMaya', 'paid'),
(18, 5, 17, 1, 0.00, 0.0000, 4690.80, 'delivered', '2025-11-10 20:07:11', 'Cash on Delivery', 'paid'),
(24, 4, 19, 1, 0.00, 0.0000, 700.00, 'Pending', '2025-11-13 04:43:30', 'GCash', 'unpaid'),
(25, 15, 18, 1, 0.00, 0.0000, 999.00, 'Pending', '2025-11-13 06:18:07', 'Cash on Delivery', 'unpaid'),
(35, 5, 19, 2, 1400.00, 0.1500, 1190.00, 'Pending', '2025-11-13 10:30:08', 'Cash on Delivery', 'unpaid'),
(36, 5, 17, 2, 10424.00, 0.1500, 8860.40, 'Pending', '2025-11-13 10:30:08', 'Cash on Delivery', 'unpaid'),
(37, 5, 19, 1, 700.00, 0.1500, 595.00, 'Pending', '2025-11-13 13:01:56', 'Cash on Delivery', 'unpaid'),
(41, 1, 15, 1, 9212.00, 0.1000, 8290.80, 'pending', '2025-11-13 17:24:21', 'Cash on Delivery', 'unpaid'),
(42, 1, 13, 1, 34221.00, 0.1000, 30798.90, 'pending', '2025-11-13 17:24:21', 'Cash on Delivery', 'unpaid'),
(52, 5, 17, 1, 5212.00, 0.1500, 4430.20, 'pending', '2025-11-14 16:25:18', 'GCash', 'paid'),
(56, 17, 19, 1, 700.00, 0.0000, 700.00, 'pending', '2025-11-14 19:00:53', 'Cash on Delivery', 'unpaid'),
(57, 5, 19, 1, 700.00, 0.1000, 630.00, 'pending', '2025-11-14 19:26:40', 'GCash', 'paid'),
(58, 5, 14, 1, 6788.00, 0.1000, 6109.20, 'pending', '2025-11-14 19:29:47', 'GCash', 'paid'),
(59, 5, 19, 1, 700.00, 0.1000, 630.00, 'pending', '2025-11-14 19:30:02', 'GCash', 'paid'),
(60, 5, 18, 1, 999.00, 0.1000, 899.10, 'pending', '2025-11-14 19:45:11', 'Cash on Delivery', 'paid'),
(61, 5, 19, 1, 700.00, 0.1000, 630.00, 'pending', '2025-11-14 20:34:01', 'Cash on Delivery', 'paid'),
(62, 5, 15, 3, 27636.00, 0.1000, 24872.40, 'pending', '2025-11-14 21:07:53', 'PayMaya', 'paid'),
(63, 5, 18, 1, 999.00, 0.1000, 899.10, 'pending', '2025-11-14 22:46:45', 'PayMaya', 'paid'),
(64, 5, 18, 1, 999.00, 0.1000, 899.10, 'pending', '2025-11-15 00:28:12', 'GCash', 'paid'),
(65, 5, 19, 1, 700.00, 0.1000, 630.00, 'pending', '2025-11-15 03:08:15', 'GCash', 'paid'),
(66, 5, 19, 1, 700.00, 0.1000, 630.00, 'delivered', '2025-11-15 12:57:43', 'GCash', 'unpaid'),
(67, 5, 18, 1, 999.00, 0.1000, 899.10, 'delivered', '2025-11-15 12:57:43', 'Cash on Delivery', 'unpaid'),
(68, 5, 17, 1, 5212.00, 0.1000, 4690.80, 'delivered', '2025-11-15 12:57:43', 'Cash on Delivery', 'unpaid'),
(69, 5, 15, 3, 27636.00, 0.1000, 24872.40, 'delivered', '2025-11-15 12:57:43', 'Cash on Delivery', 'unpaid'),
(70, 5, 19, 1, 700.00, 0.1000, 630.00, 'pending', '2025-11-17 04:40:42', 'Cash on Delivery', 'unpaid'),
(71, 5, 18, 4, 3996.00, 0.1000, 3596.40, 'pending', '2025-11-17 04:47:46', 'Cash on Delivery', 'unpaid'),
(72, 5, 15, 7, 64484.00, 0.1000, 58035.60, 'pending', '2025-11-17 04:47:46', 'Cash on Delivery', 'paid'),
(73, 5, 17, 1, 5212.00, 0.1000, 4690.80, 'pending', '2025-11-17 04:47:46', 'GCash', 'paid'),
(74, 17, 21, 1, 2424.00, 0.0000, 2424.00, 'delivered', '2025-11-17 11:31:17', 'Cash on Delivery', 'unpaid'),
(75, 5, 23, 1, 21131.00, 0.1000, 19017.90, 'pending', '2025-11-18 09:22:36', 'GCash', 'paid'),
(76, 5, 23, 1, 21131.00, 0.1000, 19017.90, 'pending', '2025-11-18 09:22:46', 'Cash on Delivery', 'unpaid'),
(77, 5, 18, 1, 999.00, 0.1000, 899.10, 'pending', '2025-11-18 09:22:46', 'Cash on Delivery', 'paid'),
(78, 5, 21, 5, 12120.00, 0.1000, 10908.00, 'pending', '2025-11-18 09:22:46', 'Cash on Delivery', 'unpaid'),
(79, 5, 24, 1, 99.99, 0.1000, 89.99, 'pending', '2025-11-18 09:33:53', 'Cash on Delivery', 'paid'),
(80, 5, 24, 1, 99.99, 0.0000, 99.99, 'delivered', '2025-11-18 13:46:30', 'Cash on Delivery', 'unpaid'),
(81, 5, 24, 1, 99.99, 0.1500, 84.99, 'pending', '2025-11-18 16:17:20', 'Cash on Delivery', 'unpaid'),
(82, 5, 27, 1, 9.99, 0.0000, 9.99, 'pending', '2025-11-18 23:40:36', 'Cash on Delivery', 'unpaid'),
(83, 5, 24, 2, 199.98, 0.1000, 179.98, 'pending', '2025-11-19 05:03:02', 'Cash on Delivery', 'unpaid'),
(84, 5, 26, 3, 149.97, 0.1000, 134.97, 'pending', '2025-11-19 05:03:02', 'Cash on Delivery', 'paid'),
(85, 5, 28, 1, 79.99, 0.1000, 71.99, 'pending', '2025-11-19 05:03:02', 'Cash on Delivery', 'unpaid'),
(86, 5, 18, 1, 999.00, 0.1500, 849.15, 'pending', '2025-11-19 10:04:05', 'Cash on Delivery', 'paid'),
(87, 5, 27, 1, 9.99, 0.1500, 8.49, 'pending', '2025-11-19 10:45:43', 'Cash on Delivery', 'unpaid'),
(88, 5, 24, 1, 99.99, 0.0000, 99.99, 'paid', '2025-11-19 14:35:26', 'Cash on Delivery', 'unpaid'),
(89, 5, 26, 1, 49.99, 0.0000, 49.99, 'delivered', '2025-11-19 15:35:13', 'Cash on Delivery', 'unpaid'),
(90, 5, 13, 1, 34221.00, 0.0000, 34221.00, 'cancelled', '2025-11-19 15:42:58', 'Cash on Delivery', 'unpaid');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT 0.00,
  `stock_qty` int(11) NOT NULL DEFAULT 0,
  `category` varchar(80) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `stock_qty`, `category`, `created_at`, `image`) VALUES
(13, 'QWERTYe', 'AFA', 34221.00, 30, 'Gaming', '2025-11-09 09:27:24', 'act2.1.1.png'),
(14, 'Laptop', 'Limited Offer', 6788.00, 7, 'Smartphones & Accessories', '2025-11-09 11:05:43', 'pict2.png.png'),
(15, 'SAC,', 'High performance laptop', 9212.00, 31, 'Computers & Laptops', '2025-11-09 12:16:20', 'RobloxScreenShot20250727_212958864.png'),
(17, 'Watch 30Kl', 'Limited Offer', 5212.00, 0, 'Smartphones & Accessories', '2025-11-10 18:52:31', 'pexels-sebastiaan-stam-1097456.jpg'),
(18, 'Speaker', 'louder than you', 999.00, 44, 'Audio & Headphones', '2025-11-10 20:18:17', 'PUNDAVELA_ACT_1.png'),
(19, 'CiscoPacket Tracer', 'Limited Offer', 700.00, 44, 'Smartphones & Accessories', '2025-11-13 04:27:50', 'PUNDAVELA_ACT_1.1.png'),
(21, 'QWERTY', 'AFA', 2424.00, 6, 'Computers & Laptops', '2025-11-17 05:37:23', 'df99199d8fe73e5f32dbb632c45b1b24_0.jpeg'),
(22, 'QWERTY', 'Limited Offer', 3234.00, 32, 'Smartphones & Accessories', '2025-11-17 12:09:56', 'act2.1.1.png'),
(23, 'Laptop', 'High performance laptop', 21131.00, 11, 'Gaming', '2025-11-17 12:12:42', 'Screenshot_2025-08-18_085418.png'),
(24, 'Wireless Headphones', 'High-quality wireless headphones with noise cancellation.', 99.99, 44, 'Electronics', '2025-11-18 09:25:35', NULL),
(25, 'Smartphone Case', 'Protective case for smartphones.', 19.99, 100, 'Accessories', '2025-11-18 09:25:35', NULL),
(26, 'Laptop Stand', 'Adjustable laptop stand for better ergonomics.', 49.99, 26, 'Electronics', '2025-11-18 09:25:35', NULL),
(27, 'USB Cable', 'Fast charging USB cable.', 9.99, 198, 'Accessories', '2025-11-18 09:25:35', NULL),
(28, 'Bluetooth Speaker', 'Portable Bluetooth speaker with great sound.', 79.99, 39, 'Electronics', '2025-11-18 09:25:35', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `username` varchar(80) NOT NULL,
  `password_hash` text NOT NULL,
  `contact_no` varchar(50) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `membership` varchar(50) DEFAULT 'None',
  `membership_payment_status` enum('paid','unpaid') DEFAULT 'unpaid',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `profile_pic` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `username`, `password_hash`, `contact_no`, `address`, `role`, `membership`, `membership_payment_status`, `created_at`, `profile_pic`) VALUES
(1, 'ElleTech', 'admin@elletech.com', 'ElleTry5', 'pbkdf2:sha256:600000', '09917452191', 'taguig city', 'admin', 'Silver', 'paid', '2025-10-28 18:06:29', NULL),
(2, 'Ellemar Pundavela', 'ellemarpundavela69@gmail.com', 'Ellemar', 'scrypt:32768:8:1$qex8aCnHoXqgx0xW$16f8bb67521f6e182b68c3543fc0f9e6f1e78c22b81ef5ffa41ec3bdd474a62da9085339184d61050d5f1ce0e57bf8c4f5f0a9b2c1eb4c42b9856829cfa5f4c1', '09917452191', 'taguig city', 'user', 'Basic', 'paid', '2025-10-30 09:15:27', NULL),
(4, 'Ellemar', 'ellemarpundavela70@gmail.com', 'Elle', 'scrypt:32768:8:1$Jmlm9N9FO6w1RHYJ$5254353c87eec5282908045432a6091f5a7c955d91e32f2cdb57c9f316bdb9fbc1f74f250762ba6d2dec9ed3950538531cd010f02d2c734e36966c3a783cc2b6', '09917452191', 'makati city', 'user', 'None', 'unpaid', '2025-11-06 10:24:39', 'pexels-sebastiaan-stam-1097456.jpg'),
(5, 'Ellemar Pundavela', 'pundavelaellemar@gmail.com', 'Ramelle', 'pbkdf2:sha256:600000$GsTsbowhBtTmLvRz$69f78bf16b2bd7eedde2ae442299ea4c90db1dbd2f5e3a30bf96bdd71f709463', '09917452191', 'Blk 14 lot 12345 jc estacio vill. brgy. calzada tipas taguig city', 'user', 'Gold', 'unpaid', '2025-11-10 18:17:43', 'inbound1964309709713199277.jpg'),
(6, 'Jan Paul De Quiroz', 'dequirozjanpaul123@gmail.com', 'DQ', 'pbkdf2:sha256:600000$Ltl1ACDPWVRZntkF$a1d41adbc631e62f399bbbd07ac836760a438d2f4eeda9175b369c343a11c980', '09060210487', 'Taguig city', 'user', 'None', 'unpaid', '2025-11-13 03:40:45', NULL),
(7, 'Test User', 'test@example.com', 'testuser', 'pbkdf2:sha256:600000$vfnWhDMkntrkUchq$413cb28e6f337535a2c9182e8629650e46141524b7d82910806ed36ecbb03cc9', '1234567890', 'Test Address', 'user', 'None', 'unpaid', '2025-11-13 04:15:21', NULL),
(15, 'CampusCare', 'araymo\r\n', 'camp', 'pbkdf2:sha256:600000$wwFn7LQ175T8GQHq$19577ce90a22b87466df5e0eee14678d17bcd058b4501afc6379782dede4f059', '09917452191', 'taguig city', 'user', 'Gold', 'paid', '2025-11-13 06:17:13', NULL),
(16, 'Rose Ann Tolentino', 'roseanntolentino0608@gmail.com', 'Ann', 'pbkdf2:sha256:600000$31GrAaO71QDyZW8k$a6cd4b5a9675de8e8200a6878410ebad1ac7a68ad04a85396c7a443f3a6678db', '', '', 'user', 'None', 'unpaid', '2025-11-13 08:41:28', NULL),
(17, 'CampusCare', 'campuscareapp@gmail.com', 'test', 'pbkdf2:sha256:600000$Mav8EVf9s4vmAxNt$34053cfaa908c8e9bda2b0c83a7fa015af49f788f9adbf7926c9070521b4f8a4', '09917452191', 'taguig city', 'admin', 'None', 'unpaid', '2025-11-14 17:58:41', NULL),
(19, 'ElleTech', 'ellemarpundavela199@gmail.com', 'bambs', 'pbkdf2:sha256:600000$JDF36zLoJSxT4myK$fba268b41acd066da47a3c66684a7493286e3e09e89eba89c60b60cca7f82298', '09917452191', 'taguig city', 'user', 'None', 'unpaid', '2025-11-18 09:26:51', NULL),
(20, 'Test User', 'testuser@example.com', 'testuser123', 'pbkdf2:sha256:600000$vh76Y2996HtU9I6j$598b08fa6645fd572ddd72261378e50ba6dad13163842062bb09c34d0a21d141', '1234567890', 'Test Address', 'user', 'None', 'unpaid', '2025-11-18 12:21:48', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `chats`
--
ALTER TABLE `chats`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `receiver_id` (`receiver_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `chats`
--
ALTER TABLE `chats`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
