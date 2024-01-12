-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 12, 2024 at 04:21 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.3.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `scheduler`
--

-- --------------------------------------------------------

--
-- Table structure for table `assinedtable`
--

CREATE TABLE `assinedtable` (
  `id` int(11) NOT NULL,
  `taskId` int(225) NOT NULL,
  `userId` int(225) NOT NULL,
  `sprintId` int(225) NOT NULL,
  `projectedDate` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `assinedtable`
--

INSERT INTO `assinedtable` (`id`, `taskId`, `userId`, `sprintId`, `projectedDate`) VALUES
(1, 15, 5, 3, '2024-02-03'),
(2, 20, 6, 3, '2024-02-07'),
(3, 19, 6, 3, '2024-02-10'),
(4, 14, 5, 3, '2024-02-06'),
(5, 18, 5, 3, '2024-02-09'),
(6, 16, 6, 3, '2024-02-12');

-- --------------------------------------------------------

--
-- Table structure for table `sprints`
--

CREATE TABLE `sprints` (
  `id` int(225) NOT NULL,
  `sprintName` varchar(225) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `sprintId` int(225) NOT NULL,
  `status` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sprints`
--

INSERT INTO `sprints` (`id`, `sprintName`, `startDate`, `endDate`, `sprintId`, `status`) VALUES
(1, 'Dummy sprint', '2024-01-18', '2024-02-01', 0, 'notPlanned'),
(2, 'New Sprint', '2024-01-25', '2024-02-08', 0, 'notPlanned'),
(3, 'Thursday', '2024-01-31', '2024-02-14', 0, 'Planned');

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

CREATE TABLE `tasks` (
  `sno` int(225) NOT NULL,
  `taskName` varchar(225) NOT NULL,
  `taskDesc` varchar(225) NOT NULL,
  `priority` int(225) NOT NULL,
  `needBy` varchar(225) NOT NULL,
  `points` int(225) NOT NULL,
  `sprintId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tasks`
--

INSERT INTO `tasks` (`sno`, `taskName`, `taskDesc`, `priority`, `needBy`, `points`, `sprintId`) VALUES
(2, 'Task 1', 'desc', 3, '2024-02-01', 2, 1),
(3, 'Task 2', 'desc', 3, '2024-02-01', 3, 1),
(4, 'Task 3', 'desc', 2, '2024-02-01', 3, 1),
(5, 'Task 4', 'Task 5', 1, '2024-02-01', 7, 1),
(6, 'Task 9', 'Desc', 2, '2024-02-01', 3, 1),
(7, 'Task 88', 'desc', 1, '2024-02-01', 2, 1),
(8, 'Task 1', 'Desc', 2, '2024-01-31', 7, 2),
(9, 'Task 2', 'Desc', 3, '2024-02-02', 2, 2),
(11, 'Task 3', 'Desc', 1, '2024-02-06', 3, 2),
(12, 'Task 4', 'Desc', 1, '2024-02-06', 7, 2),
(13, 'Task 6', 'desc', 3, '2024-02-06', 1, 2),
(14, 'T1', 'desc', 2, '2024-02-08', 3, 3),
(15, 'T2', 'desc', 3, '2024-02-05', 3, 3),
(16, 'T3', 'Desc', 1, '2024-02-14', 2, 3),
(18, 'T5', 'DESC', 2, '2024-02-09', 3, 3),
(19, 't4', 'desc', 3, '2024-02-14', 3, 3),
(20, 'T8', 'DESC', 3, '2024-02-06', 7, 3);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(225) NOT NULL,
  `userName` varchar(225) NOT NULL,
  `userEmail` varchar(225) NOT NULL,
  `sprintId` int(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `userName`, `userEmail`, `sprintId`) VALUES
(1, 'user 1', 'tkkarthik23@gmail.com', 1),
(2, 'User 2', 'kthokala@syr.edu', 1),
(3, 'Karthik', 'karthikthokala6295@gmail.com', 2),
(4, 'Azhar', 'azharDummy@example.com', 2),
(5, 'Thokala', 'karthikthokala6295@gmail.com', 3),
(6, 'Azhar', 'az@exaple.com', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `assinedtable`
--
ALTER TABLE `assinedtable`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sprints`
--
ALTER TABLE `sprints`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `assinedtable`
--
ALTER TABLE `assinedtable`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `sprints`
--
ALTER TABLE `sprints`
  MODIFY `id` int(225) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `sno` int(225) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(225) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
