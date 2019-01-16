-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Gegenereerd op: 11 jan 2019 om 15:31
-- Serverversie: 10.1.37-MariaDB-0+deb9u1
-- PHP-versie: 7.0.33-0+deb9u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smartiot`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `logs`
--

CREATE TABLE `logs` (
  `log_Id` int(11) NOT NULL,
  `info` varchar(1000) NOT NULL,
  `date_Time` datetime NOT NULL,
  `user_Id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `route_permissions`
--

CREATE TABLE `route_permissions` (
  `perm_Id` int(11) NOT NULL,
  `perm_Endpoints` varchar(50) NOT NULL,
  `userid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Gegevens worden geëxporteerd voor tabel `route_permissions`
--

INSERT INTO `route_permissions` (`perm_Id`, `perm_Endpoints`, `userid`) VALUES
(1, 'all', 1);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `naam` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Gegevens worden geëxporteerd voor tabel `users`
--

INSERT INTO `users` (`id`, `naam`, `email`, `username`, `password`, `role`, `register_date`) VALUES
(1, 'Singh Kiran', 'singh.kiran2456@hotmail.com', 'admin', '$5$rounds=535000$AuqSgpAX8B.IGlJ8$9Mvu8V1GwwiUuS74WwWYPYe9060HvyVl9yMDy7GSCQ4', 'admin', '2019-01-11 19:49:37'),
(2, 'Koen', 'koen4551@hotmail.com', 'koen', '$5$rounds=535000$QJGoSILip7hkIrB1$SFe8SAB9b41o2FZBmYGY8bgnjzWIiHN7DijSQDmDzw8', 'normal_user', '2019-01-11 19:51:49');

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`log_Id`);

--
-- Indexen voor tabel `route_permissions`
--
ALTER TABLE `route_permissions`
  ADD PRIMARY KEY (`perm_Id`);

--
-- Indexen voor tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT voor geëxporteerde tabellen
--

--
-- AUTO_INCREMENT voor een tabel `logs`
--
ALTER TABLE `logs`
  MODIFY `log_Id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT voor een tabel `route_permissions`
--
ALTER TABLE `route_permissions`
  MODIFY `perm_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT voor een tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
