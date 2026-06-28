# Entity Relationship Diagram

```text

+-----------+
|  STUDENT  |
+-----------+
| Student_ID|
| Name      |
| Email     |
| Password  |
+-----------+
      |
      | Takes
      |
      v
+----------------------+
| CAREER_ASSESSMENT    |
+----------------------+
| Assessment_ID        |
| Student_ID (FK)      |
| Score                |
| Recommendation       |
+----------------------+
      |
      | Recommends
      |
      v
+---------------+
| CAREER_PATH   |
+---------------+
| Career_ID     |
| Career_Name   |
| Description   |
+---------------+
      |
      | Contains
      |
      v
+-----------+            Offered By          +-----------+
|  COURSE   |<------------------------------>|  COLLEGE  |
+-----------+                                +-----------+
| Course_ID |                                | College_ID|
| Name      |                                | Name      |
| Duration  |                                | Location  |
+-----------+                                +-----------+

+-----------+           Applies For          +---------------+
|  STUDENT  |------------------------------->| SCHOLARSHIP   |
+-----------+                                +---------------+
                                              | Scholarship_ID|
                                              | Name          |
                                              | Eligibility   |
                                              +---------------+

+-----------+            Has                 +----------------+
|  STUDENT  |------------------------------->| CHAT_HISTORY   |
+-----------+                                +----------------+
                                              | Chat_ID        |
                                              | Question       |
                                              | Response       |
                                              +----------------+
```
