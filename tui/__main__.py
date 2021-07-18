# flake8: noqa

import sys, os

from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from tui.view.box_page import BoxPage, NewBoxPage
from tui.view.chat import ChatPage
from tui.view.home import HomePage
from tui.view.settings import Settings
from tui import api_wrapper 
from tui import crypt


class BoxSelection(object):
    """State controller object"""

    def __init__(self):
        # Current contact when editing.
        self.current_box_id = None

        # List of dicts, where each dict contains a single contact, containing
        # name, address, phone, email and notes fields.
        z = os.path.isfile("key.key")
        if not z:
            crypt.write_key()
        x = os.path.isfile("token")
        if not x:
            api_wrapper.join()
        self.boxes = dict()
        self.refresh()
        self.chat_data = {"chat":[],"my_message": ''}
        '''
        get_posts() -> box_id, page_no, load_more
        post() -> box_id, message_body
        '''

    def refresh(self, page_no="1"):
        list_box=api_wrapper.get_boxes(page_no=str(page_no))
        for bx_inf in list_box:
            self.boxes[bx_inf.get("_id")] = bx_inf.get("name")
        pass
    def new_box(self, box_name):
        api_wrapper.new_box(name=box_name)
        self.chat_data = {"chat":[],"my_message": ''}
        pass
    def load_chat(self, box_id) -> dict():
        self.chat_data = {"chat":[],"my_message": ''}
        if box_id:
            posts = api_wrapper.get_posts(box_id=str(box_id))
            for i in posts:
                self.chat_data["chat"].append(i["body"])
        return self.chat_data
    def send_message(self, box_id, message):
        api_wrapper.post(box_id=box_id, body=message)
        self.chat_data = self.load_chat(box_id=box_id)


chat_data = {
    "chat": ["This is the first text", "This is the second text"],
    "my_message": '',
}   


def main(screen: Screen, scene: Scene) -> None:
    """The class's docstring"""
    boxselection = BoxSelection()
    # boxselection.refresh()

    scenes = [
        # Scene([HomePage(screen)], -1, name="HomePage"),
        Scene([BoxPage(screen, box_selection=boxselection)], -1, name="BoxPage"),
        Scene([ChatPage(screen, box_selection=boxselection)], -1, name="ChatPage"),
        Scene([NewBoxPage(screen, boxselection)], -1, name="NewBoxPage"),
        Scene([Settings(screen)], -1, name="Settings"),
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


if __name__ == "__main__":
    last_scene = None
    while True:
        try:
            Screen.wrapper(main, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
