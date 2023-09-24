-- Find out when the client first enters our system
SELECT enter_count, first_enter_at, block_count FROM ip_addr WHERE `value` = "127.0.0.1";

-- The client enters our system
INSERT INTO ip_addr VALUES ("127.0.0.1", DEFAULT, 1695094650, DEFAULT, DEFAULT);
UPDATE ip_addr SET enter_count = enter_count + 1 WHERE `value` = "127.0.0.1";

-- Block the client
UPDATE ip_addr SET unblock_at = 1695094650, block_count = block_count + 1 WHERE `value` = "127.0.0.1";

-- Reset the client's enter count in the database
UPDATE ip_addr SET enter_count = 1, first_enter_at = 1695094650 WHERE `value` = "127.0.0.1";

-- Get the chatbot session ID of this user
SELECT id FROM chatbot_session WHERE ip_addr = "127.0.0.1";

-- Establish a new chatbot session
INSERT INTO chatbot_session VALUES ("127.0.0.1", "c9a51e4a-6b24-48c7-9154-fba64cdc9342", 1695094650);

-- Renew the chatbot session
UPDATE chatbot_session SET id = "c9a51e4a-6b24-48c7-9154-fba64cdc9342", created_at = 1695094650 WHERE ip_addr = "127.0.0.1";

-- Programme test data
INSERT INTO programme(
	programme_name,
	programme_abbr,
	programme_desc,
	duration,
	intake,
	from_programme_id,
	estimated_local_total_fee,
	estimated_international_total_fee
) VALUES
	(
		"Diploma in Computer Science",
		"DCS",
		"Students are trained in both theoretical knowledge and practical skills for software development, system design and related mathematical techniques.",
		2,
		"June",
		NULL,
		17600,
		33300
	),
	(
		"Diploma in Information Systems",
		"DIS",
		"This programme majors in business information systems. It aims to produce graduates with fundamental knowledge in information technology and its business related applications. It covers the theoretical and practical aspects of developing information systems, management, costing, accounting, electronic commerce, and mathematics. This programme is supported by case studies and computer laboratory assignments. In addition, students are exposed to part of the SAP curriculum like logistics and enterprise resource planning. Students will acquire practical skills in the C Language, HTML5, JavaScript, VB.NET, Microsoft Expression Web, Oracle Database, accounting software packages and be guided through the process of developing an information system.",
		2,
		"June",
		NULL,
		17800,
		33600
	),
	(
		"Diploma in Information Technology",
		"DIT",
		"This programme provides students with a basic understanding of computing techniques and aims to develop the computing and information technology-based knowledge and skills required in modern industrial, commercial and service organisations. It will equip students with essential knowledge of the underlying principles of modern computing technology and enable students to appreciate how modern computers are applied to a range of real world problems. Students will learn C Language, Java, Assembly Language, Oracle Database, HTML5, CSS, PHP and JavaScript. Upon completion, graduates will have acquired knowledge and developed skills in the areas of computer programming, systems analysis, operating systems, computer networking, computer applications and object-oriented software development, as well as in generic business courses.",
		2,
		"June",
		NULL,
		17800,
		33600
	);
