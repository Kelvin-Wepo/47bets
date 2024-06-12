# Project Overview
47bets is  platform allows users to place bets on sports games, manage user accounts, and view game-related information. Staff or superusers can manage games and make updates as needed.

# Installation

To run this project locally, follow these steps:

1. Clone the repository to your local machine:
  
  ``git clone https://github.com/your-username/your-repo.git``

2. Create a virtual environment and activate it:

  ``python -m venv venv``
  source venv/bin/activate # On Windows, use venv\Scripts\activate

3. Install the required dependencies:
  
  ``pip install -r requirements.txt``

4. Configure your database settings in `settings.py`.

5. Apply database migrations:

  ``python manage.py migrate``

6. Start the development server:

  ``python manage.py runserver``

7. Access the application in your web browser at `http://localhost:8000/`.

# Usage

1. **Registration**:
- Visit the registration page and fill out the registration form.
- An activation link will be sent to your email for account confirmation.

2. **Login**:
- After confirming your account, log in with your credentials.

3. **Betting**:
- View upcoming games on the home page.
- Place bets on your chosen team with a specified bet amount.
- Manage your bets on the "Bets" page.

4. **Profile**:
- View your profile to see your betting history and current bets.

# Configuration

- Email settings can be configured in `settings.py` to enable account activation emails.
- Ensure that your email service provider settings are correctly configured.

# API Endpoints

The application provides the following API endpoints for external access:

- `/teams/`: Get a list of all sports teams.
- `/players/`: Get a list of all players.
- `/games/`: Get a list of all games.
- `/api/bets/`: API for managing user bets.

# Contributing

Contributions to this project are welcome. To contribute:

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Test your changes thoroughly.
5. Commit your changes and push them to your forked repository.
6. Open a pull request to the main repository.

# License

This project is licensed under the [Kelvin Wepo](LICENSE) - (e.g., MIT) License. See the [LICENSE](LICENSE) file for details.
