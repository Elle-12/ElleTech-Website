-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 06, 2025 at 11:59 AM
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
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `total_price` decimal(10,2) NOT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  `order_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `product_id`, `quantity`, `total_price`, `status`, `order_date`) VALUES
(1, 2, 2, 1, 0.00, 'Pending', '2025-10-30 09:27:24'),
(2, 2, 2, 1, 0.00, 'Pending', '2025-10-30 09:27:37'),
(3, 2, 2, 1, 792.00, 'Pending', '2025-10-30 09:34:53'),
(4, 2, 2, 2, 1584.00, 'Pending', '2025-10-30 09:35:01'),
(5, 1, 3, 1, 5999.00, 'Pending', '2025-10-30 10:30:27'),
(6, 1, 3, 1, 5999.00, 'Pending', '2025-11-03 09:11:09'),
(7, 1, 3, 3, 17997.00, 'Pending', '2025-11-03 09:11:18'),
(8, 2, 3, 5, 29995.00, 'Pending', '2025-11-03 09:17:54'),
(9, 1, 3, 3, 17997.00, 'delivered', '2025-11-03 10:08:21');

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
(1, 'Ellen', 'jhdbjcbf', 500.00, 25, NULL, '2025-10-30 09:07:09', NULL),
(2, 'Ellemar', 'Talaga', 792.00, 55, NULL, '2025-10-30 09:13:25', NULL),
(3, 'Laptop', 'Limited Offer', 5999.00, 5, NULL, '2025-10-30 09:37:44', NULL),
(4, 'sUSHI', '5 TIMES A DAY', 59.00, 100, NULL, '2025-11-03 10:12:57', NULL),
(5, 'SAMPLE', 'AFA', 200.00, 2, NULL, '2025-11-03 10:13:37', NULL),
(6, 'LaptoppH', 'AFA', 1231.00, 4, NULL, '2025-11-03 10:13:59', NULL),
(7, 'sample2', 'AFA', 21231.00, 23, NULL, '2025-11-03 10:44:25', NULL),
(9, 'Laptop', 'High performance laptop', 50000.00, 2, NULL, '2025-11-06 05:52:21', NULL),
(10, 'Mouse', 'Wireless mouse', 500.00, 50, NULL, '2025-11-06 05:52:21', NULL),
(11, 'Keyboard', 'Mechanical keyboard', 2000.00, 20, NULL, '2025-11-06 05:52:21', NULL),
(12, 'QWERTY', 'AFA', 60218.00, 56, NULL, '2025-11-06 09:14:24', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `username` varchar(80) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `contact_no` varchar(50) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `membership` varchar(50) DEFAULT 'None',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `username`, `password_hash`, `contact_no`, `address`, `role`, `membership`, `created_at`) VALUES
(1, 'ElleTech', 'epundavela.a12344954@umak.edu.ph', 'ElleTry5', 'scrypt:32768:8:1$PITOesjl0eAQa16j$c032aa27826715f3afaed4ecc45f3d4cbc1debc786ac03ca08d3afafb6da24cfbd91512121dce37c9e7ce770fb7ae57d70f07f9fd4e63d037730eb54cea254b8', '09917452191', 'taguig city', 'admin', 'Silver', '2025-10-28 18:06:29'),
(2, 'Ellemar Pundavela', 'ellemarpundavela69@gmail.com', 'Ellemar', 'scrypt:32768:8:1$qex8aCnHoXqgx0xW$16f8bb67521f6e182b68c3543fc0f9e6f1e78c22b81ef5ffa41ec3bdd474a62da9085339184d61050d5f1ce0e57bf8c4f5f0a9b2c1eb4c42b9856829cfa5f4c1', '09917452191', 'taguig city', 'user', 'Basic', '2025-10-30 09:15:27'),
(3, 'Jan Paul De Quiroz', 'dequirozjanpaul123@gmail.com', 'DQ', 'scrypt:32768:8:1$q5in2NhqzfbnCahe$6d4acab9f19010ab1d52c3e1bb17c0eba77c1d2b6c5a0c37cba8153a96409b86ed8a4d951158f7994170c8e77b9bc7e6c0f982c0e0290cd11ed3f525b14932ef', '09060210487', 'makati city', 'user', 'None', '2025-11-06 06:29:51'),
(4, 'ElleTech', 'ellemarpundavela70@gmail.com', 'Elle', 'scrypt:32768:8:1$Jmlm9N9FO6w1RHYJ$5254353c87eec5282908045432a6091f5a7c955d91e32f2cdb57c9f316bdb9fbc1f74f250762ba6d2dec9ed3950538531cd010f02d2c734e36966c3a783cc2b6', '09917452191', 'taguig city', 'user', 'None', '2025-11-06 10:24:39');

--
-- Indexes for dumped tables
--

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
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

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
