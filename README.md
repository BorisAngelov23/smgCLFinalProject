SMG Champions League
The SMG Champions League is a web application that organizes and manages a football tournament between the classes of each grade at Sofia High School of Mathematics. Each class is represented by a Bulgarian letter (А, Б, В, Г, Д, Е), and each grade from 8th to 12th has six classes.

Features
The web application provides the following features:

User Registration: Students can register on the website as team captains. During registration, they provide their first name, last name, phone number, Facebook link, grade, and class. The username is automatically generated based on the provided information.

Team Creation: After registration, team captains can create their football teams. They need to add the names of three players, along with a picture, position, and grade-class. The team captain can create a team for their specific class or join with other classes as per the rules.

Team Matches and Results: The website displays the standings, results, and schedule of matches for each grade and class.

Team of the Week: The website features a "Team of the Week" section, where the best-performing team of the week is highlighted.

Installation
Clone the repository:
bash
Copy code
git clone https://github.com/your-username/smg-champions-league.git
cd smg-champions-league
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Set up the database and run migrations:
bash
Copy code
python manage.py migrate
Create a superuser to access the Django admin:
bash
Copy code
python manage.py createsuperuser
Run the development server:
bash
Copy code
python manage.py runserver
The web application should now be accessible at http://127.0.0.1:8000/.

Usage
Access the website through your browser and register as a team captain using the provided registration form.

After registration, log in with your credentials and navigate to the "Create Team" section to create your football team.

Provide the required information for your team members and create the team.

View the standings, match results, and other information from the homepage.

Log out when you're done.

Contributing
Contributions to the SMG Champions League project are welcome! If you find any issues or have ideas for improvements, feel free to open an issue or submit a pull request.

License
The SMG Champions League project is licensed under the MIT License. You can find the full license text in the LICENSE file.
