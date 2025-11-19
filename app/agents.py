"""
AI agent classes for RTO AI Enrollment System
"""
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from .models import StudentDatabase, StudentRecord, StudentStatus

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class EnrollmentAgent:
    """
    Autonomous AI agent for student enrollment, qualification, and follow-ups
    Uses Groq as the underlying intelligence
    """

    def __init__(self, db):
        self.db = db
        self.conversation_history = []
        self.model = "llama-3.3-70b-versatile"

        self.system_prompt = """You are an expert RTO (Registered Training Organization) enrollment agent. Your role is to:

1. QUALIFY STUDENTS: Ask relevant questions about their background, career goals, and learning preferences
2. RECOMMEND PROGRAMS: Based on their profile, suggest appropriate training programs
3. HANDLE OBJECTIONS: Address concerns about cost, time commitment, prerequisites, etc.
4. CLOSE ENROLLMENT: Guide qualified students to enrollment
5. FOLLOW-UP: For non-qualified leads, schedule follow-ups and maintain engagement

RULES:
- Be conversational and friendly
- Ask one question at a time
- Qualify based on: motivation, learning capacity, program fit, availability
- Score qualification 0-100 based on responses
- For high scorers (>70), move toward enrollment
- For medium scorers (40-70), recommend programs and schedule follow-up
- For low scorers (<40), thank them and offer future opportunities
- Keep responses concise (2-3 sentences max)
- Always end with a question or call-to-action

PROGRAMS OFFERED:
- Arts, Humanities & Social Sciences
- Aviation
- Business
- Engineering
- Design, ICT, Health, Science, Psychology, etc.

PRICING:
- Arts, Humanities & Social Sciences: $4,000-$6,000
- Aviation: $8,000-$12,000
- Business: $5,000-$8,000
- Engineering: $10,000-$15,000
- Design, ICT, Health, Science, Psychology: $6,000-$10,000
- Payment plans available

When you make a decision about qualification or recommend action, explicitly state it like:
[QUALIFICATION_SCORE: XX]
[RECOMMENDATION: enroll/follow_up/not_interested]
[ACTION: program_recommendation/objection_handling/enrollment_process]"""

    def chat(self, user_message, context=None):
        """
        Send a message and get an agent response
        context: Optional context about the student
        """
        # Build messages array
        messages = self.conversation_history.copy()

        # Add context if provided
        if context:
            context_msg = f"[STUDENT CONTEXT]\nName: {context.get('name')}\nProgram Interest: {context.get('program')}\nStatus: {context.get('status')}\nPrevious Notes: {context.get('notes')}\n\n"
            if messages:
                # Add context to first user message
                messages[0] = {"role": "user", "content": context_msg + messages[0]["content"]}
            else:
                messages.append({"role": "user", "content": context_msg + user_message})

        messages.append({"role": "user", "content": user_message})

        # Call Groq API
        response = client.chat.completions.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "system", "content": self.system_prompt}] + messages
        )

        assistant_message = response.choices[0].message.content

        # Store in conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        # Parse structured data from response
        parsed = self._parse_response(assistant_message)

        return {
            "message": assistant_message,
            "qualification_score": parsed.get("score"),
            "recommendation": parsed.get("recommendation"),
            "action": parsed.get("action")
        }

    def _parse_response(self, response):
        """Extract structured data from agent response"""
        score = None
        recommendation = None
        action = None

        # Extract qualification score
        score_match = re.search(r'\[QUALIFICATION_SCORE:\s*(\d+)\]', response)
        if score_match:
            score = int(score_match.group(1))

        # Extract recommendation
        rec_match = re.search(r'\[RECOMMENDATION:\s*(\w+)\]', response)
        if rec_match:
            recommendation = rec_match.group(1)

        # Extract action
        action_match = re.search(r'\[ACTION:\s*([\w_]+)\]', response)
        if action_match:
            action = action_match.group(1)

        return {
            "score": score,
            "recommendation": recommendation,
            "action": action
        }

    def reset_conversation(self):
        """Reset conversation history for new student"""
        self.conversation_history = []


