"""The home page of the app."""

from mood_app import styles
from mood_app.templates import template

import reflex as rx
from ..state import State

from convex import ConvexClient, ConvexError

client = ConvexClient("https://elegant-fox-172.convex.cloud")

# def add_item(self, form_data: dict[str, str]):
#     """Add a new item to the todo list.r
#
#     Args:
#         form_data: The data from the form.
#     """
#     # Add the new item to the list.
#     new_item = form_data.pop("new_item")
#     if not new_item:
#         self.invalid_item = True
#         return
#
#     self.items.append(new_item)
#     # set the invalid status to False.
#     self.invalid_item = False
#     # Clear the value of the input.
#     return rx.set_value("new_item", "")

class ChatState(State):

    answer = ""

    def process_data(self):
        # call convex here answer
        # save to database
        try:
            client.mutation("posts:add", {"body":self.answer})
        except ConvexError as err:
            print(err.data)
        return rx.redirect("/dashboard")


def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Tell me your thoughts", on_blur=ChatState.set_answer, text_align ="center", style=styles.answer_style),
        rx.button("Post", on_click=ChatState.process_data, style=styles.button_style), width="30%"
    )

@template(route="/",title="Prompt", image="/github.svg")
def index() -> rx.component:
    return rx.vstack(
        rx.heading("mood_app", font_size="3em"),
        rx.spacer(), rx.spacer(), rx.spacer(),
        # implement timer here
        rx.box("What's on your mind?",style=styles.question_style,
            text_align="center",width ="30%",),
        action_bar(),

    )

