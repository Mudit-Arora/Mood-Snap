"""The dashboard page."""
import json
from mood_app.templates import template
from mood_app import styles

import reflex as rx
from ..state import State

from convex import ConvexClient, ConvexError

client = ConvexClient("https://elegant-fox-172.convex.cloud")

class CommentState(State):

    answer = ""

    done = False
    cursor = ""
    data = []


    # @rx.var
    #
    #     return ["hello", "asdf"]

    async def process_data(self):
        # call convex here answer
       
        # while not self.done:
        result = client.mutation('posts:list')
        self.data = list(result.items())
        pass

# def message(message):
#     return rx.box(
#         rx.vstack(
#             rx.text_box(message.original_text),
#             rx.down_arrow(),
#             rx.text_box(message.text),
#             rx.box(
#                 rx.text(message.to_lang),
#                 rx.text(" · ", margin_x="0.3rem"),
#                 rx.text(message.created_at),
#                 display="flex",
#                 font_size="0.8rem",
#                 color="#666",
#             ),
#             spacing="0.3rem",
#             align_items="left",
#         ),
#         background_color="#f5f5f5",
#         padding="1rem",
#         border_radius="8px",
#     )

def action_bar() -> rx.Component:
    return rx.container(
        rx.input(placeholder="Comment",
                 on_blur=CommentState.set_answer,
                 text_align ="center",
                 style=styles.answer_style),
        rx.button("Post", on_click=CommentState.process_data, style=styles.button_style),
        # add posting functionality and showing on the spot
        # rx.vstack(
        #     rx.foreach(State.messages, message),
        #     margin_top="2rem",
        #     spacing="1rem",
        #     align_items="left",
        # ),
        # padding="2rem",
        # max_width="600px",
    )

@template(route="/dashboard", title="Feed")
def dashboard() -> rx.Component:
    return rx.vstack(
        rx.heading("Feed", font_size="3em"),
        rx.spacer(), rx.spacer(), rx.spacer(),
        rx.ordered_list(rx.foreach(CommentState.data, lambda item: rx.text(item))),
        rx.box("Attending my first hackathon!", style=styles.question_style,
               text_align="left", width="30%", ),
        action_bar(),
    )
