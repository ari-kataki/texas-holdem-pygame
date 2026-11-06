import pygame
import sys
import random
from enum import Enum
from itertools import combinations

pygame.init()

#  WINDOW

W      = 1400
H      = 800
FPS    = 60
CX     = W // 2
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Diamond Casino - Ultimate Texas Hold'em")
clock  = pygame.time.Clock()

CARD_W = 68
CARD_H = 96

Y_TITLE       = 21
Y_DEALER_LBL  = 57
Y_DEALER_CARD = 74
Y_COM_LBL     = 183
Y_COM_CARD    = 198
Y_PLAYER      = 308
PANEL_H       = 182
Y_ACTION      = 498


#  COLORS

FELT = ( 34, 100,  50)
FELT_D = ( 20,  70,  35)
FELT_L = ( 55, 130,  70)
RAIL = ( 90,  50,  10)
PANEL = (  8,  32,  16)
CARD_BG = (253, 249, 239)
C_RED = (200,  20,  20)
C_BLK = ( 15,  15,  15)
GOLD = (212, 175,  55)
GOLD_D = (140, 110,  15)
WHITE = (245, 245, 245)
GRAY = (130, 130, 130)
GRAY_D = ( 50,  50,  50)
GRAY_L = (180, 180, 180)
BTN_G = ( 42, 140,  65)
BTN_R = (165,  42,  42)
BTN_B = ( 38,  90, 190)
BTN_GD = (160, 130,  18)
BTN_GR = ( 80,  80,  80)
HI = (255, 215,   0)


#  FONTS

def loadFont(names, size, bold=False):
    for name in names:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except:
            pass
    return pygame.font.SysFont("arial", size, bold=bold)

SUIT_FONTS = ["Apple Symbols", "Arial Unicode MS",
             "Segoe UI Symbol","DejaVu Sans", "FreeSans", "unifont"]

F_TITLE = loadFont(["Georgia", "Times New Roman"], 34, bold=True)
F_BIG = loadFont(["Georgia", "Times New Roman"], 24, bold=True)
F_MED = loadFont(["Arial", "Helvetica"], 19)
F_MDB = loadFont(["Arial", "Helvetica"], 19, bold=True)
F_SM = loadFont(["Arial", "Helvetica"], 15)
F_SMB = loadFont(["Arial", "Helvetica"], 15, bold=True)
F_TINY = loadFont(["Arial", "Helvetica"], 12)
F_CVAL = loadFont(["Georgia", "Arial"], 17, bold=True)
F_SSML = loadFont(SUIT_FONTS, 13)
F_SLRG = loadFont(SUIT_FONTS, 28)


#  ENUMS

class Suit(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4

class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class HandRank(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

class GameState(Enum):
    SETUP_NUM = 1
    SETUP_NAME = 2
    SETUP_CHIPS = 3
    MENU = 4
    ANTE = 5
    TRIPS = 6
    PREFLOP = 7
    FLOP = 8
    TURN_RIVER = 9
    SHOWDOWN = 10
    RESULTS = 11
    GAME_OVER = 12


#  CARD DATA

SUIT_SYMBOL = {
    Suit.HEARTS:   "\u2665",
    Suit.DIAMONDS: "\u2666",
    Suit.CLUBS:    "\u2663",
    Suit.SPADES:   "\u2660"
}

SUIT_COLOR = {
    Suit.HEARTS: C_RED,
    Suit.DIAMONDS: C_RED,
    Suit.CLUBS: C_BLK,
    Suit.SPADES: C_BLK
}

RANK_SYMBOL = {
    Rank.TWO: "2", Rank.THREE: "3", Rank.FOUR: "4",
    Rank.FIVE: "5", Rank.SIX: "6", Rank.SEVEN: "7",
    Rank.EIGHT: "8", Rank.NINE: "9", Rank.TEN: "T",
    Rank.JACK: "J", Rank.QUEEN: "Q", Rank.KING: "K",
    Rank.ACE: "A"
}

HAND_NAME = {
    HandRank.HIGH_CARD: "High Card",
    HandRank.ONE_PAIR: "One Pair",
    HandRank.TWO_PAIR: "Two Pair",
    HandRank.THREE_OF_A_KIND: "Three of a Kind",
    HandRank.STRAIGHT: "Straight",
    HandRank.FLUSH: "Flush",
    HandRank.FULL_HOUSE: "Full House",
    HandRank.FOUR_OF_A_KIND: "Four of a Kind",
    HandRank.STRAIGHT_FLUSH: "Straight Flush",
    HandRank.ROYAL_FLUSH: "Royal Flush"
}


#  PAYOUT TABLES

PAYOUT_BLIND = {
    HandRank.ROYAL_FLUSH: 500,
    HandRank.STRAIGHT_FLUSH: 50,
    HandRank.FOUR_OF_A_KIND: 10,
    HandRank.FULL_HOUSE: 3,
    HandRank.FLUSH: 2,
    HandRank.STRAIGHT: 1
}

PAYOUT_TRIPS = {
    HandRank.ROYAL_FLUSH: 50,
    HandRank.STRAIGHT_FLUSH: 40,
    HandRank.FOUR_OF_A_KIND: 30,
    HandRank.FULL_HOUSE: 8,
    HandRank.FLUSH: 7,
    HandRank.STRAIGHT: 4,
    HandRank.THREE_OF_A_KIND: 3
}

CHIPS_MIN = 20

#  CARD CLASS

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

#  DECK

class Deck:
    def __init__(self):
        self.cards = []
        self.shuffle()

    def shuffle(self):
        self.cards = [Card(r, s) for r in Rank for s in Suit]
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) == 0:
            self.shuffle()
        return self.cards.pop()


#  HAND EVALUATOR

def evaluateHand(cards):
    best = None
    for combo in combinations(cards, 5):
        result = evaluateFive(list(combo))
        if best is None or compareHands(result, best) == 1:
            best = result
    return best

def evaluateFive(cards):
    values  = sorted([c.rank.value for c in cards], reverse=True)
    isFlush = len(set(c.suit for c in cards)) == 1
    isStraight = checkStraight(values)

    if isStraight and values == [14, 5, 4, 3, 2]:
        values = [5, 4, 3, 2, 1]

    if isFlush and values == [14, 13, 12, 11, 10]:
        return (HandRank.ROYAL_FLUSH, values)

    if isFlush and isStraight:
        return (HandRank.STRAIGHT_FLUSH, values)

    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1

    groups  = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    freqs   = [g[1] for g in groups]
    ordered = [g[0] for g in groups]

    if freqs[0] == 4:
        return (HandRank.FOUR_OF_A_KIND, ordered)

    if freqs[0] == 3 and len(freqs) > 1 and freqs[1] == 2:
        return (HandRank.FULL_HOUSE, ordered)

    if isFlush:
        return (HandRank.FLUSH, values)

    if isStraight:
        return (HandRank.STRAIGHT, values)

    if freqs[0] == 3:
        return (HandRank.THREE_OF_A_KIND, ordered)

    if freqs[0] == 2 and len(freqs) > 1 and freqs[1] == 2:
        return (HandRank.TWO_PAIR, ordered)

    if freqs[0] == 2:
        return (HandRank.ONE_PAIR, ordered)

    return (HandRank.HIGH_CARD, values)

def checkStraight(values):
    if values[0] - values[4] == 4 and len(set(values)) == 5:
        return True
    if values == [14, 5, 4, 3, 2]:
        return True
    return False

def compareHands(hand1, hand2):
    r1, k1 = hand1
    r2, k2 = hand2
    if r1.value > r2.value:
        return 1
    if r1.value < r2.value:
        return -1
    for a, b in zip(k1, k2):
        if a > b:
            return 1
        if a < b:
            return -1
    return 0


#  DRAW UTILITIES

def drawRoundedRect(surf, color, rect, radius=8, alpha=255):
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, (color[0], color[1], color[2], alpha),
                     (0, 0, rect[2], rect[3]), border_radius=radius)
    surf.blit(s, (rect[0], rect[1]))

