"""The home page of the app."""

from mood_app import styles
from mood_app.templates import template

import reflex as rx
from ..state import State
import random 
import time 

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

    show: bool = False

    def change(self):
        self.show = not (self.show)

    @rx.var
    def is_error(self) -> bool:
        return len(self.answer) <= 0

    answer = ""
    done = False

   #should_redirect: bool = False 

    alert: bool = False
    has_clicked = False

    def process_data(self):
        # call convex here answer
        # save to database
        if self.has_clicked:
            self.show = True
            return

        self.has_clicked = True
        try:
            client.mutation("posts:add", {"content":self.answer})
        except ConvexError as err:
            print(err.data)
        #return rx.redirect("/dashboard")
    
    def show_alert(self):
        self.alert = True
        yield
        import time
        time.sleep(5)
        self.alert = False

def action_bar() -> rx.Component:
    return rx.hstack(
        rx.form_control(
            rx.input(
                placeholder="Tell me your thoughts",
                on_blur=ChatState.set_answer,
                text_align="center",
                style=styles.answer_style,
            ),
            rx.cond(
                ChatState.is_error,
                rx.form_error_message("You need to write something before posting."),
                rx.form_helper_text("Enter your response"),
            ),
            is_invalid=ChatState.is_error,
            is_required=True,
        ),
        rx.cond(
            ChatState.is_error,
            rx.button("Post", disabled=True, style=styles.button_style, text_align="center"),
            rx.button("Post", on_click=ChatState.process_data, style=styles.button_style, text_align="center"),

        ),
        width="100%"
    )

# Define a list of prompts
prompts = [
    "What's on your mind?",
    "What is your comfort food",
    "Tell us ways to brighten your day",
    "Tell us about your day in one word",
    "Share a funny childhood memory",
    "What's your go-to karaoke song",
    "Tell me about a memorable adventure",
    "Share a quirky hobby that brings you joy",
    "Tell us the most cringe joke you ever made",
    "Best way to take care of your mental health"
]

@template(route="/",title="Prompt")

def index() -> rx.component:
    random_prompt = random.choice(prompts)
    return rx.center(
        rx.vstack(
            rx.heading("Mood Snap", font_size="3em"),
            rx.divider(),
            rx.box(
                random_prompt,
                style=styles.question_style,
                text_align="center",
                width="100%",
            ),
            action_bar(),
            rx.cond(
                ChatState.show,
                rx.box(
    rx.alert_dialog(
        rx.alert_dialog_overlay(
            rx.alert_dialog_content(
                rx.alert_dialog_header("We would love to hear about your thoughts but..."),
                rx.alert_dialog_body(
                    "You have already posted, please come back again in some time"
                ),
                rx.alert_dialog_footer(
                    rx.button(
                        "OK",
                        on_click=ChatState.change,
                    )
                ),
            )
        ),
        is_open=ChatState.show,
    ),
)
            ),
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