class EnrollmentManager:
    """Orchestrates the entire enrollment process"""

    def __init__(self):
        self.db = StudentDatabase()
        self.agent = EnrollmentAgent(self.db)

    def new_inquiry(self, name, email, phone, program_interest):
        """Create new student inquiry"""
        student = StudentRecord(name, email, phone, program_interest)
        student_id = self.db.add_student(student)

        # Start conversation
        self.agent.reset_conversation()
        initial_message = f"Hi {name}! Thanks for your interest in our {program_interest} program. I'd love to learn more about you. What's your main career goal?"

        student.conversation_history.append({"role": "assistant", "content": initial_message})

        return student_id, initial_message

    def process_response(self, student_id, user_message):
        """Process student response"""
        student = self.db.get_student(student_id)
        if not student:
            return {"error": "Student not found"}

        # Get context for agent
        context = {
            "name": student.name,
            "program": student.program,
            "status": student.status.value,
            "notes": student.notes[-5:] if student.notes else []  # Last 5 notes
        }

        # Get agent response
        response = self.agent.chat(user_message, context)

        # Store conversation
        student.conversation_history.append({"role": "user", "content": user_message})
        student.conversation_history.append({"role": "assistant", "content": response["message"]})

        # Update student based on agent decision
        if response["qualification_score"]:
            student.qualification_score = response["qualification_score"]

        if response["recommendation"] == "enroll":
            student.status = StudentStatus.QUALIFIED
            student.notes.append(f"[{datetime.now().isoformat()}] Qualified for enrollment")
        elif response["recommendation"] == "follow_up":
            if student.status == StudentStatus.INQUIRY:
                student.status = StudentStatus.FOLLOW_UP_1
            else:
                student.status = StudentStatus.FOLLOW_UP_2
            student.notes.append(f"[{datetime.now().isoformat()}] Follow-up scheduled")
        elif response["recommendation"] == "not_interested":
            student.status = StudentStatus.REJECTED
            student.notes.append(f"[{datetime.now().isoformat()}] Student marked as not interested")

        self.db.update_student(student_id, status=student.status, qualification_score=student.qualification_score)

        return response

    def generate_followup_message(self, student_id):
        """Generate AI-powered follow-up message"""
        student = self.db.get_student(student_id)
        if not student:
            return {"error": "Student not found"}

        self.agent.reset_conversation()

        # Create follow-up context
        days_passed = (datetime.now() - student.last_contact).days
        followup_prompt = f"Generate a friendly follow-up message for {student.name} who inquired about {student.program} {days_passed} days ago. They haven't responded yet. Keep it short and personalized."

        response = self.agent.chat(followup_prompt, {
            "name": student.name,
            "program": student.program,
            "status": student.status.value,
            "notes": student.notes
        })

        return {
            "followup_message": response["message"],
            "recommended_channel": self._pick_channel(student)
        }

    def _pick_channel(self, student):
        """Recommend best communication channel"""
        # Simple heuristic - can be enhanced with ML
        if "@" in student.email:
            return "email"
        elif student.phone:
            return "sms"
        return "whatsapp"

    def get_dashboard(self):
        """Get enrollment dashboard metrics"""
        all_students = self.db.list_all()

        return {
            "total_inquiries": len(all_students),
            "by_status": {
                "inquiry": len(self.db.get_students_by_status(StudentStatus.INQUIRY)),
                "follow_up_1": len(self.db.get_students_by_status(StudentStatus.FOLLOW_UP_1)),
                "follow_up_2": len(self.db.get_students_by_status(StudentStatus.FOLLOW_UP_2)),
                "qualified": len(self.db.get_students_by_status(StudentStatus.QUALIFIED)),
                "enrolled": len(self.db.get_students_by_status(StudentStatus.ENROLLED)),
                "rejected": len(self.db.get_students_by_status(StudentStatus.REJECTED))
            },
            "avg_qualification_score": sum(s.qualification_score for s in all_students) / len(all_students) if all_students else 0,
            "followup_due": len(self.db.get_followup_candidates()),
            "conversion_rate": len(self.db.get_students_by_status(StudentStatus.ENROLLED)) / len(all_students) * 100 if all_students else 0
        }

    def export_students(self):
        """Export all students as JSON"""
        students = self.db.list_all()
        return {
            "export_date": datetime.now().isoformat(),
            "total_records": len(students),
            "students": [s.to_dict() for s in students]
        }