def drawTextCenter(surf, text, font, color, cx, cy):
    rendered = font.render(str(text), True, color)
    surf.blit(rendered, (cx - rendered.get_width() // 2,
                         cy - rendered.get_height() // 2))

def drawCard(surf, card, x, y, hidden=False):
    rect = pygame.Rect(x, y, CARD_W, CARD_H)

    if hidden:
        pygame.draw.rect(surf, GOLD_D, rect, border_radius=7)
        pygame.draw.rect(surf, GOLD,   rect.inflate(-4, -4),   border_radius=6)
        pygame.draw.rect(surf, GOLD_D, rect.inflate(-14, -14), border_radius=4)
        pygame.draw.rect(surf, WHITE,  rect, 1, border_radius=7)
        return

    # shadow
    shadow = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 60), (0, 0, CARD_W, CARD_H), border_radius=7)
    surf.blit(shadow, (x + 3, y + 3))

    # card face
    pygame.draw.rect(surf, CARD_BG, rect, border_radius=7)
    pygame.draw.rect(surf, (155, 155, 155), rect, 1, border_radius=7)

    color  = SUIT_COLOR[card.suit]
    symbol = SUIT_SYMBOL[card.suit]
    value  = RANK_SYMBOL[card.rank]

    # top-left:rank value
    vr = F_CVAL.render(value, True, color)
    surf.blit(vr, (x + 5, y + 4))

    # top-left:small suit symbol
    sr = F_SSML.render(symbol, True, color)
    surf.blit(sr, (x + 5, y + 4 + vr.get_height() + 1))

    # center:large suit symbol
    lr = F_SLRG.render(symbol, True, color)
    surf.blit(lr, (x + CARD_W // 2 - lr.get_width() // 2,
                   y + CARD_H // 2 - lr.get_height() // 2))

    # bottom-right:rotated rank + symbol
    vb = pygame.transform.rotate(F_CVAL.render(value, True, color), 180)
    sb = pygame.transform.rotate(F_SSML.render(symbol, True, color), 180)
    surf.blit(vb, (x + CARD_W - vb.get_width() - 5,
                   y + CARD_H - vb.get_height() - sb.get_height() - 5))
    surf.blit(sb, (x + CARD_W - sb.get_width() - 5,
                   y + CARD_H - sb.get_height() - 4))

def drawSlot(surf, x, y):
    r = pygame.Rect(x, y, CARD_W, CARD_H)
    pygame.draw.rect(surf, FELT_D, r, border_radius=7)
    pygame.draw.rect(surf, FELT_L, r, 1, border_radius=7)

#  BUTTON CLASS

class Button:
    def __init__(self, x, y, w, h, label, color=BTN_G):
        self.rect   = pygame.Rect(x, y, w, h)
        self.label  = label
        self.color  = color
        self.active = True
        self.hover  = False

    def draw(self, surf):
        if not self.active:
            c = BTN_GR
        elif self.hover:
            c = tuple(min(255, v + 40) for v in self.color)
        else:
            c = self.color
        pygame.draw.rect(surf, c, self.rect, border_radius=9)
        pygame.draw.rect(surf, WHITE, self.rect, 1, border_radius=9)
        t = F_MDB.render(self.label, True, WHITE)
        surf.blit(t, (self.rect.centerx - t.get_width() // 2,
                      self.rect.centery - t.get_height() // 2))

    def update(self, pos):
        self.hover = self.rect.collidepoint(pos) and self.active

    def clicked(self, pos):
        return self.rect.collidepoint(pos) and self.active


#  INPUT BOX CLASS

class InputBox:
    def __init__(self, x, y, w, h, placeholder="", numbers_only=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.numbers_only = numbers_only

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key not in (pygame.K_RETURN, pygame.K_TAB):
                ch = event.unicode
                if self.numbers_only and ch.isdigit():
                    self.text += ch
                elif not self.numbers_only and ch.isprintable():
                    self.text += ch

    def draw(self, surf):
        border = GOLD if self.active else GRAY
        pygame.draw.rect(surf, PANEL, self.rect, border_radius=7)
        pygame.draw.rect(surf, border, self.rect, 2, border_radius=7)
        display = self.text if self.text else self.placeholder
        color   = WHITE if self.text else GRAY
        t = F_MED.render(display, True, color)
        surf.blit(t, (self.rect.x + 10,
                      self.rect.centery - t.get_height() // 2))
        if self.active and pygame.time.get_ticks() % 1000 < 500:
            off = F_MED.render(self.text, True, WHITE).get_width() if self.text else 0
            pygame.draw.line(surf, WHITE,
                             (self.rect.x + 10 + off, self.rect.y + 6),
                             (self.rect.x + 10 + off, self.rect.bottom - 6), 2)

    def getValue(self):
        if self.numbers_only:
            return int(self.text) if self.text else 0
        return self.text.strip()

#  GAME CLASS
class Game:

    def newPlayer(self, name, chips):
        return {
            "name":   name,
            "chips":  chips,
            "cards":  [],
            "ante":   0,
            "blind":  0,
            "play":   0,
            "trips":  0,
            "mult":   0,
            "folded": False,
            "out":    chips < CHIPS_MIN,
            "result": None
        }

    def __init__(self):
        self.state      = GameState.SETUP_NUM
        self.players    = []
        self.deck       = Deck()
        self.dealer     = []
        self.community  = []
        self.turn       = 0
        self.setup_idx  = 0
        self.num_target = 0
        self.message    = ""
        self.results    = []
        self.show_rules = False
        self.show_rank  = False
        self.tmp_name   = ""

       
        self.inp_name  = InputBox(CX-190, 372, 380, 46, placeholder="e.g. Marco")
        self.inp_chips = InputBox(CX-190, 372, 380, 46,
                                  placeholder="e.g. 5000", numbers_only=True)
        self.btn_num   = [Button(CX-165+i*130, 372, 110, 52, str(i+1), BTN_B)
                          for i in range(3)]
        self.btn_confirm = Button(CX-115, 442, 230, 48, "CONFIRM  >", BTN_GD)

        # Ante chip buttons
        self.bet_amount = 10
        bw  = 84
        bg  = 10
        bx0 = CX - (8 * bw + 7 * bg) // 2
        chip_values = [(-1000, BTN_R), (-200, BTN_R), (-100, BTN_R), (-20, BTN_R),
                       ( +20, BTN_G), ( +100, BTN_G), (+200, BTN_G), (+1000, BTN_G)]
        self.bet_btns = [
            Button(bx0 + i*(bw+bg), Y_ACTION+120, bw, 40,
                   ("+" if v > 0 else "") + str(v), c)
            for i, (v, c) in enumerate(chip_values)
        ]
        self.btn_bet_ok = Button(CX-120, Y_ACTION+178, 240, 46,
                                 "CONFIRM BET  >", BTN_GD)

        # Trips buttons
        self.trips_amount = 5
        self.trips_mode   = False
        self.btn_trips_yes = Button(CX-230, Y_ACTION+110, 200, 48, "YES - TRIPS", BTN_G)
        self.btn_trips_no  = Button(CX+ 30, Y_ACTION+110, 200, 48, "NO TRIPS",    BTN_R)
        tx0 = CX - (8*bw + 7*bg) // 2
        self.trips_btns = [
            Button(tx0 + i*(bw+bg), Y_ACTION+120, bw, 40,
                   ("+" if v > 0 else "") + str(v), c)
            for i, (v, c) in enumerate(chip_values)
        ]

        # Action buttons 
        ay = Y_ACTION + 148
        self.btn_preflop = [
            Button(CX-370, ay, 155, 48, "CHECK",    BTN_B),
            Button(CX-195, ay, 155, 48, "RAISE x3", BTN_GD),
            Button(CX- 20, ay, 155, 48, "RAISE x4", BTN_G),
            Button(CX+155, ay, 120, 48, "FOLD",     BTN_R),
        ]
        self.btn_flop = [
            Button(CX-195, ay, 175, 48, "CHECK",    BTN_B),
            Button(CX+ 20, ay, 175, 48, "RAISE x2", BTN_G),
        ]
        self.btn_river = [
            Button(CX-195, ay, 175, 48, "FOLD",    BTN_R),
            Button(CX+ 20, ay, 175, 48, "CALL x1", BTN_G),
        ]

        # Menu buttons
        self.btn_menu = [
            Button(CX-170, 308, 340, 52, "NEW HAND", BTN_G),
            Button(CX-170, 374, 340, 52, "LEADERBOARD", BTN_B),
            Button(CX-170, 440, 340, 52, "PAYOUT TABLE", BTN_GD),
            Button(CX-170, 506, 340, 52, "QUIT", BTN_R),
        ]

        # continue button
        self.btn_continue = Button(CX-130, Y_ACTION+198, 260, 46,
                                   "CONTINUE  >", BTN_G)

 
    #  MAIN LOOP

    def run(self):
        while True:
            events = pygame.event.get()
            for ev in events:
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    self.show_rules = False
                    self.show_rank  = False

            pos = pygame.mouse.get_pos()
            self.updateHovers(pos)
            self.handleEvents(events, pos)
            self.drawAll()
            pygame.display.flip()
            clock.tick(FPS)

    def updateHovers(self, pos):
        all_buttons = (self.btn_num + self.bet_btns + self.trips_btns +
                       self.btn_preflop + self.btn_flop + self.btn_river +
                       self.btn_menu)
        for b in all_buttons:
            b.update(pos)
        self.btn_confirm.update(pos)
        self.btn_bet_ok.update(pos)
        self.btn_trips_yes.update(pos)
        self.btn_trips_no.update(pos)
        self.btn_continue.update(pos)

    #  EVENTS

    def handleEvents(self, events, pos):
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                self.inp_name.handle(ev)
                self.inp_chips.handle(ev)
                if ev.key == pygame.K_RETURN:
                    if self.state == GameState.SETUP_NAME:
                        self.confirmName()
                    elif self.state == GameState.SETUP_CHIPS:
                        self.confirmChips()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                self.inp_name.handle(ev)
                self.inp_chips.handle(ev)

            if ev.type == pygame.MOUSEBUTTONUP:
                self.handleClick(pos)

    def handleClick(self, pos):
        s = self.state

        if self.show_rules or self.show_rank:
            self.show_rules = False
            self.show_rank  = False
            return

        if s == GameState.SETUP_NUM:
            for i, b in enumerate(self.btn_num):
                if b.clicked(pos):
                    self.num_target = i + 1
                    self.setup_idx  = 0
                    self.players    = []
                    self.inp_name.text = ""
                    self.inp_name.active = True
                    self.state = GameState.SETUP_NAME

        elif s == GameState.SETUP_NAME:
            if self.btn_confirm.clicked(pos):
                self.confirmName()

        elif s == GameState.SETUP_CHIPS:
            if self.btn_confirm.clicked(pos):
                self.confirmChips()

        elif s == GameState.MENU:
            if self.btn_menu[0].clicked(pos): self.startHand()
            if self.btn_menu[1].clicked(pos): self.show_rank  = True
            if self.btn_menu[2].clicked(pos): self.show_rules = True
            if self.btn_menu[3].clicked(pos): pygame.quit(); sys.exit()

        elif s == GameState.ANTE:
            for b in self.bet_btns:
                if b.clicked(pos):
                    delta = int(b.label.replace("+", ""))
                    p  = self.players[self.turn]
                    mx = max(10, p["chips"] // 2)
                    self.bet_amount = max(10, min(mx, self.bet_amount + delta))
            if self.btn_bet_ok.clicked(pos) and self.bet_amount >= 10:
                p = self.players[self.turn]
                p["ante"]   = self.bet_amount
                p["blind"]  = self.bet_amount
                p["chips"] -= self.bet_amount * 2
                self.trips_mode   = False
                self.trips_amount = 5
                self.state = GameState.TRIPS

        elif s == GameState.TRIPS:
            if self.btn_trips_yes.clicked(pos) and not self.trips_mode:
                self.trips_mode = True
            if self.trips_mode:
                for b in self.trips_btns:
                    if b.clicked(pos):
                        delta = int(b.label.replace("+", ""))
                        p = self.players[self.turn]
                        self.trips_amount = max(5, min(p["chips"],
                                                       self.trips_amount + delta))
                if self.btn_bet_ok.clicked(pos) and self.trips_amount >= 5:
                    p = self.players[self.turn]
                    p["trips"]  = self.trips_amount
                    p["chips"] -= self.trips_amount
                    self.nextAnte()
            elif self.btn_trips_no.clicked(pos):
                self.nextAnte()

        elif s == GameState.PREFLOP:
            p = self.players[self.turn]
            if self.btn_preflop[0].clicked(pos):
                p["mult"] = 0
                self.nextPreflop()
            elif self.btn_preflop[1].clicked(pos) and p["chips"] >= p["ante"] * 3:
                p["play"]   = p["ante"] * 3
                p["chips"] -= p["play"]
                p["mult"]   = 3
                self.nextPreflop()
            elif self.btn_preflop[2].clicked(pos) and p["chips"] >= p["ante"] * 4:
                p["play"]   = p["ante"] * 4
                p["chips"] -= p["play"]
                p["mult"]   = 4
                self.nextPreflop()
            elif self.btn_preflop[3].clicked(pos):
                p["folded"] = True
                self.nextPreflop()

        elif s == GameState.FLOP:
            p = self.players[self.turn]
            if self.btn_flop[0].clicked(pos):
                p["mult"] = 0
                self.nextFlop()
            elif self.btn_flop[1].clicked(pos) and p["chips"] >= p["ante"] * 2:
                p["play"]   = p["ante"] * 2
                p["chips"] -= p["play"]
                p["mult"]   = 2
                self.nextFlop()

        elif s == GameState.TURN_RIVER:
            p = self.players[self.turn]
            if self.btn_river[0].clicked(pos):
                p["folded"] = True
                self.nextRiver()
            elif self.btn_river[1].clicked(pos) and p["chips"] >= p["ante"]:
                p["play"]   = p["ante"]
                p["chips"] -= p["play"]
                p["mult"]   = 1
                self.nextRiver()

        elif s == GameState.SHOWDOWN:
            if self.btn_continue.clicked(pos):
                self.calcResults()
                self.state = GameState.RESULTS

        elif s == GameState.RESULTS:
            if self.btn_continue.clicked(pos):
                active = [p for p in self.players if not p["out"]]
                if not active:
                    self.state = GameState.GAME_OVER
                else:
                    self.state = GameState.MENU

        elif s == GameState.GAME_OVER:
            if self.btn_continue.clicked(pos):
                self.__init__()

    #  SETUP HELPERS
   
    def confirmName(self):
        name = self.inp_name.getValue()
        if not name:
            name = "Player " + str(self.setup_idx + 1)
        self.tmp_name = name
        self.inp_chips.text = ""
        self.inp_name.active = False
        self.inp_chips.active = True
        self.state = GameState.SETUP_CHIPS

    def confirmChips(self):
        chips = self.inp_chips.getValue()
        if chips < 500 or chips > 1000000:
            self.message = "Enter an amount between $500 and $1,000,000"
            return
        self.players.append(self.newPlayer(self.tmp_name, chips))
        self.setup_idx += 1
        self.inp_chips.active = False
        if self.setup_idx >= self.num_target:
            self.state = GameState.MENU
        else:
            self.inp_name.text = ""
            self.inp_name.active = True
            self.state = GameState.SETUP_NAME
        self.message = ""


    #  GAME FLOW
 
    def startHand(self):
        self.deck      = Deck()
        self.dealer    = []
        self.community = []
        for p in self.players:
            p["cards"]  = []
            p["ante"]   = 0
            p["blind"]  = 0
            p["play"]   = 0
            p["trips"]  = 0
            p["mult"]   = 0
            p["folded"] = False
            p["result"] = None
            p["out"]    = p["chips"] < CHIPS_MIN
        self.turn         = self.firstActive()
        self.bet_amount   = 10
        self.trips_amount = 5
        self.trips_mode   = False
        self.state        = GameState.ANTE

    def firstActive(self):
        for i in range(len(self.players)):
            if not self.players[i]["out"]:
                return i
        return 0

    def nextAnte(self):
        self.trips_mode   = False
        self.trips_amount = 5
        nxt = self.turn + 1
        while nxt < len(self.players):
            if not self.players[nxt]["out"]:
                self.turn       = nxt
                self.bet_amount = 10
                self.state      = GameState.ANTE
                return
            nxt += 1
        self.dealHoleCards()

    def dealHoleCards(self):
        for p in self.players:
            if not p["out"]:
                p["cards"] = [self.deck.deal(), self.deck.deal()]
        self.dealer = [self.deck.deal(), self.deck.deal()]
        self.turn   = self.firstActive()
        self.state  = GameState.PREFLOP

    def nextPreflop(self):
        nxt = self.turn + 1
        while nxt < len(self.players):
            p = self.players[nxt]
            if not p["out"] and not p["folded"]:
                self.turn = nxt
                return
            nxt += 1
        for i in range(3):
            self.community.append(self.deck.deal())
        self.turn = self.firstUnraised()
        if self.turn == -1:
            self.dealTurnRiver()
        else:
            self.state = GameState.FLOP

    def nextFlop(self):
        nxt = self.turn + 1
        while nxt < len(self.players):
            p = self.players[nxt]
            if not p["out"] and not p["folded"] and p["mult"] == 0:
                self.turn = nxt
                return
            nxt += 1
        self.dealTurnRiver()

    def dealTurnRiver(self):
        while len(self.community) < 5:
            self.community.append(self.deck.deal())
        self.turn = self.firstUnraised()
        if self.turn == -1:
            self.state = GameState.SHOWDOWN
        else:
            self.state = GameState.TURN_RIVER

    def nextRiver(self):
        nxt = self.turn + 1
        while nxt < len(self.players):
            p = self.players[nxt]
            if not p["out"] and not p["folded"] and p["mult"] == 0:
                self.turn = nxt
                return
            nxt += 1
        self.state = GameState.SHOWDOWN

    def firstUnraised(self):
        for i in range(len(self.players)):
            p = self.players[i]
            if not p["out"] and not p["folded"] and p["mult"] == 0:
                return i
        return -1


    #  CALCULATE RESULTS

    def calcResults(self):
        comm    = self.community
        hand_d  = evaluateHand(self.dealer + comm)
        qualifies = hand_d[0].value >= HandRank.ONE_PAIR.value
        self.results = []

        for p in self.players:
            if p["out"]:
                continue

            if p["folded"]:
                gain = 0
                if p["trips"] > 0:
                    hand_f = evaluateHand(p["cards"] + comm)
                    if hand_f[0] in PAYOUT_TRIPS:
                        gain = p["trips"] * (PAYOUT_TRIPS[hand_f[0]] + 1)
                        p["chips"] += gain
                delta = gain - (p["ante"] + p["blind"] + p["trips"])
                p["result"] = {"outcome": "FOLD",
                               "delta": delta}
                self.results.append(
                    p["name"] + ": FOLD  " + ("+" if delta >= 0 else "-") +
                    "$" + str(abs(delta)))
                p["out"] = p["chips"] < CHIPS_MIN
                continue

            hand_p = evaluateHand(p["cards"] + comm)
            cmp    = compareHands(hand_p, hand_d)
            gain   = 0

            if cmp == 1:
                gain += p["play"] * 2
            elif cmp == 0:
                gain += p["play"]

            if qualifies:
                if cmp == 1:
                    gain += p["ante"] * 2
                elif cmp == 0:
                    gain += p["ante"]
            else:
                gain += p["ante"]

            if cmp == 1:
                if hand_p[0] in PAYOUT_BLIND:
                    gain += p["blind"] * (PAYOUT_BLIND[hand_p[0]] + 1)
                else:
                    gain += p["blind"]
            elif cmp == 0:
                gain += p["blind"]

            if p["trips"] > 0 and hand_p[0] in PAYOUT_TRIPS:
                gain += p["trips"] * (PAYOUT_TRIPS[hand_p[0]] + 1)

            p["chips"] += gain
            total_bet   = p["ante"] + p["blind"] + p["play"] + p["trips"]
            delta       = gain - total_bet

            if cmp == 1:
                tag = "WIN"
            elif cmp == 0:
                tag = "PUSH"
            else:
                tag = "LOSE"

            if delta >= 0:
                sign = "+"
            else:
                sign = ""

            p["result"] = {
                "outcome":     cmp,
                "delta":       delta,
                "hand":        HAND_NAME[hand_p[0]],
                "dealer_hand": HAND_NAME[hand_d[0]],
                "qualifies":   qualifies
            }
            self.results.append(
                p["name"] + "  [" + HAND_NAME[hand_p[0]] + "]  " +
                tag + "  " + sign + "$ " + str(delta))
            p["out"] = p["chips"] < CHIPS_MIN


    #  DRAW – MAIN
   
    def drawAll(self):
        screen.fill(FELT_D)
        self.drawBackground()

        s = self.state
        if   s == GameState.SETUP_NUM:   self.drawSetupNum()
        elif s == GameState.SETUP_NAME:  self.drawSetupName()
        elif s == GameState.SETUP_CHIPS: self.drawSetupChips()
        elif s == GameState.MENU:        self.drawMenu()
        elif s == GameState.ANTE:
            self.drawTable()
            self.drawAnte()
        elif s == GameState.TRIPS:
            self.drawTable()
            self.drawTrips()
        elif s == GameState.PREFLOP:
            self.drawTable()
            self.drawAction(self.btn_preflop, "PRE-FLOP")
        elif s == GameState.FLOP:
            self.drawTable()
            self.drawAction(self.btn_flop, "FLOP")
        elif s == GameState.TURN_RIVER:
            self.drawTable()
            self.drawAction(self.btn_river, "TURN & RIVER")
        elif s == GameState.SHOWDOWN:
            self.drawTable(showdown=True)
            self.drawShowdown()
        elif s == GameState.RESULTS:
            self.drawTable(showdown=True)
            self.drawResults()
        elif s == GameState.GAME_OVER:
            self.drawGameOver()

        if self.show_rules:
            self.drawRulesOverlay()
        if self.show_rank:
            self.drawRankOverlay()

    # background 
    def drawBackground(self):
        pygame.draw.ellipse(screen, FELT,  (46, 42, W-92, H-64))
        pygame.draw.ellipse(screen, RAIL,  (34, 30, W-68, H-40), 20)
        pygame.draw.ellipse(screen, GOLD,  (34, 30, W-68, H-40), 3)
        drawRoundedRect(screen, (0,0,0), (0, 0, W, 40), radius=0, alpha=185)
        drawTextCenter(screen,
                       "DIAMOND CASINO  -  ULTIMATE TEXAS HOLD'EM",
                       F_TITLE, GOLD, CX, Y_TITLE)

    # setup 
    def drawSetupNum(self):
        drawRoundedRect(screen, PANEL, (CX-290, 278, 580, 210), radius=16, alpha=228)
        pygame.draw.rect(screen, GOLD, (CX-290, 278, 580, 210), 2, border_radius=16)
        drawTextCenter(screen, "How many players?", F_BIG, GOLD, CX, 310)
        for b in self.btn_num:
            b.draw(screen)
        drawTextCenter(screen, "Solo  |  Duo  |  Trio",
                       F_SM, GRAY_L, CX, 450)

    def drawSetupName(self):
        drawRoundedRect(screen, PANEL, (CX-290, 270, 580, 240), radius=16, alpha=228)
        pygame.draw.rect(screen, GOLD, (CX-290, 270, 580, 240), 2, border_radius=16)
        drawTextCenter(screen,
                       "Player " + str(self.setup_idx+1) + " of " +
                       str(self.num_target) + "  -  Enter Name",
                       F_BIG, GOLD, CX, 306)
        drawTextCenter(screen, "Press ENTER or click CONFIRM",
                       F_TINY, GRAY, CX, 344)
        self.inp_name.draw(screen)
        self.btn_confirm.draw(screen)
        if self.message:
            drawTextCenter(screen, self.message, F_SM, BTN_R, CX, 510)

    def drawSetupChips(self):
        drawRoundedRect(screen, PANEL, (CX-290, 270, 580, 250), radius=16, alpha=228)
        pygame.draw.rect(screen, GOLD, (CX-290, 270, 580, 250), 2, border_radius=16)
        drawTextCenter(screen, "Starting Budget  -  " + self.tmp_name,
                       F_BIG, GOLD, CX, 306)
        drawTextCenter(screen, "min $500  |  max $1,000,000",
                       F_SM, GRAY, CX, 340)
        self.inp_chips.draw(screen)
        self.btn_confirm.draw(screen)
        if self.message:
            drawTextCenter(screen, self.message, F_SM, BTN_R, CX, 510)

    # ── menu ───────────────────────────────────────────────────
    def drawMenu(self):
        drawRoundedRect(screen, PANEL, (CX-230, 272, 460, 310), radius=16, alpha=218)
        pygame.draw.rect(screen, GOLD, (CX-230, 272, 460, 310), 2, border_radius=16)
        drawTextCenter(screen, "MAIN MENU", F_BIG, GOLD, CX, 296)
        y = 309
        for p in self.players:
            if not p["out"]:
                col = WHITE
                lbl = "$ " + str(p["chips"])
            else:
                col = BTN_R
                lbl = "ELIMINATED"
            drawTextCenter(screen, p["name"] + "  |  " + lbl, F_SM, col, CX, y)
            y += 19
        for b in self.btn_menu:
            b.draw(screen)

    # table 
    def drawTable(self, showdown=False):
        # Dealer area
        drawRoundedRect(screen, PANEL, (CX-120, Y_DEALER_LBL-13, 240, 26),
                        radius=6, alpha=190)
        drawTextCenter(screen, "DEALER", F_SMB, GOLD, CX, Y_DEALER_LBL)
        bx0 = CX - CARD_W - 6
        for i in range(2):
            x = bx0 + i * (CARD_W + 12)
            if i < len(self.dealer):
                drawCard(screen, self.dealer[i], x, Y_DEALER_CARD,
                         hidden=not showdown)
            else:
                drawSlot(screen, x, Y_DEALER_CARD)

        # Community cards
        drawRoundedRect(screen, PANEL, (CX-210, Y_COM_LBL-12, 420, 22),
                        radius=6, alpha=170)
        drawTextCenter(screen, "COMMUNITY CARDS", F_TINY, GRAY_L, CX, Y_COM_LBL)
        total_w = 5 * CARD_W + 4 * 12
        cx0 = CX - total_w // 2
        for i in range(5):
            x = cx0 + i * (CARD_W + 12)
            if i < len(self.community):
                drawCard(screen, self.community[i], x, Y_COM_CARD)
            else:
                drawSlot(screen, x, Y_COM_CARD)

        # Player panels
        n  = len(self.players)
        if n == 1:
            pw = 420
        elif n == 2:
            pw = 390
        else:
            pw = 348
        gap     = 28
        total_w = n * pw + (n - 1) * gap
        sx      = CX - total_w // 2
        for i in range(len(self.players)):
            p  = self.players[i]
            px = sx + i * (pw + gap)
            hl = (i == self.turn and
                  self.state not in (GameState.SHOWDOWN, GameState.RESULTS,
                                     GameState.MENU, GameState.GAME_OVER))
            self.drawPlayerPanel(p, px, Y_PLAYER, pw, PANEL_H, hl, showdown)

    def drawPlayerPanel(self, p, px, py, pw, ph, highlight, showdown):
        if highlight:
            border = GOLD
        elif not p["out"]:
            border = GRAY_D
        else:
            border = BTN_R

        if not p["out"]:
            alpha = 215
        else:
            alpha = 110

        drawRoundedRect(screen, PANEL, (px, py, pw, ph), radius=10, alpha=alpha)
        pygame.draw.rect(screen, border,
                         pygame.Rect(px, py, pw, ph), 2, border_radius=10)

        if highlight:
            name_col = HI
        else:
            name_col = WHITE
        drawTextCenter(screen, p["name"], F_MDB, name_col, px+pw//2, py+14)

        if p["chips"] > 0:
            chips_col = BTN_G
        else:
            chips_col = BTN_R
        drawTextCenter(screen, "$ " + str(p["chips"]),
                       F_SMB, chips_col, px+pw//2, py+33)

        badge_y = py + 52
        if p["folded"]:
            drawTextCenter(screen, "FOLD", F_SMB, BTN_R, px+pw//2, badge_y)
        elif p["out"]:
            drawTextCenter(screen, "ELIMINATED", F_SMB, BTN_R, px+pw//2, badge_y)
        elif p.get("result") and not p["folded"]:
            res     = p["result"]
            outcome = res.get("outcome")
            if outcome == 1:
                drawTextCenter(screen,
                               "WIN  +$ " + str(res["delta"]),
                               F_SMB, BTN_G, px+pw//2, badge_y)
            elif outcome == -1:
                drawTextCenter(screen,
                               "LOSE  $ " + str(res["delta"]),
                               F_SMB, BTN_R, px+pw//2, badge_y)
            elif outcome == 0:
                drawTextCenter(screen, "PUSH", F_SMB, HI, px+pw//2, badge_y)
            if "hand" in res:
                drawTextCenter(screen, res["hand"],
                               F_TINY, GRAY_L, px+pw//2, badge_y+16)

        reveal = showdown or highlight
        cx0 = px + pw//2 - CARD_W - 6
        cy  = py + 70
        for j in range(2):
            x = cx0 + j * (CARD_W + 12)
            if j < len(p["cards"]):
                drawCard(screen, p["cards"][j], x, cy, hidden=not reveal)
            else:
                drawSlot(screen, x, cy)

        bets = []
        if p["ante"]:  bets.append("A:$" + str(p["ante"]))
        if p["blind"]: bets.append("B:$" + str(p["blind"]))
        if p["play"]:  bets.append("P:$" + str(p["play"]))
        if p["trips"]: bets.append("T:$" + str(p["trips"]))
        if bets:
            drawTextCenter(screen, "  ".join(bets),
                           F_TINY, GRAY_L, px+pw//2, py+ph-9)

    # action panel base 
    def drawActionPanel(self, title, rows):
        pw = 780
        ph = 252
        drawRoundedRect(screen, PANEL, (CX-pw//2, Y_ACTION, pw, ph),
                        radius=14, alpha=240)
        pygame.draw.rect(screen, GOLD,
                         (CX-pw//2, Y_ACTION, pw, ph), 2, border_radius=14)
        drawTextCenter(screen, title, F_BIG, GOLD, CX, Y_ACTION+20)
        for i in range(len(rows)):
            text, col = rows[i]
            drawTextCenter(screen, text, F_SM, col, CX, Y_ACTION+46+i*20)

    def drawAnte(self):
        p  = self.players[self.turn]
        mx = max(10, p["chips"] // 2)
        self.drawActionPanel(
            p["name"] + "  -  Place your ANTE  (max $" + str(mx) + ")",
            [("ANTE: $" + str(self.bet_amount) +
              "    BLIND: $" + str(self.bet_amount) +
              "    TOTAL: $" + str(self.bet_amount*2), WHITE),
             ("Chips remaining: $" + str(p["chips"] - self.bet_amount*2), BTN_G)]
        )
        for b in self.bet_btns:
            b.draw(screen)
        self.btn_bet_ok.label  = "CONFIRM BET  >"
        self.btn_bet_ok.active = self.bet_amount >= 10
        self.btn_bet_ok.draw(screen)

    def drawTrips(self):
        p = self.players[self.turn]
        self.drawActionPanel(
            p["name"] + "  -  TRIPS side bet?",
            [("TRIPS always pays: 3 of a Kind 3:1 | Straight 4:1 | Flush 7:1 | Full 8:1 | Quads 30:1",
              GRAY_L)]
        )
        if not self.trips_mode:
            self.btn_trips_yes.draw(screen)
            self.btn_trips_no.draw(screen)
        else:
            drawTextCenter(screen,
                           "TRIPS amount: $" + str(self.trips_amount),
                           F_MED, WHITE, CX, Y_ACTION+96)
            for b in self.trips_btns:
                b.draw(screen)
            self.btn_bet_ok.label  = "CONFIRM TRIPS  >"
            self.btn_bet_ok.active = self.trips_amount >= 5
            self.btn_bet_ok.draw(screen)

    def drawAction(self, buttons, phase):
        p = self.players[self.turn]
        if p["cards"]:
            cards_str = "   ".join(
                RANK_SYMBOL[c.rank] + SUIT_SYMBOL[c.suit]
                for c in p["cards"]
            )
        else:
            cards_str = "-"
        self.drawActionPanel(
            p["name"] + "  -  " + phase,
            [("Your hand: " + cards_str, WHITE),
             ("Chips: $" + str(p["chips"]) +
              "    Ante: $" + str(p["ante"]) +
              "    Blind: $" + str(p["blind"]), GRAY_L)]
        )
        for b in buttons:
            b.draw(screen)

    def drawShowdown(self):
        hand_d = None
        if self.dealer and self.community:
            hand_d = evaluateHand(self.dealer + self.community)
        if hand_d:
            q = hand_d[0].value >= HandRank.ONE_PAIR.value
            if q:
                q_str = "Dealer: " + HAND_NAME[hand_d[0]] + "  -  QUALIFIES"
                q_col = BTN_G
            else:
                q_str = "Dealer: " + HAND_NAME[hand_d[0]] + "  -  DOES NOT QUALIFY"
                q_col = BTN_R
        else:
            q_str = ""
            q_col = WHITE
        self.drawActionPanel(
            "SHOWDOWN  -  Final Reveal",
            [(q_str, q_col),
             ("All cards revealed. Click to calculate results.", WHITE)]
        )
        self.btn_continue.label = "CALCULATE RESULTS  >"
        self.btn_continue.draw(screen)

    def drawResults(self):
        self.drawActionPanel("HAND RESULTS", [])
        for i in range(len(self.results)):
            line = self.results[i]
            if "WIN" in line or "+$" in line:
                col = BTN_G
            elif "PUSH" in line:
                col = HI
            else:
                col = BTN_R
            drawTextCenter(screen, line, F_SM, col, CX, Y_ACTION+46+i*22)
        self.btn_continue.label = "CONTINUE  >"
        self.btn_continue.draw(screen)

    # game over 
    def drawGameOver(self):
        self.drawBackground()
        drawRoundedRect(screen, PANEL, (CX-330, 196, 660, 390), radius=18, alpha=238)
        pygame.draw.rect(screen, BTN_R,
                         (CX-330, 196, 660, 390), 2, border_radius=18)
        drawTextCenter(screen, "GAME OVER", F_TITLE, BTN_R, CX, 238)
        drawTextCenter(screen, "All players have been eliminated.",
                       F_MED, WHITE, CX, 280)
        ordered = sorted(self.players, key=lambda p: p["chips"], reverse=True)
        medals  = ["1st", "2nd", "3rd"]
        for i in range(len(ordered)):
            p = ordered[i]
            if i == 0:
                col = HI
            else:
                col = GRAY_L
            if p["chips"] < CHIPS_MIN:
                lbl = "ELIMINATED"
            else:
                lbl = "$ " + str(p["chips"])
            if i < 3:
                m = medals[i]
            else:
                m = "  "
            drawTextCenter(screen, m + "  " + p["name"] + "    " + lbl,
                           F_MED, col, CX, 330+i*46)
        self.btn_continue.label  = "PLAY AGAIN  >"
        self.btn_continue.rect.topleft = (CX-130, 520)
        self.btn_continue.draw(screen)

    # overlays 
    def drawRulesOverlay(self):
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 215))
        screen.blit(ov, (0, 0))
        drawRoundedRect(screen, PANEL, (CX-370, 52, 740, 630), radius=16, alpha=250)
        pygame.draw.rect(screen, GOLD,
                         (CX-370, 52, 740, 630), 2, border_radius=16)
        drawTextCenter(screen, "PAYOUT TABLE", F_BIG, GOLD, CX, 82)
        rows = [
            ("-- BLIND BET  (only pays if you WIN) --",         GOLD),
            ("Royal Flush 500:1  |  Straight Flush 50:1  |  Four of a Kind 10:1", WHITE),
            ("Full House 3:1  |  Flush 2:1  |  Straight 1:1  |  Below Straight PUSH", WHITE),
            ("", WHITE),
            ("-- TRIPS BET  (always pays, win or lose) --",     GOLD),
            ("Royal Flush 50:1  |  Straight Flush 40:1  |  Four of a Kind 30:1", WHITE),
            ("Full House 8:1  |  Flush 7:1  |  Straight 4:1  |  Three of a Kind 3:1", WHITE),
            ("", WHITE),
            ("-- PLAY & ANTE BET  (vs dealer) --",              GOLD),
            ("Win 1:1  |  Push: get bet back  |  Lose: bet forfeited", WHITE),
            ("", WHITE),
            ("-- DEALER QUALIFYING HAND --",                    GOLD),
            ("Dealer must have at least ONE PAIR to qualify.", WHITE),
            ("If dealer does not qualify: ANTE is always a PUSH.", WHITE),
            ("", WHITE),
            ("-- BASIC STRATEGY --",                            GOLD),
            ("Pre-Flop: raise x4 with a pair, ace, or two high cards", WHITE),
            ("Flop:     raise x2 with a hidden pair or better", WHITE),
            ("River:    call x1 with any pair or better; else FOLD", WHITE),
            ("", WHITE),
            ("Press ESC or click anywhere to close",            GRAY),
        ]
        y = 116
        for text, col in rows:
            drawTextCenter(screen, text, F_SM, col, CX, y)
            y += 22

    def drawRankOverlay(self):
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 215))
        screen.blit(ov, (0, 0))
        drawRoundedRect(screen, PANEL, (CX-300, 148, 600, 380), radius=16, alpha=250)
        pygame.draw.rect(screen, GOLD,
                         (CX-300, 148, 600, 380), 2, border_radius=16)
        drawTextCenter(screen, "LEADERBOARD", F_BIG, GOLD, CX, 184)
        ordered = sorted(self.players, key=lambda p: p["chips"], reverse=True)
        medals  = ["1st", "2nd", "3rd"]
        for i in range(len(ordered)):
            p = ordered[i]
            if i == 0:
                col = HI
            elif p["out"]:
                col = GRAY_L
            else:
                col = WHITE
            if p["out"]:
                lbl = "ELIMINATED"
            else:
                lbl = "$ " + str(p["chips"])
            if i < 3:
                m = medals[i]
            else:
                m = "   "
            drawTextCenter(screen,
                           m + "   " + p["name"] + "   " + lbl,
                           F_MED, col, CX, 236+i*54)
        drawTextCenter(screen, "Press ESC or click anywhere to close",
                       F_TINY, GRAY, CX, 492)

#  ENTRY

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
