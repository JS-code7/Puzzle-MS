1,   1: import pygame
    2,   2: import random
    3,   3: import sys
    4,   4: import time
-   5     : import math
    6,   5: from pygame.locals import *
    7,   6:
-   8     : # Initialize pygame
+        7: # Initialize Pygame
    9,   8: pygame.init()
   10,   9:
-  11     : # Constants
+       10: # Game constants
   12,  11: WINDOW_WIDTH = 800
   13,  12: WINDOW_HEIGHT = 600
-  14     : FPS = 30
   15,  13: CARD_WIDTH = 100
   16,  14: CARD_HEIGHT = 100
   17,  15: GRID_ROWS = 4
   18,  16: GRID_COLS = 4
-  19     : MARGIN = 10
-  20     : REVEAL_SPEED = 8
+       17: GRID_PADDING = 20
+       18: CARD_PADDING = 10
   21,  19:
   22,  20: # Colors
-  23     : WHITE = (255, 255, 255)
   24,  21: BLACK = (0, 0, 0)
-  25     : GRAY = (100, 100, 100)
+       22: WHITE = (255, 255, 255)
+       23: GRAY = (200, 200, 200)
+       24: DARK_GREEN = (0, 100, 0)
+       25: LIGHT_GREEN = (144, 238, 144)
   26,  26: BLUE = (0, 0, 255)
-  27     : GREEN = (0, 255, 0)
   28,  27: RED = (255, 0, 0)
-  29     : YELLOW = (255, 255, 0)
   30,  28: PURPLE = (128, 0, 128)
-  31     : CYAN = (0, 255, 255)
   32,  29: ORANGE = (255, 165, 0)
+       30: CYAN = (0, 255, 255)
+       31: YELLOW = (255, 255, 0)
   33,  32: PINK = (255, 192, 203)
-  34     : DARK_GREEN = (0, 100, 0)
-  35     : DARK_BLUE = (0, 0, 100)
-  36     : DARK_RED = (100, 0, 0)
-  37     : DARK_PURPLE = (50, 0, 50)
-  38     : DARK_CYAN = (0, 100, 100)
-  39     : DARK_ORANGE = (139, 69, 19)
-  40     : DARK_PINK = (199, 21, 133)
   41,  33:
   42,  34: # Primordium theme colors
-  43     : PRIMORDIUM_BG = (20, 20, 30)
-  44     : PRIMORDIUM_CARD_BACK = (40, 40, 60)
-  45     : PRIMORDIUM_HIGHLIGHT = (100, 80, 200)
-  46     : PRIMORDIUM_TEXT = (220, 220, 255)
+       35: PRIMORDIUM_BG = (25, 25, 35)
+       36: PRIMORDIUM_CARD_BACK = (45, 45, 60)
+       37: PRIMORDIUM_HIGHLIGHT = (100, 180, 120)
+       38: PRIMORDIUM_TEXT = (220, 220, 220)
   47,  39:
