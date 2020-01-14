import arcade
import settings

from time import time
import random
from typing import List
import pickle
from datetime import date

TITLE = "Some disasterous Game"
TEXT_COLOR = arcade.color.ARSENIC
SCREEN_COLOR = arcade.color.BONE

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT
PRESS_ANY_KEY_TEXT = "Press any key to return to the Menu"

PICKLE_FILE = "sri_data.p"

global mode, save_file, cur_game
mode = "menu"


class SriMenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)
    
    def on_draw(self):
        arcade.start_render()

        # Title
        arcade.draw_text(TITLE, WIDTH/2, 0.85 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 30), anchor_x="center", align="right")

        # Labels
        arcade.draw_text("PLAY (P)", WIDTH/2, 0.7 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
        arcade.draw_text("INSTRUCTIONS (I)", WIDTH/2, 0.5 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
        arcade.draw_text("SCOREBOARD (S)", WIDTH/2, 0.3 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
        arcade.draw_text("Press (N) to go to the next game", 0.175 * WIDTH, 0.003 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")

    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        global mode
        if key == 112: # P for Play
            mode = "ask player name"
            self.window.show_view(SriGameView())
        elif key == 105: # I for Instructions
            mode = "instructions"
            self.window.show_view(SriInstructionsView(self))
        elif key == 115: # S for Scoreboard
            mode = "scoreboard"
            self.window.show_view(SriScoreBoardView(self))
        elif key == 110: # N for Next Game
            self.window.next_view()


class SriAskPlayerNameView(arcade.View):
    name = ""

    def __init__(self):
        super().__init__()
        SriAskPlayerNameView.name = ""
    
    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)
    
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text("Please type your name | Your name must be 5 characters or shorter", 0.5 * WIDTH, HEIGHT - (0.03 * HEIGHT),
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")
        arcade.draw_text("Press (ENTER) when complete | Press (ESC) to go to the Menu", 0.5 * WIDTH, HEIGHT - (0.07 * HEIGHT),
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")

        arcade.draw_text(f'Name: "{SriAskPlayerNameView.name}"', 0.5 * WIDTH, 0.5 * HEIGHT,
                         TEXT_COLOR, font_size=(0.02 * (HEIGHT + WIDTH)), anchor_x="center", align="center")
    
    def update(self, delta_time: float):
        pass

    def on_key_press(self, key, modifiers):
        global mode
        if key == 65307: # ESCAPE
            mode = "menu"
            self.window.show_view(SriMenuView(self))
        elif key == 65288: # BACKSPACE
            SriAskPlayerNameView.name = SriAskPlayerNameView.name[:-1]
        elif key == 65293: # ENTER
            mode = "play"
            self.window.show_view(SriGameView())
        elif len(SriAskPlayerNameView.name) >= 5:
            pass
        elif key in range(97, 122 + 1):
            SriAskPlayerNameView.name += key_code_to_letter(key)


class SriGameView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        global mode, cur_game
        if mode == "menu":
            self.window.show_view(SriMenuView(self))
        elif mode == "instructions":
            self.window.show_view(SriInstructionsView(self))
        elif mode == "scoreboard":
            self.window.show_view(SriScoreBoardView(self))
        elif mode == "play":
            cur_player = SriAskPlayerNameView.name
            cur_game = Game(
                Score(0, cur_player),
                Article()
                )
        elif mode == "ask player name":
            self.window.show_view(SriAskPlayerNameView())
    

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(SCREEN_COLOR)

        global cur_game

        # Titles and Related
        arcade.draw_text("Press (ESC) to go to the Menu | Use the mouse to click on the words", 0.5 * WIDTH, 0.97 *  HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")        

        disp_clock = game_display_time(1)
        cur_points = cur_game.game_score.get_points()
        disp_date = convert_date_to_words(cur_game.article.date)

        arcade.draw_text(f"Time: {disp_clock}s / {cur_game.max_time}s", 0.5 * WIDTH, 0.035 * HEIGHT,
                         TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)), anchor_x="left", align="left")
        arcade.draw_text(f"Points: {cur_points}", 0.2 * WIDTH, 0.035 * HEIGHT,
                         TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)), anchor_x="left", align="left")

        arcade.draw_text(f"{cur_game.article.title}    By: {cur_game.article.author}", 0.5 * WIDTH, 0.9 * HEIGHT,
                         TEXT_COLOR, font_size=(0.016 * (HEIGHT + WIDTH)), anchor_x="center", align="center", bold=True, italic=True)
        arcade.draw_text(f"Date: {disp_date}", 0.5 * WIDTH, 0.85 * HEIGHT,
                         TEXT_COLOR, font_size=(0.012 * (HEIGHT + WIDTH)), anchor_x="center", align="center", bold=True, italic=True)


        unused_words = cur_game.article.unused_words
        lines_to_show = cur_game.article.words_to_lines(unused_words)

        num_lines_to_show = len(lines_to_show)

        if num_lines_to_show > 7:
            num_lines_to_show = 7

        '''

        word_writing_range = range(1, num_lines_to_show)

        for i in word_writing_range:
            arcade.draw_text(lines_to_show[i], 0.5 * WIDTH, (i + 1) * 0.1 * HEIGHT,
                            TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)), anchor_x="center", align="center")

        '''
        # IM CHANGING THE WAY THE GAME WORDS!!!

        # 10 words, labelled 0 - 9
        # computer plays the game (finds a path of words that work)
        # shuffles the words and displays them 0 - 9
        # each word = 10 points
        # more points based on the time left



        '''
        words pop up on screen in boxes

        bottom of screen: score, words joined, word_speed (time it took from your previous word to current word)

        # add stuff like words joined and word speed to the game class

        '''
        
        # End Game
        if float(disp_clock[:-1]) > cur_game.max_time:
            global mode
            mode = "endgame"
            self.window.show_view(SriEndGameView())
    

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            print("Im here!", x, y)

    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        if key == 65307: # ESCAPE for menu
            global mode
            mode = "menu"
            self.window.show_view(SriMenuView(self))


class SriInstructionsView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)
    
    def on_draw(self):
        arcade.start_render()
        instruction_text = """

        CONTROLS:

        Move the mouse and
        click on the
        words and buttons

        """
        arcade.draw_text(instruction_text, 0.6 * WIDTH,  0 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
    
        arcade.draw_text(PRESS_ANY_KEY_TEXT, 0.175 * WIDTH, 0.003 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")
        
    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        global mode
        mode = "menu"
        self.window.show_view(SriMenuView(self))


class SriScoreBoardView(arcade.View):
    nuke_counter = 0

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view


    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)


    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Score Board", WIDTH/2, 0.9 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")

        arcade.draw_text(PRESS_ANY_KEY_TEXT, 0.175 * WIDTH, 0.003 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")

        top_5_names = []
        top_5_scores = []

        top_scores = Score.get_top_scores()

        num_scores_to_show = len(top_scores)

        if num_scores_to_show > 5:
            num_scores_to_show = 5

        for i in range(num_scores_to_show):
            top_5_scores.append(top_scores[i].get_points())
            top_5_names.append(top_scores[i].get_player())

        for i in range(num_scores_to_show):
            arcade.draw_text(f"{i + 1}. '{top_5_names[i]}' ---- {top_5_scores[i]}",
                             WIDTH * 0.3, 0.8 * HEIGHT - HEIGHT * 0.07 * i * 2, arcade.color.BLUE, 18, align="left")
    
    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        if key == 110: # N for nuke
            SriScoreBoardView.nuke_counter += 1
            if SriScoreBoardView.nuke_counter >= 10:
                global save_file
                SriScoreBoardView.nuke_counter = 0
                save_file.nuke()
                save_file.load_from_file()
        else:
            self.window.show_view(SriMenuView(self))
            global mode
            mode = "menu"


class SriEndGameView(arcade.View):
    def __init__(self):
        super().__init__()
    
    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)
    
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text("Press any key to return to the menu", 0.5 * WIDTH, HEIGHT - (0.03 * HEIGHT),
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="center")
        
        global cur_game

        arcade.draw_text(f"Player: {cur_game.game_score.get_player()}\n\nPoints: {cur_game.game_score.get_points()}\n\n Rank: {cur_game.game_score.find_rank()}", 0.5 * WIDTH, 0.2 * HEIGHT,
                         TEXT_COLOR, font_size=(0.05 * (HEIGHT + WIDTH)), anchor_x="center", align="center")
    
    def update(self, delta_time: float):
        pass

    def on_key_press(self, key, modifiers):
        global mode
        mode = "menu"
        self.window.show_view(SriMenuView(self))


class Game:
    def __init__(self, game_score: "Score", article: "Article"):
        self.game_score = game_score
        self.article = article
        self.start_time = time()
        self.max_time = 30


class Score:
    all_scores = []
    
    def __init__(self, points: int, player: int):
        self._points = points
        self._player = player
        self._time = float(time())

        Score.all_scores.append(self)
    
    def change_points(self, points: int):
        if isinstance(points, int):
            self._points = points
        else:
            raise Exception("Points should be an integer")

    def add_points(self, points: int):
        if isinstance(points, int):
            self._points += points
        else:
            raise Exception("Points should be an integer")

    def get_points(self):
        return self._points

    def set_player(self, player: str):
        if isinstance(player, str):
            self._player = player
        else:
            self._player = str(player)

    def get_player(self):
        return self._player

    def set_time(self, time: float):
        if isinstance(time, float) and time > 0:
            self._time = time
        else:
            raise Exception("Time should be a positive float")

    def get_time(self):
        return time

    @classmethod
    def get_top_scores(cls): 
        return merge_sort_scores(cls.all_scores)
    
    def find_rank(self) -> int:
        scores = Score.get_top_scores()

        global cur_game

        for i in range(len(scores)):
            if scores[i] == cur_game.game_score:
                rank = i
                break

        return rank + 1


class Article:
    def __init__(self):
        self.used_words = []
        unused_words = get_words()
        random.shuffle(unused_words)
        self.unused_words = unused_words[0:100]
        self.all_words = unused_words[0:100]
        self.title = Article.make_title(3)

        self.author = f'{Article.make_name("Berock")} {Article.make_name("Obamer")}'
        self.date = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1600, 2300)}"

    @staticmethod
    def make_title(num_words: int) -> str:
        words = get_words()
        random.shuffle(words)
        
        title = ""

        for i in range(3):
            rand_word = random.choice(words)
            rand_word = rand_word[0].upper() + rand_word[1:].lower()
            title += (rand_word + " ")
        
        return title[:-1]

    @staticmethod
    def make_name(backup: str) -> str:
        words = get_words()

        random.shuffle(words)
        for word in words:
            if word[0].isupper() and len(word) > 3:
                    name = word
                    break
            else:
                name = backup
    
        return name
    
    @staticmethod
    def words_to_lines(words: List[str], line_len: int = 40) -> List[str]:
        lines = [""]

        line_counter = 0    
        i = 0

        while i < len(words):
            if len(lines[line_counter]) + len(words[i]) < line_len:
                lines[line_counter] += (words[i] + " ")
                i += 1
            else:
                line_counter += 1
                lines.append("")

                if len(words[i]) > line_len:
                    i += 1
        
        for i in range(len(lines)):
            lines[i] = lines[i].split()

        return lines


