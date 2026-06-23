"""
RTH AI Enrollment System - CLI Interface
Command-line interface for the enrollment system
"""

from app import EnrollmentManager, VoiceOutputHandler

# ============================================================================
# TEXT INPUT FUNCTIONS
# ============================================================================

def get_text_input(prompt_text, voice_output):
    """Get input via text with spoken prompt"""
    voice_output.speak(prompt_text)
    print(f"\n{prompt_text}")
    return input().strip()

def get_text_menu_choice(voice_output):
    """Get menu choice via text input"""
    menu_text = "Please enter the number of your choice. 1 for new inquiry, 2 for continue conversation, 3 for follow up, 4 for dashboard, 5 for export, or 6 to exit."
    voice_output.speak(menu_text)
    print(f"\n{menu_text}")

    while True:
        choice = input("\nSelect option (1-6): ").strip()
        if choice in ['1', '2', '3', '4', '5', '6']:
            print(f"Selected: {choice}")
            return choice
        print("❌ Invalid choice. Please enter 1-6.")

# ============================================================================
# MAIN CLI INTERFACE
# ============================================================================

def main():
    """Text input with voice output enrollment management"""
    manager = EnrollmentManager()
    voice_output = VoiceOutputHandler()
    
    print("\n" + "="*60)
    print("RTH AI ENROLLMENT & MARKETING SYSTEM")
    print("VOICE OUTPUT + TEXT INPUT INTERFACE")
    print("="*60 + "\n")

    # Welcome message
    welcome_msg = "Welcome to the RTH HETR AI Enrollment System. You can type your responses and I will speak my replies. Let's get started!"
    voice_output.speak(welcome_msg)
    print(f"\n{welcome_msg}\n")
    
    while True:
        # Text menu
        print("\n" + "-"*60)
        print("MENU:")
        print("1. New Student Inquiry")
        print("2. Continue Student Conversation")
        print("3. Generate Follow-up Message")
        print("4. View Dashboard")
        print("5. Export Student Records")
        print("6. Exit")
        print("-"*60)
        
        choice = get_text_menu_choice(voice_output)
        
        if choice == "1":
            # New Student Inquiry - text input with voice output
            name = get_text_input("Please enter the student's name:", voice_output)
            if not name:
                continue

            email = get_text_input("Please enter the student's email address:", voice_output)
            if not email:
                continue

            phone = get_text_input("Please enter the student's phone number:", voice_output)
            if not phone:
                continue

            program = get_text_input("Please enter the program of interest:", voice_output)
            if not program:
                continue
            
            student_id, message = manager.new_inquiry(name, email, phone, program)
            print(f"\n[AGENT] {message}")
            print(f"[Student ID: {student_id}]")
            
            # Speak the agent's greeting
            voice_output.speak(message)

        elif choice == "2":
            # Continue Student Conversation - text input with voice output
            student_id = get_text_input("Please enter the student ID:", voice_output)
            if not student_id:
                continue

            student = manager.db.get_student(student_id)
            if not student:
                error_msg = "Student not found. Please try again."
                voice_output.speak(error_msg)
                print(f"❌ {error_msg}")
                continue
            
            # Start text conversation loop
            voice_output.speak(f"Starting conversation with {student.name}. You can type your messages now.")
            print(f"\n💬 Text conversation with {student.name}")
            print("Type 'exit' or 'quit' to end the conversation\n")

            conversation_active = True
            while conversation_active:
                user_input = get_text_input("Please type your message:", voice_output)

                if not user_input:
                    continue

                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'stop', 'end', 'done']:
                    goodbye_msg = "Ending conversation. Thank you!"
                    voice_output.speak(goodbye_msg)
                    print(f"\n👋 {goodbye_msg}")
                    conversation_active = False
                    break

                # Process response
            response = manager.process_response(student_id, user_input)
            
            if "error" not in response:
                print(f"\n[AGENT] {response['message']}")

                # Always speak the agent's response
                voice_output.speak(response['message'])

                if response.get("qualification_score"):
                    score_msg = f"Qualification score: {response['qualification_score']} out of 100"
                    print(f"[Qualification Score: {response['qualification_score']}/100]")
                    voice_output.speak(score_msg)

                if response.get("recommendation"):
                    print(f"[Recommendation: {response['recommendation']}]")
                else:
                    error_msg = response.get('error', 'Unknown error occurred')
                    print(f"❌ {error_msg}")
                    voice_output.speak(f"Error: {error_msg}")
        
        elif choice == "3":
            # Generate Follow-up Message
            student_id = get_text_input("Please enter the student ID for follow-up:", voice_output)
            if not student_id:
                continue

            followup = manager.generate_followup_message(student_id)
            
            if "error" not in followup:
                print(f"\n[SUGGESTED FOLLOW-UP MESSAGE]")
                print(f"{followup['followup_message']}")
                print(f"[Recommended Channel: {followup['recommended_channel']}]")

                # Speak the follow-up message
                followup_voice_msg = f"Follow-up message: {followup['followup_message']}. Recommended channel: {followup['recommended_channel']}"
                voice_output.speak(followup_voice_msg)
            else:
                error_msg = followup.get("error", "Unknown error")
                print(f"❌ {error_msg}")
                voice_output.speak(f"Error: {error_msg}")
        
        elif choice == "4":
            # View Dashboard
            dashboard = manager.get_dashboard()
            print("\n[ENROLLMENT DASHBOARD]")
            print(f"Total Inquiries: {dashboard['total_inquiries']}")
            print(f"Qualified: {dashboard['by_status']['qualified']}")
            print(f"Enrolled: {dashboard['by_status']['enrolled']}")
            print(f"Conversion Rate: {dashboard['conversion_rate']:.1f}%")

            # Speak key metrics
            dashboard_msg = f"Total inquiries: {dashboard['total_inquiries']}. Qualified: {dashboard['by_status']['qualified']}. Enrolled: {dashboard['by_status']['enrolled']}. Conversion rate: {dashboard['conversion_rate']:.1f} percent."
            voice_output.speak(dashboard_msg)
        
        elif choice == "5":
            # Export Student Records
            export = manager.export_students()
            print("\n[STUDENT EXPORT]")
            print(f"Total Records: {export['total_records']}")
            
            # Also save to file
            with open("students_export.json", "w") as f:
                import json
                json.dump(export, f, indent=2)

            success_msg = f"Exported {export['total_records']} student records. Saved to students_export.json"
            print(f"✅ {success_msg}")
            voice_output.speak(success_msg)
        
        elif choice == "6":
            goodbye_msg = "Thank you for using the RTO AI Enrollment System. Goodbye!"
            voice_output.speak(goodbye_msg)
            print(f"\n👋 {goodbye_msg}")
            break
        
        else:
            error_msg = "Invalid option. Please try again."
            voice_output.speak(error_msg)
            print(f"❌ {error_msg}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Run CLI interface
        main()
    else:
        # Run web server (default) - always on port 5008
        from app import run_web_server
        run_web_server()