"""Welcome to Reflex!."""

from mood_app import styles

# Import all the pages.
from mood_app.pages import *

import reflex as rx

# Create the app and compile it.
app = rx.App(style=styles.base_style)
app.compile()
