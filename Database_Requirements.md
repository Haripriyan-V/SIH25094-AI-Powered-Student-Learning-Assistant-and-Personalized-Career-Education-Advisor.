# Database Requirements

## Student Table
- student_id (PK)
- full_name
- email
- phone
- password
- education_level
- current_course
- interests
- skills
- location

## Career Assessment Table
- assessment_id (PK)
- student_id (FK)
- aptitude_score
- personality_type
- recommended_career

## Career Path Table
- career_id (PK)
- career_name
- description
- required_skills
- salary_range

## Course Table
- course_id (PK)
- course_name
- provider
- duration

## College Table
- college_id (PK)
- college_name
- location
- ranking

## Scholarship Table
- scholarship_id (PK)
- scholarship_name
- amount
- deadline
