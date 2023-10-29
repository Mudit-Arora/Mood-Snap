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
    comment = ""

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
        #breakpoint()
        self.data = [(v["content"], v["_id"]) for v in result]
        #pass

    def add_comment(self, postId):
        # call convex here answer
        # while not self.done:
        client.mutation('posts:comment', {'postId': postId, 'content': self.comment})
        #breakpoint()
        #pass

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

def action_bar(postId) -> rx.Component:
    return rx.container(
        rx.box(
            rx.input(
                placeholder="Comment",
                on_blur=CommentState.set_comment,
                text_align="center",
                style=styles.answer_style,
            ),
            width="100%",  # Adjust the width of the input box
        ),
        rx.box(
            rx.button(
                "Post",
                on_click=CommentState.add_comment(postId),
                style=styles.button_style,
            ),
            width="30%",  # Adjust the width of the "Post" button
        ),
        display="flex",  # Use flex layout to align input and button horizontally
        justify_content="center",  # Center-align the input and button
        width="100%",
        padding="1em",
    )

@template(route="/dashboard", title="Feed")
def dashboard() -> rx.Component:
    data = client.mutation('posts:list')
    answers = [(v["content"], v["_id"]) for v in data]

    # Create a list to hold the combined answer box and action bar components
    answer_components = []

    # Iterate through the answers and create a combined component for each answer
    for answer in answers:
        answer_box = rx.box(answer[0], style=styles.question_style, width="100%", text_align="center")
        action_bar_component = action_bar(postId=answer[1])  # Create an action bar component

        # Combine the answer box and action bar components in a vertical stack
        answer_component = rx.vstack(answer_box, action_bar_component)
        
        answer_components.append(answer_component)

    return rx.vstack(
        rx.heading("Feed", font_size="3em"),
        rx.divider(),
        rx.ordered_list(rx.foreach(CommentState.data, lambda item: rx.text(item))),
        # Add the answer box and action bar components to the layout
        *answer_components,
    )