class SaveData:
    def __init__(self):
        global mode
        self.game_mode = "menu"
        self.scores = Score.all_scores

    def load_from_file(self, save_file: str = PICKLE_FILE):
        try:
            save_files = pickle.load(open(save_file, "rb"))
        except EOFError:
            self.game_mode = "menu"

        try:
            self.game_mode = save_files["game_mode"]
            self.scores = save_files["scores"]
        except KeyError:
            self.game_mode = "menu"
            self.scores = []
        except UnboundLocalError:
            self.game_mode = "menu"
            self.scores = []

        global mode
        Score.all_scores = self.scores
        mode = self.game_mode

    def save(self, save_file: str = PICKLE_FILE):
        self.scores = Score.all_scores

        save_files = {
            "game_mode": self.game_mode,
            "scores": self.scores
        }

        pickle.dump(save_files, open(save_file, "wb"))
    
    def nuke(self, save_file: str = PICKLE_FILE):
        pickle.dump({}, open(save_file, "wb"))


global save_file
save_file = SaveData()
save_file.load_from_file()


def get_words():
    lines = []
    with open("Sri_Words.txt", "r") as f:
        for line in f:
            lines.append(line.strip())
    
    return lines


def merge_sort_scores(nums: List["Score"]) -> List["Score"]:
    
    if len(nums) <= 1:
        return nums
    
    midpoint = len(nums) // 2

    left_side = merge_sort_scores(nums[:midpoint])
    right_side = merge_sort_scores(nums[midpoint:])

    sorted_list = []

    left_marker = 0
    right_marker = 0

    while left_marker < len(left_side) and right_marker < len(right_side):
        
        if left_side[left_marker].get_points() > right_side[right_marker].get_points():
            sorted_list.append(left_side[left_marker])
            left_marker += 1
        else:
            sorted_list.append(right_side[right_marker])
            right_marker += 1
        
    
    while left_marker < len(left_side):
        sorted_list.append(left_side[left_marker])
        left_marker += 1
    
    while right_marker < len(right_side):
        sorted_list.append(right_side[right_marker])
        right_marker += 1
    
    return sorted_list


def key_code_to_letter(key_code: int) -> str:
    letters = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()

    # A -> 97
    # Z -> 122

    key_code -= 97

    return letters[key_code]


def delta_time(time_1: float, time_2: float) -> float:
    return time_2 - time_1


def game_display_time(decimal_places: int = 3) -> str:
    global cur_game
    disp_clock = delta_time(cur_game.start_time, time())

    disp_clock = round(disp_clock, decimal_places)
    
    return f"{disp_clock}"


def convert_date_to_words(slash_date: str) -> str:
    slash_date = slash_date.split("/")

    for i in range(len(slash_date)):
        slash_date[i] = int(slash_date[i])

    words = date(day=slash_date[0],
                 month=slash_date[1],
                 year=slash_date[2]).strftime('%A %d %B %Y')

    return words

if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = SriGameView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
