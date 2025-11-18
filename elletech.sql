-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 10, 2025 at 07:43 PM
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
  `payment_method` varchar(50) DEFAULT NULL,
  `added_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `original_price` decimal(10,2) NOT NULL,
  `discount_applied` decimal(10,2) DEFAULT 0.00,
  `total_price` decimal(10,2) NOT NULL,
  `status` varchar(50) DEFAULT 'pending',
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `payment_method` varchar(50) DEFAULT NULL,
  `payment_status` enum('paid','unpaid') DEFAULT 'unpaid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `product_id`, `quantity`, `total_price`, `status`, `order_date`, `payment_method`, `payment_status`) VALUES
(1, 2, 2, 1, 0.00, 'Pending', '2025-10-30 09:27:24', NULL, 'unpaid'),
(2, 2, 2, 1, 0.00, 'Pending', '2025-10-30 09:27:37', NULL, 'unpaid'),
(3, 2, 2, 1, 792.00, 'Pending', '2025-10-30 09:34:53', NULL, 'unpaid'),
(4, 2, 2, 2, 1584.00, 'Pending', '2025-10-30 09:35:01', NULL, 'unpaid'),
(5, 1, 3, 1, 5999.00, 'Pending', '2025-10-30 10:30:27', NULL, 'unpaid'),
(6, 1, 3, 1, 5999.00, 'Pending', '2025-11-03 09:11:09', NULL, 'unpaid'),
(7, 1, 3, 3, 17997.00, 'Pending', '2025-11-03 09:11:18', NULL, 'unpaid'),
(8, 2, 3, 5, 29995.00, 'shipped', '2025-11-03 09:17:54', NULL, 'unpaid'),
(9, 1, 3, 3, 17997.00, 'pending', '2025-11-03 10:08:21', NULL, 'paid'),
(10, 4, 15, 1, 9212.00, 'Pending', '2025-11-09 13:11:49', 'PayMaya', 'paid'),
(11, 4, 14, 1, 6788.00, 'Pending', '2025-11-09 13:42:49', 'PayMaya', 'paid'),
(12, 4, 14, 1, 6788.00, 'delivered', '2025-11-09 13:44:04', 'GCash', 'unpaid'),
(13, 1, 13, 1, 34221.00, 'delivered', '2025-11-09 14:11:43', 'Cash on Delivery', 'paid'),
(14, 4, 14, 1, 6788.00, 'Pending', '2025-11-10 13:17:32', 'Cash on Delivery', 'unpaid'),
(15, 4, 14, 1, 6788.00, 'Pending', '2025-11-10 13:33:44', 'Cash on Delivery', 'unpaid'),
(16, 4, 15, 1, 9212.00, 'Pending', '2025-11-10 16:11:23', 'PayMaya', 'paid');

-- --------------------------------------------------------

--
-- Table structure for table `otps`
--

CREATE TABLE `otps` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `otp_code` varchar(10) NOT NULL,
  `type` varchar(50) DEFAULT 'login',
  `expires_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `otps`
--

INSERT INTO `otps` (`id`, `user_id`, `otp_code`, `type`, `expires_at`) VALUES
(2, 1, '479423', 'login', '2025-11-11 02:39:40'),
(3, 5, '973935', 'login', '2025-11-11 02:40:57'),
(4, 5, '125356', 'login', '2025-11-11 02:42:24'),
(5, 1, '863343', 'login', '2025-11-11 02:43:16');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `user_pictures`
--

CREATE TABLE `user_pictures` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `image` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
(13, 'QWERTYe', 'AFA', 34221.00, 32, 'Gaming', '2025-11-09 09:27:24', 'act2.1.1.png'),
(14, 'Laptop', 'Limited Offer', 6788.00, 6, 'Smartphones & Accessories', '2025-11-09 11:05:43', 'pict2.png.png'),
(15, 'SAC,', 'High performance laptop', 9212.00, 43, 'Computers & Laptops', '2025-11-09 12:16:20', 'RobloxScreenShot20250727_212958864.png');

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
  `membership_payment_status` enum('paid','unpaid') DEFAULT 'unpaid',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `profile_pic` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `username`, `password_hash`, `contact_no`, `address`, `role`, `membership`, `created_at`, `profile_pic`) VALUES
(1, 'ElleTech', 'epundavela.a12344954@umak.edu.ph', 'ElleTry5', 'scrypt:32768:8:1$PITOesjl0eAQa16j$c032aa27826715f3afaed4ecc45f3d4cbc1debc786ac03ca08d3afafb6da24cfbd91512121dce37c9e7ce770fb7ae57d70f07f9fd4e63d037730eb54cea254b8', '09917452191', 'taguig city', 'admin', 'Silver', '2025-10-28 18:06:29', NULL),
(2, 'Ellemar Pundavela', 'ellemarpundavela69@gmail.com', 'Ellemar', 'scrypt:32768:8:1$qex8aCnHoXqgx0xW$16f8bb67521f6e182b68c3543fc0f9e6f1e78c22b81ef5ffa41ec3bdd474a62da9085339184d61050d5f1ce0e57bf8c4f5f0a9b2c1eb4c42b9856829cfa5f4c1', '09917452191', 'taguig city', 'user', 'Basic', '2025-10-30 09:15:27', NULL),
(3, 'Jan Paul De Quiroz', 'dequirozjanpaul123@gmail.com', 'DQ', 'scrypt:32768:8:1$q5in2NhqzfbnCahe$6d4acab9f19010ab1d52c3e1bb17c0eba77c1d2b6c5a0c37cba8153a96409b86ed8a4d951158f7994170c8e77b9bc7e6c0f982c0e0290cd11ed3f525b14932ef', '09060210487', 'makati city', 'user', 'None', '2025-11-06 06:29:51', NULL),
(4, 'ElleTech', 'ellemarpundavela70@gmail.com', 'Elle', 'scrypt:32768:8:1$Jmlm9N9FO6w1RHYJ$5254353c87eec5282908045432a6091f5a7c955d91e32f2cdb57c9f316bdb9fbc1f74f250762ba6d2dec9ed3950538531cd010f02d2c734e36966c3a783cc2b6', '09917452191', 'taguig city', 'user', 'None', '2025-11-06 10:24:39', 'pexels-sebastiaan-stam-1097456.jpg'),
(5, 'Ellemar Pundavela', 'pundavelaellemar@gmail.com', 'Ramelle', 'scrypt:32768:8:1$KYWiMVhvYNKNWXVR$76aa0ea155fc4214bb4501e4bfa92582d3d5bdba62a30fae544aa9f60a507cbeeb68c96dfe9e1c5d4dc677bb8195037b54958e19741aeb6f33db697a1c206010', '09917452191', 'Blk 14 lot 12345 jc estacio vill. brgy. calzada tipas taguig city', 'user', 'None', '2025-11-10 18:17:43', NULL);

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
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `receiver_id` (`receiver_id`);

--
-- Indexes for table `otps`
--
ALTER TABLE `otps`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_pictures`
--
ALTER TABLE `user_pictures`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `otps`
--
ALTER TABLE `otps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `user_pictures`
--
ALTER TABLE `user_pictures`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `otps`
--
ALTER TABLE `otps`
  ADD CONSTRAINT `otps_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `user_pictures`
--
ALTER TABLE `user_pictures`
  ADD CONSTRAINT `user_pictures_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
