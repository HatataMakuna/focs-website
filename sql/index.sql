-- Find out when the client first enters our system
SELECT enter_count, first_enter_at, block_count FROM ip_addr WHERE `value` = "127.0.0.1";

-- The client enters our system
INSERT INTO ip_addr VALUES ("127.0.0.1", DEFAULT, 1695094650, DEFAULT, DEFAULT);
UPDATE ip_addr SET enter_count = enter_count + 1 WHERE `value` = "127.0.0.1";

-- Block the client
UPDATE ip_addr SET unblock_at = 1695094650, block_count = block_count + 1 WHERE `value` = "127.0.0.1";

-- Reset the client's enter count in the database
UPDATE ip_addr SET enter_count = 1, first_enter_at = 1695094650 WHERE `value` = "127.0.0.1";
