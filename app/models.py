"""
Data models and database classes for RTO AI Enrollment System
"""
from datetime import datetime
from enum import Enum


class StudentStatus(Enum):
    INQUIRY = "inquiry"
    FOLLOW_UP_1 = "follow_up_1"
    FOLLOW_UP_2 = "follow_up_2"
    QUALIFIED = "qualified"
    ENROLLED = "enrolled"
    REJECTED = "rejected"


class StudentRecord:
    """Represents a student record"""

    def __init__(self, name, email, phone, program, status=StudentStatus.INQUIRY):
        self.id = self._generate_id()
        self.name = name
        self.email = email
        self.phone = phone
        self.program = program
        self.status = status
        self.created_at = datetime.now()
        self.last_contact = datetime.now()
        self.conversation_history = []
        self.qualification_score = 0
        self.notes = []

    def _generate_id(self):
        return f"STU_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "program": self.program,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "last_contact": self.last_contact.isoformat(),
            "qualification_score": self.qualification_score,
            "notes": self.notes
        }


class StudentDatabase:
    """In-memory database for student records"""

    def __init__(self):
        self.students = {}

    def add_student(self, student):
        self.students[student.id] = student
        return student.id

    def get_student(self, student_id):
        return self.students.get(student_id)

    def update_student(self, student_id, **kwargs):
        if student_id in self.students:
            student = self.students[student_id]
            for key, value in kwargs.items():
                if hasattr(student, key):
                    setattr(student, key, value)
            student.last_contact = datetime.now()

    def get_students_by_status(self, status):
        return [s for s in self.students.values() if s.status == status]

    def get_followup_candidates(self):
        now = datetime.now()
        candidates = []
        for student in self.students.values():
            days_since_contact = (now - student.last_contact).days
            if student.status == StudentStatus.INQUIRY and days_since_contact >= 3:
                candidates.append(student)
            elif student.status == StudentStatus.FOLLOW_UP_1 and days_since_contact >= 5:
                candidates.append(student)
        return candidates

    def list_all(self):
        return list(self.students.values())

