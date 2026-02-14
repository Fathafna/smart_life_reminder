
smart_life_reminder
Basic Details
Team Name: Bug hunters
Team Members
Member 1: Fathima Afna Z.M - LBS college of engineering kasaragod
Member 2: Ayshath Amra K.A - LBS college of engineering kasaragod
Hosted Project Link
[https://smart-life-reminder.vercel.app/login]


Project Description :
Smart Life Reminder is a web-based system that helps users manage important tasks and deadlines through timely in-website popup reminders and daily check-ins. It is designed to be simple and elder-friendly, ensuring that bills, registrations, and other critical tasks are never forgotten.

The Problem statement
People often forget important tasks such as bill payments, registrations, and renewals due to busy schedules or memory issues. This problem is especially challenging for elderly users, leading to missed deadlines, penalties, and unnecessary stress.

The Solution
Smart Life Reminder is a user-friendly web application that allows users to add important tasks and receive timely in-website popup reminders and daily check-ins. By providing clear alerts and an elder-friendly interface, the system ensures critical tasks are completed on time without confusion.

Technical Details
Technologies/Components Used
For Software:

Languages used: Python,JavaScript,HTML,CSS
Frameworks used: Flask (Python web framework
Libraries used:Flask-SQLAlchemy (database ORM)
Werkzeug (security utilities – session handling)
JavaScript Fetch API 
Tools used: Visual Studio Code
Git & GitHub 

Implementation
For Software:
Installation
[Installation commands -pip install -r requirements.txt]
Run
[ python app.py]



Circuit Setup
[Explain how to set up the circuit]

Project Documentation
For Software:
Screenshots (Add at least 3)
![<img width="1920" height="1080" alt="Screenshot (53)" src="https://github.com/user-attachments/assets/912eee49-f59d-4f15-81d8-b4ceb9238849" />
][login page]-user login to use website

!<img width="1920" height="1080" alt="Screenshot (55)" src="https://github.com/user-attachments/assets/c7459aff-1ddd-481f-927c-e080bd751d91" />
[](Add task) entering the details of task that will reminder before deadline

[<img width="1920" height="1080" alt="Screenshot (57)" src="https://github.com/user-attachments/assets/1ac308c4-c825-41e8-9f33-fdafcbab3084" />
[ task added and popup reminder]
]

Diagrams
System Architecture:![WhatsApp Image 2026-02-14 at 8 20 52 AM](https://github.com/user-attachments/assets/32982f3a-791a-4a3c-a297-ae207b9839ab)


Architecture Diagram Explain your system architecture - components, data flow, tech stack interaction

Application Workflow:

Workflow Add caption explaining your workflow


For Web Projects with Backend:
API Documentation
Base URL: https://api.yourproject.com

Endpoints
GET /api/endpoint

Description: [What it does]
Parameters:
param1 (string): [Description]
param2 (integer): [Description]
Response:
{
  "status": "success",
  "data": {}
}
POST /api/endpoint

Description: [What it does]
Request Body:
{
  "field1": "value1",
  "field2": "value2"
}
Response:
{
  "status": "success",
  "message": "Operation completed"
}
[Add more endpoints as needed...]

For Mobile Apps:
App Flow Diagram
App Flow Explain the user flow through your application

Installation Guide
For Android (APK):

Download the APK from [Release Link]
Enable "Install from Unknown Sources" in your device settings:
Go to Settings > Security
Enable "Unknown Sources"
Open the downloaded APK file
Follow the installation prompts
Open the app and enjoy!
For iOS (IPA) - TestFlight:

Download TestFlight from the App Store
Open this TestFlight link: [Your TestFlight Link]
Click "Install" or "Accept"
Wait for the app to install
Open the app from your home screen
Building from Source:

# For Android
flutter build apk
# or
./gradlew assembleDebug

# For iOS
flutter build ios
# or
xcodebuild -workspace App.xcworkspace -scheme App -configuration Debug
For Hardware Projects:
Bill of Materials (BOM)
Component	Quantity	Specifications	Price	Link/Source
Arduino Uno	1	ATmega328P, 16MHz	₹450	[Link]
LED	5	Red, 5mm, 20mA	₹5 each	[Link]
Resistor	5	220Ω, 1/4W	₹1 each	[Link]
Breadboard	1	830 points	₹100	[Link]
Jumper Wires	20	Male-to-Male	₹50	[Link]
[Add more...]				
Total Estimated Cost: ₹[Amount]

Assembly Instructions
Step 1: Prepare Components

Gather all components listed in the BOM
Check component specifications
Prepare your workspace Step 1 Caption: All components laid out
Step 2: Build the Power Supply

Connect the power rails on the breadboard
Connect Arduino 5V to breadboard positive rail
Connect Arduino GND to breadboard negative rail Step 2 Caption: Power connections completed
Step 3: Add Components

Place LEDs on breadboard
Connect resistors in series with LEDs
Connect LED cathodes to GND
Connect LED anodes to Arduino digital pins (2-6) Step 3 Caption: LED circuit assembled
Step 4: [Continue for all steps...]

Final Assembly: Final Build Caption: Completed project ready for testing

For Scripts/CLI Tools:
Command Reference
Basic Usage:

python script.py [options] [arguments]
Available Commands:

command1 [args] - Description of what command1 does
command2 [args] - Description of what command2 does
command3 [args] - Description of what command3 does
Options:

-h, --help - Show help message and exit
-v, --verbose - Enable verbose output
-o, --output FILE - Specify output file path
-c, --config FILE - Specify configuration file
--version - Show version information
Examples:

# Example 1: Basic usage
python script.py input.txt

# Example 2: With verbose output
python script.py -v input.txt

# Example 3: Specify output file
python script.py -o output.txt input.txt

# Example 4: Using configuration
python script.py -c config.json --verbose input.txt
Demo Output
Example 1: Basic Processing

Input:

This is a sample input file
with multiple lines of text
for demonstration purposes
Command:

python script.py sample.txt
Output:

Processing: sample.txt
Lines processed: 3
Characters counted: 86
Status: Success
Output saved to: output.txt
Example 2: Advanced Usage

Input:

{
  "name": "test",
  "value": 123
}
Command:

python script.py -v --format json data.json
Output:

[VERBOSE] Loading configuration...
[VERBOSE] Parsing JSON input...
[VERBOSE] Processing data...
{
  "status": "success",
  "processed": true,
  "result": {
    "name": "test",
    "value": 123,
    "timestamp": "2024-02-07T10:30:00"
  }
}
[VERBOSE] Operation completed in 0.23s
Project Demo
Video 
https://drive.google.com/file/d/19BUnNvxzw4IjCZm66ADo6SFiKrwAp2Hv/view?usp=sharing

Explain what the video demonstrates - key features, user flow, technical highlights

Additional Demos
[Add any extra demo materials/links - Live site, APK download, online demo, etc.]

AI Tools Used (Optional - For Transparency Bonus)
If you used AI tools during development, document them here for transparency:

Tool Used: [e.g., GitHub Copilot, v0.dev, Cursor, ChatGPT, Claude]

Purpose: [What you used it for]

Example: "Generated boilerplate React components"
Example: "Debugging assistance for async functions"
Example: "Code review and optimization suggestions"
Key Prompts Used:

"Create a REST API endpoint for user authentication"
"Debug this async function that's causing race conditions"
"Optimize this database query for better performance"
Percentage of AI-generated code: [Approximately X%]

Human Contributions:

Architecture design and planning
Custom business logic implementation
Integration and testing
UI/UX design decisions
Note: Proper documentation of AI usage demonstrates transparency and earns bonus points in evaluation!

Team Contributions
[Name 1]: [Specific contributions - e.g., Frontend development, API integration, etc.]
[Name 2]: [Specific contributions - e.g., Backend development, Database design, etc.]
[Name 3]: [Specific contributions - e.g., UI/UX design, Testing, Documentation, etc.]
License
This project is licensed under the [LICENSE_NAME] License - see the LICENSE file for details.

Common License Options:

MIT License (Permissive, widely used)
Apache 2.0 (Permissive with patent grant)
GPL v3 (Copyleft, requires derivative works to be open sou
