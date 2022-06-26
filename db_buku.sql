-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 24 Jun 2022 pada 16.22
-- Versi server: 10.4.24-MariaDB
-- Versi PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `heroku_82c5fa00d5406b1`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_buku`
--

CREATE TABLE `tbl_buku` (
  `id_buku` int(11) NOT NULL,
  `judul` varchar(250) NOT NULL,
  `penerbit` varchar(50) NOT NULL,
  `tahun_terbit` int(11) NOT NULL,
  `tempat_terbit` varchar(50) NOT NULL,
  `pengarang` varchar(50) NOT NULL,
  `kategori` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `tbl_buku`
--

INSERT INTO `tbl_buku` (`id_buku`, `judul`, `penerbit`, `tahun_terbit`, `tempat_terbit`, `pengarang`, `kategori`) VALUES
(153, 'Pendidikan Agama Islam', 'Noura Books', 2004, 'Jakarta', 'Wahyudin, Achmad, M.Ilyas, M.Saifullah', 'umum'),
(154, 'Tuhan Ada di Hatimu', 'Noura Books', 2018, 'Jakarta', 'Husein Jafar Al-Hadar', 'agama'),
(155, 'Why? Computer Virus - Virus Komputer', 'Elex Media Komputindo', 2021, 'Jakarta', 'YeaRimDang ', 'komputer'),
(157, 'Akuntansi Sektor Publik', 'Erlangga', 2020, 'Jakarta', 'Indra Bastian', 'akuntansi'),
(158, 'Mahir Dan Terampil Belajar Elektronika Untuk Pemula', 'Deepublish', 2018, 'Bandung', 'Udik Wahyudi', 'elektronika'),
(159, 'PENGANTAR FARMASI SOSIAL', 'SCOPINDO MEDIA PUSTAKA', 2020, 'Semarang', 'apt. Putu Eka Arimbawa, S.Farm., M.Kes', 'farmasi'),
(161, 'Food & Beverage And Table Setting', 'Grasindo', 2019, 'Yogyakarta', 'FY Djoko Subroto', 'perhotelan'),
(162, 'Why? Medical Equipment - Alat-Alat Kesehatan', 'Elex Media Komputindo', 2021, 'Bandung', 'YeaRimDang', 'teknik'),
(163, 'Ilmu Diet yang Sehat dan Alami', 'Prenada Media', 2018, 'Jakarta', 'Fajar Junaedi', 'kesehatan'),
(164, 'Merawat dan Memperbaiki Mesin Cuci', 'Penerbit Agromedia Pustaka', 2019, 'Jakarta', 'M. Hidayat', 'mesin'),
(165, 'The Japanese Textbook Problem and Solution, 1945-1946', 'Stanford University', 1952, 'California', 'Herbert John Wunderlich', 'textbook');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_kategori`
--

CREATE TABLE `tbl_kategori` (
  `id_kategori` varchar(50) NOT NULL,
  `kategori` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `tbl_kategori`
--

INSERT INTO `tbl_kategori` (`id_kategori`, `kategori`) VALUES
('1', 'Agama'),
('2', 'Akuntansi'),
('5', 'Elektronika'),
('6', 'Farmasi'),
('7', 'Fiction'),
('8', 'Informatika'),
('9', 'Kebidanan'),
('10', 'Kesehatan'),
('4', 'Komputer'),
('11', 'Laporan KKL'),
('12', 'Laporan KP'),
('13', 'Laporan Penelitian Dosen'),
('14', 'Laporan PKM'),
('15', 'Laporan TA/KTI'),
('17', 'Mesin'),
('16', 'Perhotelan'),
('18', 'Prosiding'),
('19', 'Reference'),
('20', 'Teknik'),
('3', 'Umum');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_user`
--

CREATE TABLE `tbl_user` (
  `id_user` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `address` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `tbl_user`
--

INSERT INTO `tbl_user` (`id_user`, `nama`, `username`, `password`, `email`, `address`) VALUES
(1, 'Hadi Kusumanto', 'hadi', '76671d4b83f6e6f953ea2dfb75ded921', 'hadi@gmail.com', 'Brebes'),
(2, 'admin', 'admin', '21232f297a57a5a743894a0e4a801fc3', 'admin@gmail.com', 'Tegal');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tbl_buku`
--
ALTER TABLE `tbl_buku`
  ADD PRIMARY KEY (`id_buku`),
  ADD KEY `kategori` (`kategori`);

--
-- Indeks untuk tabel `tbl_kategori`
--
ALTER TABLE `tbl_kategori`
  ADD PRIMARY KEY (`id_kategori`),
  ADD KEY `kategori` (`kategori`);

--
-- Indeks untuk tabel `tbl_user`
--
ALTER TABLE `tbl_user`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `tbl_buku`
--
ALTER TABLE `tbl_buku`
  MODIFY `id_buku` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=168;

--
-- AUTO_INCREMENT untuk tabel `tbl_user`
--
ALTER TABLE `tbl_user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
