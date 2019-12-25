import arcade
import settings
import math

game = []

class Grid:
    def __init__(self, columns, rows, margin):
        self.columns = columns
        self.rows = rows
        self.margin = margin
        self.start_board = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
        self.board = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
        self.selected = (math.ceil(self.columns / 2), math.ceil(self.rows / 2))
        self.x_gap = settings.WIDTH / self.columns
        self.y_gap = settings.HEIGHT / self.rows

    
    def generate_board(self, difficulty):
        # this will create a start_board for the game
        pass
    
    def solve(self):
        pass

    def validate(self):
        pass

    def pencil(self, x_cord, y_cord, number):
        pass

    def draw_grid(self):
        # REMOVE -- y_bottom is 100 and y_top is 550
        x_start = settings.WIDTH / 9
        y_pos = settings.HEIGHT / 6

        # HORIZONTAL LINES
        for i in range(1, self.columns):
            x_pos = x_start * i

            if i % 3 != 0:
                thickness = 1
                color = arcade.color.LIGHT_SLATE_GRAY

            else:
                thickness *= 3
                color = arcade.color.BLIZZARD_BLUE

            arcade.draw_rectangle_filled(x_pos, settings.HEIGHT / 1.865, thickness, settings.HEIGHT / (4/3), color)
        
        # VERTICAL LINES
        for i in range(1, self.rows):
            y_pos += (settings.HEIGHT / (4/3)) / 9

            if i % 3 != 0:
                thickness = 1
                color = arcade.color.LIGHT_SLATE_GRAY
            else:
                thickness *= 3
                color = arcade.color.BLIZZARD_BLUE

            arcade.draw_rectangle_filled(settings.WIDTH / 2, y_pos, thickness, settings.WIDTH, color, tilt_angle=90)

        # GIVEN NUMBERS
        for row in range(self.rows):
            for column in range(self.columns):
                if self.start_board[row][column]:
                    x = column
                    y = row
                    translated_x = self.x_gap * (3/2) + ((self.x_gap) * (x - 1))
                    translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y)
                    arcade.draw_circle_filled(translated_x, translated_y - 51, 17, arcade.color.PAYNE_GREY)
                    arcade.draw_text(str(self.start_board[row][column]), translated_x, translated_y - 60,
                         arcade.color.LIGHT_GRAY,font_size=18, font_name='arial', anchor_x="center")
                elif self.board[row][column]:
                    x = column
                    y = row
                    translated_x = self.x_gap * (3/2) + ((self.x_gap) * (x - 1))
                    translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y)

                    if self.selected == (column + 1, row + 1):
                        arcade.draw_text(str(self.board[row][column]), translated_x, translated_y - 60,
                         arcade.color.BLACK,font_size=18, font_name='arial', anchor_x="center")
                    else:
                        arcade.draw_text(str(self.board[row][column]), translated_x, translated_y - 60,
                            arcade.color.BLIZZARD_BLUE,font_size=18, font_name='arial', anchor_x="center")
                else:
                    pass

    def display_selected(self):
        x = self.selected[0]
        y = self.selected[1]
        translated_x = self.x_gap / 2 + ((self.x_gap) * (x - 1))
        translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y)
        
        arcade.draw_circle_filled(translated_x, translated_y - 1, 17, arcade.color.BLIZZARD_BLUE)


class Winner:
    all_winners = []

    def __init__(self, name, time):
        self.name = name
        self.time = time
        all_winners.append(self)
    
    @classmethod
    def create_anon_winner(cls, time):
        return Winner('Anonymous', time)


class Menu(arcade.View):
    pass

class Instructions(arcade.View):
    pass

class Sudoku(arcade.View):
    def __init__(self):
        super().__init__()
        self.timer = 0

    def on_show(self):
        global game
        arcade.set_background_color(arcade.color.EERIE_BLACK)
        if game != []:
            pass
        else:
            game = Grid(9, 9, 15)
    
    def on_draw(self):
        time = f"Time: {str(int((round(self.timer, 0))))}"
        arcade.start_render()
        arcade.draw_text(time, 50, 570,
                         arcade.color.LIGHT_GRAY,font_size=18, font_name='arial', anchor_x="center")
        game.display_selected()
        game.draw_grid()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == 49:
            x = game.selected[0] - 1
            y = game.selected[1] - 1
            if game.start_board[y][x]:
                pass
            else:
                game.board[y][x] = 1
        elif symbol == 50:
            x = game.selected[0] - 1
            y = game.selected[1] - 1
            if game.start_board[y][x]:
                pass
            else:
                game.board[y][x] = 2
        elif symbol == 51:
            x = game.selected[0] - 1
            y = game.selected[1] - 1
            if game.start_board[y][x]:
                pass
            else:
                game.board[y][x] = 3
        elif symbol == 52:
            x = game.selected[0] - 1
            y = game.selected[1] - 1
            if game.start_board[y][x]:
                pass
            else:
                game.board[y][x] = 4
        elif symbol == 53:
            x = game.selected[0] - 1
            y = game.selected[1] - 1
            if game.start_board[y][x]:
                pass
            else:
                game.board[y][x] = 5
        elif symbol == 54:
            x = game.selected[0] - 1
            y = game.selected[1] - 1
            if game.start_board[y][x]:
                pass
            else:
                game.board[y][x] = 6
        elif symbol == 55:
            x = game.selected[0] - 1
            y = game.selected[1] - 1
            if game.start_board[y][x]:
                pass
            else:
                game.board[y][x] = 7
        elif symbol == 56:
            x = game.selected[0] - 1
            y = game.selected[1] - 1
            if game.start_board[y][x]:
                pass
            else:
                game.board[y][x] = 8
        elif symbol == 57:
            x = game.selected[0] - 1
            y = game.selected[1] - 1
            if game.start_board[y][x]:
                pass
            else:
                game.board[y][x] = 9
        else:
            pass

        if symbol == 65307:
            pause_screen = PauseScreen(self)
            self.window.show_view(pause_screen)
        else:
            pass
    
    def on_update(self, delta_time):
        self.timer += delta_time
    
    def on_mouse_press(self, x, y, button, modifiers):
        x_coordinate = math.ceil(x / (settings.WIDTH / 9))
        y_coordinate = 11 - math.ceil((y - (settings.HEIGHT / 12)) / (settings.HEIGHT / 12))
        if x_coordinate <= 9 and y_coordinate <= 9 and x_coordinate > 0 and y_coordinate > 0:
            game.selected = (x_coordinate, y_coordinate)

class PauseScreen(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.EERIE_BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('>PRESS <ESCAPE> TO GIVE UP', settings.WIDTH / 2, settings.HEIGHT / 2,
                         arcade.color.LIGHT_GRAY,font_size=25, font_name='arial', anchor_x="center")
        arcade.draw_text('>PRESS <ENTER> TO RESUME GAME', settings.WIDTH / 2, settings.HEIGHT / 1.5,
                         arcade.color.LIGHT_GRAY,font_size=25, font_name='arial', anchor_x="center")


    def on_key_press(self, symbol, modifiers):
        if symbol == 65307: # escape
            self.window.next_view()
        elif symbol == 65293: # enter
            self.window.show_view(self.game_view)
        else:
            pass

class Leaderboard(arcade.View):
    pass


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
    game_view = Sudoku()
    window.show_view(game_view)
    arcade.run()

# am I allowed to do this lol?
if __name__ != "__main__":
    #set-up for main.py
    game_view = Sudoku()