-  48     : # Primordium themed shapes for card fronts
-  49     : SHAPES = [
-  50     :     "crystal", "rune", "portal", "artifact",
-  51     :     "sigil", "vortex", "glyph", "essence"
-  52     : ]
-  53     :
-  54     : # Shape colors
-  55     : SHAPE_COLORS = [
-  56     :     (255, 0, 128),    # Magenta
-  57     :     (128, 0, 255),    # Purple
-  58     :     (0, 128, 255),    # Blue
-  59     :     (0, 255, 128),    # Teal
-  60     :     (128, 255, 0),    # Lime
-  61     :     (255, 128, 0),    # Orange
-  62     :     (255, 255, 128),  # Light Yellow
-  63     :     (128, 255, 255),  # Light Cyan
+       40: # Primordium themed symbols (using simple shapes for demonstration)
+       41: PRIMORDIUM_SYMBOLS = [
+       42:     "crystal", "leaf", "eye", "rune",
+       43:     "spiral", "star", "moon", "sun"
   64,  44: ]
   65,  45:
-  66     : # Set up the window
-  67     : DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
-  68     : pygame.display.set_caption('Primordium Memory Game')
-  69     : CLOCK = pygame.time.Clock()
-  70     :
-  71     : # Font setup
-  72     : FONT = pygame.font.SysFont('Arial', 32)
-  73     : SMALL_FONT = pygame.font.SysFont('Arial', 20)
-  74     :
   75,  46: class Card:
-  76     :     def __init__(self, x, y, shape_type, color):
+       47:     def __init__(self, x, y, width, height, symbol):
   77,  48:         self.x = x
   78,  49:         self.y = y
-  79     :         self.shape_type = shape_type
-  80     :         self.color = color
-  81     :         self.revealed = False
-  82     :         self.matched = False
-  83     :         self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
-  84     :
-  85     :     def draw(self):
-  86     :         if self.matched:
-  87     :             # Draw matched card (slightly transparent)
-  88     :             pygame.draw.rect(DISPLAY_SURFACE, PRIMORDIUM_CARD_BACK, self.rect)
-  89     :             pygame.draw.rect(DISPLAY_SURFACE, PRIMORDIUM_HIGHLIGHT, self.rect, 2)
-  90     :             self.draw_shape()
-  91     :         elif self.revealed:
-  92     :             # Draw revealed card
-  93     :             pygame.draw.rect(DISPLAY_SURFACE, PRIMORDIUM_CARD_BACK, self.rect)
-  94     :             pygame.draw.rect(DISPLAY_SURFACE, PRIMORDIUM_HIGHLIGHT, self.rect, 2)
-  95     :             self.draw_shape()
+       50:         self.width = width
+       51:         self.height = height
+       52:         self.symbol = symbol
+       53:         self.is_flipped = False
+       54:         self.is_matched = False
+       55:         self.flip_animation = 0
+       56:         self.rect = pygame.Rect(x, y, width, height)
+       57:
+       58:     def draw(self, surface):
+       59:         if self.is_matched:
+       60:             # Draw matched card
+       61:             pygame.draw.rect(surface, PRIMORDIUM_HIGHLIGHT, self.rect, border_radius=5)
+       62:             self.draw_symbol(surface)
+       63:         elif self.is_flipped:
+       64:             # Draw flipped card
+       65:             pygame.draw.rect(surface, WHITE, self.rect, border_radius=5)
+       66:             self.draw_symbol(surface)
   96,  67:         else:
   97,  68:             # Draw card back
-  98     :             pygame.draw.rect(DISPLAY_SURFACE, PRIMORDIUM_CARD_BACK, self.rect)
-  99     :             pygame.draw.rect(DISPLAY_SURFACE, PRIMORDIUM_HIGHLIGHT, self.rect, 1)
+       69:             pygame.draw.rect(surface, PRIMORDIUM_CARD_BACK, self.rect, border_radius=5)
  100,  70:
  101,  71:             # Draw decorative pattern on card back
- 102     :             center_x = self.x + CARD_WIDTH // 2
- 103     :             center_y = self.y + CARD_HEIGHT // 2
- 104     :             radius = min(CARD_WIDTH, CARD_HEIGHT) // 4
- 105     :             pygame.draw.circle(DISPLAY_SURFACE, PRIMORDIUM_HIGHLIGHT, (center_x, center_y), radius, 2)
- 106     :             pygame.draw.circle(DISPLAY_SURFACE, PRIMORDIUM_HIGHLIGHT, (center_x, center_y), radius // 2, 1)
+       72:             pygame.draw.rect(surface, (55, 55, 70),
+       73:                             (self.x + 10, self.y + 10, self.width - 20, self.height - 20),
+       74:                             border_radius=3)
+       75:
+       76:             # Draw a small circle in the center
+       77:             pygame.draw.circle(surface, (65, 120, 90),
+       78:                               (self.x + self.width // 2, self.y + self.height // 2),
+       79:                               10)
  107,  80:
- 108     :     def draw_shape(self):
- 109     :         center_x = self.x + CARD_WIDTH // 2
- 110     :         center_y = self.y + CARD_HEIGHT // 2
+       81:     def draw_symbol(self, surface):
+       82:         font = pygame.font.SysFont('Arial', 20)
  111,  83:
- 112     :         if self.shape_type == "crystal":
+       84:         # Different drawing logic based on symbol type
+       85:         if self.symbol == "crystal":
  113,  86:             # Draw a crystal shape
  114,  87:             points = [
- 115     :                 (center_x, center_y - 30),
- 116     :                 (center_x + 20, center_y),
- 117     :                 (center_x, center_y + 30),
- 118     :                 (center_x - 20, center_y)
+       88:                 (self.x + self.width // 2, self.y + 20),
+       89:                 (self.x + self.width - 20, self.y + self.height // 2),
+       90:                 (self.x + self.width // 2, self.y + self.height - 20),
+       91:                 (self.x + 20, self.y + self.height // 2)
  119,  92:             ]
- 120     :             pygame.draw.polygon(DISPLAY_SURFACE, self.color, points)
- 121     :             pygame.draw.polygon(DISPLAY_SURFACE, WHITE, points, 2)
- 122     :
- 123     :         elif self.shape_type == "rune":
- 124     :             # Draw a rune shape
- 125     :             pygame.draw.circle(DISPLAY_SURFACE, self.color, (center_x, center_y), 25)
- 126     :             pygame.draw.line(DISPLAY_SURFACE, WHITE, (center_x - 15, center_y), (center_x + 15, center_y), 2)
- 127     :             pygame.draw.line(DISPLAY_SURFACE, WHITE, (center_x, center_y - 15), (center_x, center_y + 15), 2)
- 128     :             pygame.draw.line(DISPLAY_SURFACE, WHITE, (center_x - 10, center_y - 10), (center_x + 10, center_y + 10), 2)
- 129     :
- 130     :         elif self.shape_type == "portal":
- 131     :             # Draw a portal shape
- 132     :             pygame.draw.circle(DISPLAY_SURFACE, self.color, (center_x, center_y), 25)
- 133     :             pygame.draw.circle(DISPLAY_SURFACE, PRIMORDIUM_BG, (center_x, center_y), 15)
- 134     :             pygame.draw.circle(DISPLAY_SURFACE, WHITE, (center_x, center_y), 25, 2)
- 135     :             pygame.draw.circle(DISPLAY_SURFACE, WHITE, (center_x, center_y), 15, 1)
+       93:             pygame.draw.polygon(surface, CYAN, points)
  136,  94:
- 137     :         elif self.shape_type == "artifact":
- 138     :             # Draw an artifact shape
- 139     :             pygame.draw.rect(DISPLAY_SURFACE, self.color, (center_x - 20, center_y - 20, 40, 40))
- 140     :             pygame.draw.circle(DISPLAY_SURFACE, WHITE, (center_x, center_y), 10)
- 141     :             pygame.draw.rect(DISPLAY_SURFACE, WHITE, (center_x - 20, center_y - 20, 40, 40), 2)
+       95:         elif self.symbol == "leaf":
+       96:             # Draw a leaf shape
+       97:             pygame.draw.ellipse(surface, LIGHT_GREEN,
+       98:                                (self.x + 25, self.y + 25, self.width - 50, self.height - 50))
+       99:             pygame.draw.line(surface, DARK_GREEN,
+      100:                             (self.x + self.width // 2, self.y + 25),
+      101:                             (self.x + self.width // 2, self.y + self.height - 25), 3)
  142, 102:
- 143     :         elif self.shape_type == "sigil":
- 144     :             # Draw a sigil shape
- 145     :             pygame.draw.circle(DISPLAY_SURFACE, self.color, (center_x, center_y), 25)
- 146     :             points = [
- 147     :                 (center_x, center_y - 20),
- 148     :                 (center_x + 20, center_y + 10),
- 149     :                 (center_x - 20, center_y + 10)
- 150     :             ]
- 151     :             pygame.draw.polygon(DISPLAY_SURFACE, WHITE, points, 2)
+      103:         elif self.symbol == "eye":
+      104:             # Draw an eye
+      105:             pygame.draw.ellipse(surface, WHITE,
+      106:                                (self.x + 20, self.y + 35, self.width - 40, self.height - 70))
+      107:             pygame.draw.circle(surface, BLUE,
+      108:                               (self.x + self.width // 2, self.y + self.height // 2), 15)
+      109:             pygame.draw.circle(surface, BLACK,
+      110:                               (self.x + self.width // 2, self.y + self.height // 2), 7)
  152, 111:
- 153     :         elif self.shape_type == "vortex":
- 154     :             # Draw a vortex shape
- 155     :             pygame.draw.circle(DISPLAY_SURFACE, self.color, (center_x, center_y), 25)
- 156     :             for i in range(0, 360, 45):
- 157     :                 rad = i * 3.14159 / 180
- 158     :                 x1 = center_x + int(15 * math.cos(rad))
- 159     :                 y1 = center_y + int(15 * math.sin(rad))
- 160     :                 x2 = center_x + int(25 * math.cos(rad))
- 161     :                 y2 = center_y + int(25 * math.sin(rad))
- 162     :                 pygame.draw.line(DISPLAY_SURFACE, WHITE, (x1, y1), (x2, y2), 2)
+      112:         elif self.symbol == "rune":
+      113:             # Draw a rune symbol
+      114:             pygame.draw.line(surface, PURPLE,
+      115:                             (self.x + 30, self.y + 30),
+      116:                             (self.x + self.width - 30, self.y + self.height - 30), 5)
+      117:             pygame.draw.line(surface, PURPLE,
+      118:                             (self.x + self.width - 30, self.y + 30),
+      119:                             (self.x + 30, self.y + self.height - 30), 5)
+      120:             pygame.draw.circle(surface, PURPLE,
+      121:                               (self.x + self.width // 2, self.y + self.height // 2), 10, 3)
  163, 122:
- 164     :         elif self.shape_type == "glyph":
- 165     :             # Draw a glyph shape
- 166     :             pygame.draw.rect(DISPLAY_SURFACE, self.color, (center_x - 20, center_y - 20, 40, 40))
- 167     :             pygame.draw.line(DISPLAY_SURFACE, WHITE, (center_x - 15, center_y - 15), (center_x + 15, center_y + 15), 2)
- 168     :             pygame.draw.line(DISPLAY_SURFACE, WHITE, (center_x + 15, center_y - 15), (center_x - 15, center_y + 15), 2)
- 169     :             pygame.draw.rect(DISPLAY_SURFACE, WHITE, (center_x - 20, center_y - 20, 40, 40), 2)
+      123:         elif self.symbol == "spiral":
+      124:             # Draw a spiral (simplified)
+      125:             center_x = self.x + self.width // 2
+      126:             center_y = self.y + self.height // 2
+      127:             for i in range(0, 80, 5):
+      128:                 angle = 0.1 * i
+      129:                 x = center_x + int(i/3 * pygame.math.Vector2(1, 0).rotate(angle).x)
+      130:                 y = center_y + int(i/3 * pygame.math.Vector2(1, 0).rotate(angle).y)
+      131:                 pygame.draw.circle(surface, ORANGE, (x, y), 3)
+      132:
+      133:         elif self.symbol == "star":
+      134:             # Draw a star
+      135:             center_x = self.x + self.width // 2
+      136:             center_y = self.y + self.height // 2
+      137:             points = []
+      138:             for i in range(5):
+      139:                 # Outer points
+      140:                 angle = (2 * pygame.math.pi * i / 5) - pygame.math.pi / 2
+      141:                 points.append((
+      142:                     center_x + int(30 * pygame.math.cos(angle)),
+      143:                     center_y + int(30 * pygame.math.sin(angle))
+      144:                 ))
+      145:                 # Inner points
+      146:                 angle += pygame.math.pi / 5
+      147:                 points.append((
+      148:                     center_x + int(15 * pygame.math.cos(angle)),
+      149:                     center_y + int(15 * pygame.math.sin(angle))
+      150:                 ))
+      151:             pygame.draw.polygon(surface, YELLOW, points)
  170, 152:
- 171     :         elif self.shape_type == "essence":
- 172     :             # Draw an essence shape
- 173     :             points = [
- 174     :                 (center_x, center_y - 25),
- 175     :                 (center_x + 25, center_y),
- 176     :                 (center_x, center_y + 25),
- 177     :                 (center_x - 25, center_y)
- 178     :             ]
- 179     :             pygame.draw.polygon(DISPLAY_SURFACE, self.color, points)
- 180     :             pygame.draw.circle(DISPLAY_SURFACE, WHITE, (center_x, center_y), 10, 1)
- 181     :             pygame.draw.polygon(DISPLAY_SURFACE, WHITE, points, 2)
+      153:         elif self.symbol == "moon":
+      154:             # Draw a crescent moon
+      155:             pygame.draw.circle(surface, WHITE,
+      156:                               (self.x + self.width // 2, self.y + self.height // 2), 30)
+      157:             pygame.draw.circle(surface, PRIMORDIUM_CARD_BACK,
+      158:                               (self.x + self.width // 2 + 15, self.y + self.height // 2 - 5), 25)
  182, 159:
- 183     :         # Draw shape name
- 184     :         text = SMALL_FONT.render(self.shape_type, True, WHITE)
- 185     :         text_rect = text.get_rect(center=(center_x, center_y + 35))
- 186     :         DISPLAY_SURFACE.blit(text, text_rect)
+      160:         elif self.symbol == "sun":
+      161:             # Draw a sun
+      162:             pygame.draw.circle(surface, YELLOW,
+      163:                               (self.x + self.width // 2, self.y + self.height // 2), 25)
+      164:             for i in range(8):
+      165:                 angle = 2 * pygame.math.pi * i / 8
+      166:                 start_x = self.x + self.width // 2 + int(25 * pygame.math.cos(angle))
+      167:                 start_y = self.y + self.height // 2 + int(25 * pygame.math.sin(angle))
+      168:                 end_x = self.x + self.width // 2 + int(35 * pygame.math.cos(angle))
+      169:                 end_y = self.y + self.height // 2 + int(35 * pygame.math.sin(angle))
+      170:                 pygame.draw.line(surface, YELLOW, (start_x, start_y), (end_x, end_y), 3)
+      171:
+      172:         # Draw symbol text below the visual representation
+      173:         text = font.render(self.symbol.capitalize(), True, BLACK)
+      174:         text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height - 15))
+      175:         surface.blit(text, text_rect)
+      176:
+      177:     def flip(self):
+      178:         if not self.is_matched and not self.is_flipped:
+      179:             self.is_flipped = True
+      180:             return True
+      181:         return False
  187, 182:
- 188     : class Game:
+      183: class MemoryGame:
  189, 184:     def __init__(self):
- 190     :         self.reset_game()
+      185:         self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
+      186:         pygame.display.set_caption("Primordium Memory Game")
+      187:         self.clock = pygame.time.Clock()
+      188:         self.font = pygame.font.SysFont('Arial', 32)
+      189:         self.small_font = pygame.font.SysFont('Arial', 24)
  191, 190:
- 192     :     def reset_game(self):
- 193     :         self.cards = []
- 194     :         self.first_selection = None
- 195     :         self.second_selection = None
  196, 191:         self.current_player = 1
  197, 192:         self.player1_score = 0
  198, 193:         self.player2_score = 0
+      194:
+      195:         self.cards = []
+      196:         self.flipped_cards = []
+      197:         self.waiting_time = 0
  199, 198:         self.game_over = False
- 200     :         self.wait_time = 0
- 201     :         self.matches_found = 0
- 202     :         self.total_pairs = (GRID_ROWS * GRID_COLS) // 2
  203, 199:
- 204     :         # Create card pairs
- 205     :         shape_colors = list(zip(SHAPES, SHAPE_COLORS))
- 206     :         selected_pairs = random.sample(shape_colors, (GRID_ROWS * GRID_COLS) // 2)
- 207     :         card_data = selected_pairs * 2
- 208     :         random.shuffle(card_data)
+      200:         self.init_game()
+      201:
+      202:     def init_game(self):
+      203:         # Create a list of symbols (pairs)
+      204:         symbols = PRIMORDIUM_SYMBOLS * 2
+      205:         random.shuffle(symbols)
  209, 206:
- 210     :         # Create and position cards
- 211     :         start_x = (WINDOW_WIDTH - (GRID_COLS * (CARD_WIDTH + MARGIN))) // 2
- 212     :         start_y = (WINDOW_HEIGHT - (GRID_ROWS * (CARD_HEIGHT + MARGIN))) // 2
+      207:         # Calculate grid dimensions
+      208:         grid_width = GRID_COLS * (CARD_WIDTH + CARD_PADDING) - CARD_PADDING
+      209:         grid_height = GRID_ROWS * (CARD_HEIGHT + CARD_PADDING) - CARD_PADDING
  213, 210:
- 214     :         index = 0
+      211:         start_x = (WINDOW_WIDTH - grid_width) // 2
+      212:         start_y = (WINDOW_HEIGHT - grid_height) // 2
+      213:
+      214:         # Create cards
+      215:         self.cards = []
+      216:         symbol_index = 0
+      217:
  215, 218:         for row in range(GRID_ROWS):
  216, 219:             for col in range(GRID_COLS):
- 217     :                 x = start_x + col * (CARD_WIDTH + MARGIN)
- 218     :                 y = start_y + row * (CARD_HEIGHT + MARGIN)
- 219     :                 shape_type, color = card_data[index]
- 220     :                 self.cards.append(Card(x, y, shape_type, color))
- 221     :                 index += 1
+      220:                 x = start_x + col * (CARD_WIDTH + CARD_PADDING)
+      221:                 y = start_y + row * (CARD_HEIGHT + CARD_PADDING)
+      222:
+      223:                 card = Card(x, y, CARD_WIDTH, CARD_HEIGHT, symbols[symbol_index])
+      224:                 self.cards.append(card)
+      225:                 symbol_index += 1
+      226:
+      227:         self.flipped_cards = []
+      228:         self.waiting_time = 0
+      229:         self.game_over = False
+      230:         self.current_player = 1
+      231:         self.player1_score = 0
+      232:         self.player2_score = 0
  222, 233:
- 223     :     def handle_click(self, pos):
- 224     :         if self.wait_time > 0 or self.game_over:
- 225     :             return
+      234:     def handle_events(self):
+      235:         for event in pygame.event.get():
+      236:             if event.type == QUIT:
+      237:                 pygame.quit()
+      238:                 sys.exit()
+      239:
+      240:             if event.type == KEYDOWN:
+      241:                 if event.key == K_ESCAPE:
+      242:                     pygame.quit()
+      243:                     sys.exit()
+      244:                 elif event.key == K_r:
+      245:                     self.init_game()
  226, 246:
- 227     :         for card in self.cards:
- 228     :             if card.rect.collidepoint(pos) and not card.revealed and not card.matched:
- 229     :                 if self.first_selection is None:
- 230     :                     self.first_selection = card
- 231     :                     card.revealed = True
- 232     :                 elif self.second_selection is None and card != self.first_selection:
- 233     :                     self.second_selection = card
- 234     :                     card.revealed = True
- 235     :                     self.check_match()
- 236     :                 break
+      247:             if self.game_over:
+      248:                 if event.type == MOUSEBUTTONDOWN:
+      249:                     # Check if play again button is clicked
+      250:                     mouse_pos = pygame.mouse.get_pos()
+      251:                     button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 50)
+      252:                     if button_rect.collidepoint(mouse_pos):
+      253:                         self.init_game()
+      254:             elif self.waiting_time <= 0:
+      255:                 if event.type == MOUSEBUTTONDOWN and len(self.flipped_cards) < 2:
+      256:                     mouse_pos = pygame.mouse.get_pos()
+      257:                     for card in self.cards:
+      258:                         if card.rect.collidepoint(mouse_pos):
+      259:                             if card.flip():
+      260:                                 self.flipped_cards.append(card)
+      261:                                 if len(self.flipped_cards) == 2:
+      262:                                     self.waiting_time = 1.0  # 1 second delay
+      263:                                 break
  237, 264:
- 238     :     def check_match(self):
- 239     :         if (self.first_selection.shape_type == self.second_selection.shape_type and
- 240     :             self.first_selection.color == self.second_selection.color):
- 241     :             # Match found
- 242     :             self.first_selection.matched = True
- 243     :             self.second_selection.matched = True
+      265:     def update(self):
+      266:         if len(self.flipped_cards) == 2 and self.waiting_time > 0:
+      267:             self.waiting_time -= 1/60  # Assuming 60 FPS
  244, 268:
- 245     :             # Update score
- 246     :             if self.current_player == 1:
- 247     :                 self.player1_score += 1
- 248     :             else:
- 249     :                 self.player2_score += 1
+      269:             if self.waiting_time <= 0:
+      270:                 # Check if cards match
+      271:                 if self.flipped_cards[0].symbol == self.flipped_cards[1].symbol:
+      272:                     # Match found
+      273:                     self.flipped_cards[0].is_matched = True
+      274:                     self.flipped_cards[1].is_matched = True
+      275:
+      276:                     # Update score
+      277:                     if self.current_player == 1:
+      278:                         self.player1_score += 1
+      279:                     else:
+      280:                         self.player2_score += 1
+      281:                 else:
+      282:                     # No match, flip cards back
+      283:                     self.flipped_cards[0].is_flipped = False
+      284:                     self.flipped_cards[1].is_flipped = False
+      285:
+      286:                     # Switch player
+      287:                     self.current_player = 3 - self.current_player  # Toggle between 1 and 2
  250, 288:
- 251     :             self.matches_found += 1
- 252     :
- 253     :             # Reset selections
- 254     :             self.first_selection = None
- 255     :             self.second_selection = None
- 256     :
- 257     :             # Check if game is over
- 258     :             if self.matches_found == self.total_pairs:
- 259     :                 self.game_over = True
- 260     :         else:
- 261     :             # No match, set wait time
- 262     :             self.wait_time = FPS
- 263     :             # Switch player
- 264     :             self.current_player = 3 - self.current_player  # Toggle between 1 and 2
- 265     :
- 266     :     def update(self):
- 267     :         if self.wait_time > 0:
- 268     :             self.wait_time -= 1
- 269     :             if self.wait_time == 0:
- 270     :                 # Flip cards back
- 271     :                 self.first_selection.revealed = False
- 272     :                 self.second_selection.revealed = False
- 273     :                 self.first_selection = None
- 274     :                 self.second_selection = None
+      289:                 self.flipped_cards = []
+      290:
+      291:         # Check if game is over
+      292:         all_matched = all(card.is_matched for card in self.cards)
+      293:         if all_matched:
+      294:             self.game_over = True
  275, 295:
  276, 296:     def draw(self):
  277, 297:         # Draw background
- 278     :         DISPLAY_SURFACE.fill(PRIMORDIUM_BG)
+      298:         self.screen.fill(PRIMORDIUM_BG)
  279, 299:
  280, 300:         # Draw cards
  281, 301:         for card in self.cards:
- 282     :             card.draw()
- 283     :
- 284     :         # Draw UI elements
- 285     :         self.draw_ui()
- 286     :
- 287     :         # Draw game over message if applicable
- 288     :         if self.game_over:
- 289     :             self.draw_game_over()
- 290     :
- 291     :     def draw_ui(self):
- 292     :         # Draw title
- 293     :         title_text = FONT.render("Primordium Memory Game", True, PRIMORDIUM_TEXT)
- 294     :         DISPLAY_SURFACE.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 20))
+      302:             card.draw(self.screen)
  295, 303:
- 296     :         # Draw player scores
- 297     :         p1_text = FONT.render(f"Player 1: {self.player1_score}", True, PRIMORDIUM_TEXT)
- 298     :         p2_text = FONT.render(f"Player 2: {self.player2_score}", True, PRIMORDIUM_TEXT)
+      304:         # Draw player info
+      305:         player1_text = self.font.render(f"Player 1: {self.player1_score}", True,
+      306:                                        PRIMORDIUM_TEXT if self.current_player == 1 else GRAY)
+      307:         player2_text = self.font.render(f"Player 2: {self.player2_score}", True,
+      308:                                        PRIMORDIUM_TEXT if self.current_player == 2 else GRAY)
  299, 309:
- 300     :         DISPLAY_SURFACE.blit(p1_text, (50, 20))
- 301     :         DISPLAY_SURFACE.blit(p2_text, (WINDOW_WIDTH - p2_text.get_width() - 50, 20))
+      310:         self.screen.blit(player1_text, (20, 20))
+      311:         self.screen.blit(player2_text, (WINDOW_WIDTH - player2_text.get_width() - 20, 20))
  302, 312:
  303, 313:         # Draw current player indicator
- 304     :         current_text = SMALL_FONT.render(f"Current Player: {self.current_player}", True, PRIMORDIUM_TEXT)
- 305     :         DISPLAY_SURFACE.blit(current_text, (WINDOW_WIDTH // 2 - current_text.get_width() // 2, 60))
- 306     :
- 307     :         # Draw instructions
- 308     :         instructions = SMALL_FONT.render("Click to flip cards. Match pairs to score points.", True, PRIMORDIUM_TEXT)
- 309     :         DISPLAY_SURFACE.blit(instructions, (WINDOW_WIDTH // 2 - instructions.get_width() // 2, WINDOW_HEIGHT - 30))
- 310     :
- 311     :     def draw_game_over(self):
- 312     :         # Create semi-transparent overlay
- 313     :         overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
- 314     :         overlay.fill((0, 0, 0, 180))
- 315     :         DISPLAY_SURFACE.blit(overlay, (0, 0))
+      314:         current_player_text = self.small_font.render(f"Current Player: {self.current_player}", True, PRIMORDIUM_TEXT)
+      315:         self.screen.blit(current_player_text, (WINDOW_WIDTH // 2 - current_player_text.get_width() // 2, 20))
  316, 316:
- 317     :         # Determine winner
- 318     :         if self.player1_score > self.player2_score:
- 319     :             winner_text = "Player 1 Wins!"
- 320     :         elif self.player2_score > self.player1_score:
- 321     :             winner_text = "Player 2 Wins!"
- 322     :         else:
- 323     :             winner_text = "It's a Tie!"
- 324     :
- 325     :         # Draw game over message
- 326     :         game_over_text = FONT.render("Game Over", True, PRIMORDIUM_TEXT)
- 327     :         winner_render = FONT.render(winner_text, True, PRIMORDIUM_TEXT)
- 328     :
- 329     :         DISPLAY_SURFACE.blit(game_over_text,
+      317:         # Draw game over screen
+      318:         if self.game_over:
+      319:             # Semi-transparent overlay
+      320:             overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
+      321:             overlay.fill((0, 0, 0, 180))
+      322:             self.screen.blit(overlay, (0, 0))
+      323:
+      324:             # Game over text
+      325:             if self.player1_score > self.player2_score:
+      326:                 winner_text = "Player 1 Wins!"
+      327:             elif self.player2_score > self.player1_score:
+      328:                 winner_text = "Player 2 Wins!"
+      329:             else:
+      330:                 winner_text = "It's a Tie!"
+      331:
+      332:             game_over_text = self.font.render("Game Over", True, PRIMORDIUM_TEXT)
+      333:             winner_render = self.font.render(winner_text, True, PRIMORDIUM_TEXT)
+      334:             score_text = self.small_font.render(f"Score: {self.player1_score} - {self.player2_score}", True, PRIMORDIUM_TEXT)
+      335:
+      336:             self.screen.blit(game_over_text,
  330, 337:                             (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,
- 331     :                              WINDOW_HEIGHT // 2 - 50))
- 332     :         DISPLAY_SURFACE.blit(winner_render,
+      338:                              WINDOW_HEIGHT // 2 - 80))
+      339:             self.screen.blit(winner_render,
  333, 340:                             (WINDOW_WIDTH // 2 - winner_render.get_width() // 2,
- 334     :                              WINDOW_HEIGHT // 2))
- 335     :
- 336     :         # Draw play again button
- 337     :         play_again_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 50)
- 338     :         pygame.draw.rect(DISPLAY_SURFACE, PRIMORDIUM_HIGHLIGHT, play_again_rect)
- 339     :         pygame.draw.rect(DISPLAY_SURFACE, PRIMORDIUM_TEXT, play_again_rect, 2)
- 340     :
- 341     :         play_again_text = FONT.render("Play Again", True, PRIMORDIUM_TEXT)
- 342     :         DISPLAY_SURFACE.blit(play_again_text,
+      341:                              WINDOW_HEIGHT // 2 - 30))
+      342:             self.screen.blit(score_text,
+      343:                             (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
+      344:                              WINDOW_HEIGHT // 2 + 20))
+      345:
+      346:             # Play again button
+      347:             button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 50)
+      348:             pygame.draw.rect(self.screen, PRIMORDIUM_HIGHLIGHT, button_rect, border_radius=10)
+      349:
+      350:             play_again_text = self.small_font.render("Play Again", True, BLACK)
+      351:             self.screen.blit(play_again_text,
  343, 352:                             (WINDOW_WIDTH // 2 - play_again_text.get_width() // 2,
  344, 353:                              WINDOW_HEIGHT // 2 + 50 + (50 - play_again_text.get_height()) // 2))
  345, 354:
- 346     :         return play_again_rect
- 347     :
- 348     : def main():
- 349     :     game = Game()
- 350     :     play_again_rect = None
+      355:         pygame.display.flip()
  351, 356:
- 352     :     # Main game loop
- 353     :     while True:
- 354     :         for event in pygame.event.get():
- 355     :             if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
- 356     :                 pygame.quit()
- 357     :                 sys.exit()
- 358     :             elif event.type == MOUSEBUTTONDOWN:
- 359     :                 if game.game_over:
- 360     :                     # Check if play again button was clicked
- 361     :                     if play_again_rect and play_again_rect.collidepoint(event.pos):
- 362     :                         game.reset_game()
- 363     :                 else:
- 364     :                     game.handle_click(event.pos)
- 365     :
- 366     :         # Update game state
- 367     :         game.update()
- 368     :
- 369     :         # Draw everything
- 370     :         game.draw()
- 371     :
- 372     :         # Get play again button rect if game is over
- 373     :         if game.game_over:
- 374     :             play_again_rect = game.draw_game_over()
- 375     :
- 376     :         # Update display
- 377     :         pygame.display.update()
- 378     :         CLOCK.tick(FPS)
+      357:     def run(self):
+      358:         while True:
+      359:             self.handle_events()
+      360:             self.update()
+      361:             self.draw()
+      362:             self.clock.tick(60)
  379, 363:
  380, 364: if __name__ == "__main__":
- 381     :     main()
+      365:     game = MemoryGame()
+      366:     game.run()


Allow this action? Use 't' to trust (always allow) this tool for the session. [y/n/t]:

> t
Replacing: primordium_memory_game.py

 ⋮
 ● Completed in 0.9s



🛠️  Using tool: execute_bash
 ⋮
 ● I will run the following shell command:
cd /mnt/c/Users/Jeet\ soni/ && python -m pip install pygame
 ⋮
 ↳ Purpose: Installing the Pygame library which is required to run the memory game


Allow this action? Use 't' to trust (always allow) this tool for the session. [y/n/t]:

> t
bash: line 1: python: command not found

 ⋮
 ● Completed in 0.92s
Let me try with python3 instead:


🛠️  Using tool: execute_bash (trusted)
 ⋮
 ● I will run the following shell command:
cd /mnt/c/Users/Jeet\ soni/ && python3 -m pip install pygame
 ⋮
 ↳ Purpose: Installing the Pygame library using python3

error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.

    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.

    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.

    See /usr/share/doc/python3.12/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.

 ⋮
 ● Completed in 0.353s
Let's create a virtual environment and install pygame there:


🛠️  Using tool: execute_bash (trusted)
 ⋮
 ● I will run the following shell command:
cd /mnt/c/Users/Jeet\ soni/ && python3 -m venv memory_game_env
 ⋮
 ↳ Purpose: Creating a virtual environment for the game


 ⋮
 ● Completed in 1.534s



🛠️  Using tool: execute_bash (trusted)
 ⋮
 ● I will run the following shell command:
cd /mnt/c/Users/Jeet\ soni/ && source memory_game_env/bin/activate && pip install pygame
 ⋮
 ↳ Purpose: Installing Pygame in the virtual environment

Requirement already satisfied: pygame in ./memory_game_env/lib/python3.12/site-packages (2.6.1)

 ⋮
 ● Completed in 4.170s



🛠️  Using tool: execute_bash (trusted)
 ⋮
 ● I will run the following shell command:
cd /mnt/c/Users/Jeet\ soni/ && source memory_game_env/bin/activate && python primordium_memory_game.py
 ⋮
 ↳ Purpose: Running the Primordium Memory Game

pygame 2.6.1 (SDL 2.28.4, Python 3.12.3)
Hello from the pygame community. https://www.pygame.org/contribute.html
Traceback (most recent call last):
  File "/mnt/c/Users/Jeet soni/primordium_memory_game.py", line 366, in <module>
    game.run()
  File "/mnt/c/Users/Jeet soni/primordium_memory_game.py", line 361, in run
    self.draw()
  File "/mnt/c/Users/Jeet soni/primordium_memory_game.py", line 302, in draw
    card.draw(self.screen)
  File "/mnt/c/Users/Jeet soni/primordium_memory_game.py", line 66, in draw
    self.draw_symbol(surface)
  File "/mnt/c/Users/Jeet soni/primordium_memory_game.py", line 140, in draw_symbol
    angle = (2 * pygame.math.pi * i / 5) - pygame.math.pi / 2
                 ^^^^^^^^^^^^^^
AttributeError: module 'pygame.math' has no attribute 'pi'

 ⋮
 ● Completed in 27.661s



🛠️  Using tool: fs_write (trusted)
 ⋮
 ● Path: primordium_memory_game.py

  133, 133:         elif self.symbol == "star":
  134, 134:             # Draw a star
  135, 135:             center_x = self.x + self.width // 2
  136, 136:             center_y = self.y + self.height // 2
  137, 137:             points = []
  138, 138:             for i in range(5):
  139, 139:                 # Outer points
- 140     :                 angle = (2 * pygame.math.pi * i / 5) - pygame.math.pi / 2
+      140:                 angle = (2 * 3.14159 * i / 5) - 3.14159 / 2
  141, 141:                 points.append((
  142, 142:                     center_x + int(30 * pygame.math.cos(angle)),
  143, 143:                     center_y + int(30 * pygame.math.sin(angle))
  144, 144:                 ))
  145, 145:                 # Inner points
- 146     :                 angle += pygame.math.pi / 5
+      146:                 angle += 3.14159 / 5
  147, 147:                 points.append((
  148, 148:                     center_x + int(15 * pygame.math.cos(angle)),
  149, 149:                     center_y + int(15 * pygame.math.sin(angle))
  150, 150:                 ))

Updating: primordium_memory_game.py

 ⋮
 ● Completed in 0.3s



🛠️  Using tool: fs_write (trusted)
 ⋮
 ● Path: primordium_memory_game.py

  160, 160:         elif self.symbol == "sun":
  161, 161:             # Draw a sun
  162, 162:             pygame.draw.circle(surface, YELLOW,
  163, 163:                               (self.x + self.width // 2, self.y + self.height // 2), 25)
  164, 164:             for i in range(8):
- 165     :                 angle = 2 * pygame.math.pi * i / 8
+      165:                 angle = 2 * 3.14159 * i / 8
  166, 166:                 start_x = self.x + self.width // 2 + int(25 * pygame.math.cos(angle))
  167, 167:                 start_y = self.y + self.height // 2 + int(25 * pygame.math.sin(angle))
  168, 168:                 end_x = self.x + self.width // 2 + int(35 * pygame.math.cos(angle))
  169, 169:                 end_y = self.y + self.height // 2 + int(35 * pygame.math.sin(angle))
  170, 170:                 pygame.draw.line(surface, YELLOW, (start_x, start_y), (end_x, end_y), 3)

Updating: primordium_memory_game.py

 ⋮
 ● Completed in 0.5s



🛠️  Using tool: fs_write (trusted)
 ⋮
 ● Path: primordium_memory_game.py

  123, 123:         elif self.symbol == "spiral":
  124, 124:             # Draw a spiral (simplified)
  125, 125:             center_x = self.x + self.width // 2
  126, 126:             center_y = self.y + self.height // 2
  127, 127:             for i in range(0, 80, 5):
  128, 128:                 angle = 0.1 * i
- 129     :                 x = center_x + int(i/3 * pygame.math.Vector2(1, 0).rotate(angle).x)
- 130     :                 y = center_y + int(i/3 * pygame.math.Vector2(1, 0).rotate(angle).y)
+      129:                 x = center_x + int(i/3 * math.cos(angle))
+      130:                 y = center_y + int(i/3 * math.sin(angle))
  131, 131:                 pygame.draw.circle(surface, ORANGE, (x, y), 3)

Updating: primordium_memory_game.py

 ⋮
 ● Completed in 0.3s



🛠️  Using tool: fs_write (trusted)
 ⋮
 ● Path: primordium_memory_game.py

  1, 1: import pygame
  2, 2: import random
  3, 3: import sys
  4, 4: import time
+    5: import math
  5, 6: from pygame.locals import *

Updating: primordium_memory_game.py

 ⋮
 ● Completed in 0.4s



🛠️  Using tool: execute_bash (trusted)
 ⋮
 ● I will run the following shell command:
cd /mnt/c/Users/Jeet\ soni/ && source memory_game_env/bin/activate && python primordium_memory_game.py
 ⋮
 ↳ Purpose: Running the fixed Primordium Memory Game

pygame 2.6.1 (SDL 2.28.4, Python 3.12.3)
Hello from the pygame community. https://www.pygame.org/contribute.html
Traceback (most recent call last):
  File "/mnt/c/Users/Jeet soni/primordium_memory_game.py", line 367, in <module>
    game.run()
  File "/mnt/c/Users/Jeet soni/primordium_memory_game.py", line 362, in run
    self.draw()
  File "/mnt/c/Users/Jeet soni/primordium_memory_game.py", line 303, in draw
    card.draw(self.screen)
  File "/mnt/c/Users/Jeet soni/primordium_memory_game.py", line 67, in draw
    self.draw_symbol(surface)
  File "/mnt/c/Users/Jeet soni/primordium_memory_game.py", line 143, in draw_symbol
    center_x + int(30 * pygame.math.cos(angle)),
                        ^^^^^^^^^^^^^^^
AttributeError: module 'pygame.math' has no attribute 'cos'

 ⋮
 ● Completed in 9.99s



🛠️  Using tool: fs_write (trusted)
 ⋮
 ● Path: primordium_memory_game.py

  134, 134:         elif self.symbol == "star":
  135, 135:             # Draw a star
  136, 136:             center_x = self.x + self.width // 2
  137, 137:             center_y = self.y + self.height // 2
  138, 138:             points = []
  139, 139:             for i in range(5):
  140, 140:                 # Outer points
- 141     :                 angle = (2 * 3.14159 * i / 5) - 3.14159 / 2
+      141:                 angle = (2 * math.pi * i / 5) - math.pi / 2
  142, 142:                 points.append((
- 143     :                     center_x + int(30 * pygame.math.cos(angle)),
- 144     :                     center_y + int(30 * pygame.math.sin(angle))
+      143:                     center_x + int(30 * math.cos(angle)),
+      144:                     center_y + int(30 * math.sin(angle))
  145, 145:                 ))
  146, 146:                 # Inner points
- 147     :                 angle += 3.14159 / 5
+      147:                 angle += math.pi / 5
  148, 148:                 points.append((
- 149     :                     center_x + int(15 * pygame.math.cos(angle)),
- 150     :                     center_y + int(15 * pygame.math.sin(angle))
+      149:                     center_x + int(15 * math.cos(angle)),
+      150:                     center_y + int(15 * math.sin(angle))
  151, 151:                 ))

Updating: primordium_memory_game.py

 ⋮
 ● Completed in 0.5s



🛠️  Using tool: fs_write (trusted)
 ⋮
 ● Path: primordium_memory_game.py

  161, 161:         elif self.symbol == "sun":
  162, 162:             # Draw a sun
  163, 163:             pygame.draw.circle(surface, YELLOW,
  164, 164:                               (self.x + self.width // 2, self.y + self.height // 2), 25)
  165, 165:             for i in range(8):
- 166     :                 angle = 2 * 3.14159 * i / 8
- 167     :                 start_x = self.x + self.width // 2 + int(25 * pygame.math.cos(angle))
- 168     :                 start_y = self.y + self.height // 2 + int(25 * pygame.math.sin(angle))
- 169     :                 end_x = self.x + self.width // 2 + int(35 * pygame.math.cos(angle))
- 170     :                 end_y = self.y + self.height // 2 + int(35 * pygame.math.sin(angle))
+      166:                 angle = 2 * math.pi * i / 8
+      167:                 start_x = self.x + self.width // 2 + int(25 * math.cos(angle))
+      168:                 start_y = self.y + self.height // 2 + int(25 * math.sin(angle))
+      169:                 end_x = self.x + self.width // 2 + int(35 * math.cos(angle))
+      170:                 end_y = self.y + self.height // 2 + int(35 * math.sin(angle))
  171, 171:                 pygame.draw.line(surface, YELLOW, (start_x, start_y), (end_x, end_y), 3)

Updating: primordium_memory_game.py

 ⋮
 ● Completed in 0.4s



🛠️  Using tool: execute_bash (trusted)
 ⋮
 ● I will run the following shell command:
cd /mnt/c/Users/Jeet\ soni/ && source memory_game_env/bin/activate && python primordium_memory_game.py
 ⋮
 ↳ Purpose: Running the fixed Primordium Memory Game