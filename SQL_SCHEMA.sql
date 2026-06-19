CREATE TABLE Student (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100),
    email VARCHAR(100),
    interests TEXT,
    skills TEXT
);

CREATE TABLE Career_Path (
    career_id INT PRIMARY KEY AUTO_INCREMENT,
    career_name VARCHAR(100),
    required_skills TEXT
);

CREATE TABLE Career_Assessment (
    assessment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    recommended_career INT,
    FOREIGN KEY(student_id) REFERENCES Student(student_id),
    FOREIGN KEY(recommended_career) REFERENCES Career_Path(career_id)
);
