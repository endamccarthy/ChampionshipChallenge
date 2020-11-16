[![Build Status](https://travis-ci.org/endamccarthy/ChampionshipChallenge.svg?branch=production)](https://travis-ci.org/endamccarthy/ChampionshipChallenge)

Currently a ***work in progress*** (~70% complete)

# Championship Challenge 
Predict results of the Munster and Leinster hurling championships

Currently hosted [here](https://www.championshipchallenge.ie/).

### Developed Using: 
- **Front-End** - HTML / CSS (Bootstrap) / JavaScript
- **Back-End** - Python (Django)
- **Database** - PostgreSQL (on AWS RDS)
- **Host** - Heroku
- **DNS** - Blacknight
- **Static File Hosting** - AWS S3
- **CI/CD** - Github -> TravisCI -> Heroku
- **Editor** - VSCode

---

Regular users will be able to register and enter the competition. Stripe will be used to accept payments. Rules for the competition can be found on the website.

Admin users will have limited access to some CRUD functionality. They will be able to create and update fixtures, results, players, teams, etc.

There will also be a Superuser who will have full access to the Django admin panel. This user will have full Admin user permissions along with the ability to update user accounts among other things.

There are a number of items in the TODO list for this project such as expanding the entry form to include top scorers and provincial finalists. I hope to pick this up again in early 2021 if I have time!
