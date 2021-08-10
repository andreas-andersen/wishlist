# Wishlist.app
#### A django app for creating gift exchange groups and wish list assignments
[Heroku deployment](https://stormy-harbor-20992.herokuapp.com/)

The app has the following features:
* General user interface (sign-up, login, etc.)
* Interface for user-based management of groups
* Interface for creating wish lists
* Interface for choosing wish list assignment method and distributing wish lists among group memebers (both manual and random)
* Rudimentary notification system

## Dependencies:
Wishlist.app uses following packages:
* `django`
* `environs`
* `gunicorn`
* `numpy` (for random assignment algorithms)
* `psycopg2`
* `environs`
* `reportlab` and `xhtml2pdf` (for generating basic wish list print-outs)
* `six` (for generating user activation tokens)
* `whitenoise`

## Reflections and improvement potential:
This is my first django project. I had only had experience following the excellenet tutorials provided by the ["Django for..."](http://wsvincent.com/books/) books by William S. Vincent. The requirements for the project also grew organically, and there is thus a distinct feeling of "progression" in my coding style from what I wrote at the beginning compared to the end.

For example, I was trying to do everything within the class-based view system. This would inevitably prove too complex for pages containing two forms, complex POST functionalities etc and I opted for creating my own function based views. (This is a technique that would have saved a tremendous amount of pain had I learned earlier). I would also have opted for a Sass approach to styling (my css looks very messy at this point), and have a more structured approach to the naming of models, views, templates etc. The admin section could also do with some improvements.

In terms of additional features, these come to mind:
* Internationalization / Localization.
* Implementation of a mobile version

But this will probably be in a different project.

### Other Acknowledgements:
* Icons by [flaticon](https://www.flaticon.com/uicons)

## Screenshots:
![Screenshot1](screenshot.png?raw=true "Screenshot 1")
![Screenshot2](screenshot2.png?raw=true "Screenshot 2")
![Screenshot3](screenshot3.png?raw=true "Screenshot 3")