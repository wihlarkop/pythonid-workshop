"""
Simple Meeting Notes Summarizer using Google Gemini AI
Workshop Version - Easy to understand and use
"""

import os
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv


def setup_gemini_api():
    """Setup Gemini API with API key from environment or user input"""
    load_dotenv()

    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        print("⚠️  No Gemini API key found in .env file")
        print("\n📝 Get your free API key from:")
        print("   https://makersuite.google.com/app/apikey")
        print("\nThen create a .env file with:")
        print("   GEMINI_API_KEY=your_key_here\n")

        api_key = input("Enter your Gemini API key (or press Enter to exit): ").strip()
        if not api_key:
            print("❌ No API key provided. Exiting...")
            exit()

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini API configured successfully\n")
        return model
    except Exception as e:
        print(f"❌ Error setting up Gemini: {e}")
        exit()


def load_meeting_notes(file_path="data/meeting_notes.txt"):
    """Load meeting notes from text file"""
    try:
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            print("📝 Please create a file with your meeting notes at:")
            print(f"   {file_path.absolute()}")
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if not content:
            print("❌ Meeting notes file is empty")
            return None

        print(f"📄 Loaded meeting notes: {len(content)} characters")
        return content

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None


def generate_summary(model, meeting_text):
    """Generate meeting summary using Gemini"""
    prompt = f"""
    Please analyze these meeting notes and create a summary with:

    1. Key Decisions (what was decided)
    2. Action Items (who needs to do what by when)
    3. Important Topics (main discussion points)
    4. Next Steps (what happens next)

    Meeting Notes:
    {meeting_text}

    Please provide a clear, bullet-point summary:
    """

    try:
        print("🤖 Generating AI summary...")
        response = model.generate_content(prompt)

        if response.text:
            print("✅ Summary generated successfully!\n")
            return response.text
        else:
            print("❌ No response from Gemini")
            return None

    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return None


def save_summary(summary, output_file="output/meeting_summary.md"):
    """Save the summary to a markdown file"""
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# AI Meeting Summary\n\n")
            f.write(summary)
            f.write("\n\n---\n*Generated using Google Gemini AI*")

        print(f"💾 Summary saved to: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Error saving summary: {e}")
        return False


def display_summary(summary):
    """Display the summary in the console"""
    print("=" * 60)
    print("📝 MEETING SUMMARY")
    print("=" * 60)
    print(summary)
    print("=" * 60)


def main():
    """Main function - runs the complete summarization process"""
    print("\n🚀 Meeting Notes AI Summarizer")
    print("=" * 60)

    # Step 1: Setup Gemini API
    model = setup_gemini_api()

    # Step 2: Load meeting notes
    meeting_text = load_meeting_notes()
    if not meeting_text:
        return

    # Step 3: Generate summary
    summary = generate_summary(model, meeting_text)
    if not summary:
        return

    # Step 4: Display summary
    display_summary(summary)

    # Step 5: Save summary
    save_summary(summary)

    print("\n✨ Done! Your meeting has been summarized.")


if __name__ == "__main__":
    main()