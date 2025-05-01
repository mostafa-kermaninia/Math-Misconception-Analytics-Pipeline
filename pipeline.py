from scripts.import_to_db import import_misconceptions, import_questions, import_answers

if __name__ == "__main__":
    try:
        # Import data in order: misconceptions -> questions -> answers
        import_misconceptions()
        import_questions()
        import_answers()
        print("🎉 All data imported successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
