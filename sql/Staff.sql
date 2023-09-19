-- Insert to general staff table
INSERT INTO `staff` (`staff_id`, `staff_name`, `avatar`, `designation`, `department`, `position`, `email`) VALUES (1, 'Dr. Lim Wei Jie', 'staff_1.png', 'Dean', 'Faculty of Computing And Information Technology', 'Senior Lecturer', 'limwj@tarc.edu.my');

-- Insert to detailed staff table
INSERT INTO `staff_details` (`staff_id`, `publications`, `specialization`, `area_of_interest`) VALUES (1, NULL, 'Management Information Systems', '*Information Security<br>*Networking');
