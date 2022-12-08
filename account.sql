CREATE TABLE `account` (
  username text NOT NULL,
  password text NOT NULL,
  dict text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Attendee` (
  `FirstName` text NOT NULL,
  `LastName` text NOT NULL,
  `IDNumber` text NOT NULL,
  `Email` text NOT NULL,
  `CheckedIn` text NOT NULL 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;