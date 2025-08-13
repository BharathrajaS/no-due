-- Create sample subjects for CSE department
INSERT OR IGNORE INTO subject (name, department, semester) VALUES
('Mathematics I', 'CSE', 1),
('Physics', 'CSE', 1),
('Chemistry', 'CSE', 1),
('Programming Fundamentals', 'CSE', 1),
('English Communication', 'CSE', 1),
('Data Structures', 'CSE', 2),
('Computer Organization', 'CSE', 2),
('Discrete Mathematics', 'CSE', 2),
('Object Oriented Programming', 'CSE', 2),
('Environmental Science', 'CSE', 2);

-- Create sample HOD user
INSERT OR IGNORE INTO user (name, email, password, role, department, class_section) VALUES
('Dr. John Smith', 'hod@college.edu', 'scrypt:32768:8:1$salt$hash', 'hod', 'CSE', 'A');

-- Create sample staff users
INSERT OR IGNORE INTO user (name, email, password, role, department, class_section) VALUES
('Prof. Alice Johnson', 'alice@college.edu', 'scrypt:32768:8:1$salt$hash', 'staff', 'CSE', 'A'),
('Prof. Bob Wilson', 'bob@college.edu', 'scrypt:32768:8:1$salt$hash', 'staff', 'CSE', 'B'),
('Prof. Carol Davis', 'carol@college.edu', 'scrypt:32768:8:1$salt$hash', 'staff', 'CSE', 'A');

-- Create sample student users
INSERT OR IGNORE INTO user (name, email, password, role, department, class_section, year, semester, roll_number) VALUES
('Student One', 'student1@college.edu', 'scrypt:32768:8:1$salt$hash', 'student', 'CSE', 'A', 1, 1, 'CSE001'),
('Student Two', 'student2@college.edu', 'scrypt:32768:8:1$salt$hash', 'student', 'CSE', 'A', 1, 1, 'CSE002'),
('Student Three', 'student3@college.edu', 'scrypt:32768:8:1$salt$hash', 'student', 'CSE', 'B', 1, 1, 'CSE003'),
('Student Four', 'student4@college.edu', 'scrypt:32768:8:1$salt$hash', 'student', 'CSE', 'B', 1, 1, 'CSE004');
