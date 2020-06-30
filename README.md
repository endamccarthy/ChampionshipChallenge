# ChampionshipChallenge

## Enda McCarthy

#### Web Programming with Python and JavaScript

#### August 2019

GAA Fundraiser - Predict results of the Munster and Leinster hurling championships

# Rules
Pick a winner or draw for each game in the Munster and Leinster championship round robin.

Also pick the finalists, the champions and the top scorer from play in both championships.

- Predict a win - 5 points per game
- Predict a draw - 10 points per game
- Predict finalists - 15 points per finalist
- Predict champions - 25 points per champion
- Predict top scorer and amount scored (from play) - 20 points per correct player*

*In case of a tie break, the amount scored will also be taken into account

# Info
This project was created using Django. There are two apps installed, one for the main functionality of the project called 'gameplay' and another to handle the user login/registration called 'users'.

Bootstrap is used for general styling throughout and Django Crispy is used to style forms.

The user account handling is done by the Django Allauth plugin.

Payments are handled using Stripe test mode. To simulate a payment use the following card details:

- 4242 4242 4242 4242
- Any expiry date in the future and any numbers for security and ZIP codes

Sign in to the admin section using the following credentials:

- Email: admin@email.com
- Password: championshipadmin