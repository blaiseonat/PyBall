import pygame
import sys
import random

pygame.init()

# =============== WINDOW / GLOBALS ===============
WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Baseball Career Mode")

# Grey + black theme
COLOR_BG = (15, 15, 15)
COLOR_PANEL = (30, 30, 30)
COLOR_ACCENT = (180, 180, 180)
COLOR_ACCENT_HOVER = (220, 220, 220)
COLOR_TEXT = (230, 230, 230)
COLOR_TEXT_DIM = (150, 150, 150)
COLOR_INPUT_BG = (25, 25, 25)
COLOR_INPUT_BORDER = (120, 120, 120)
COLOR_INPUT_BORDER_FOCUS = (200, 200, 200)

pygame.font.init()
FONT_LARGE = pygame.font.SysFont("segoeui", 60)
FONT_MED = pygame.font.SysFont("segoeui", 36)
FONT_SMALL = pygame.font.SysFont("segoeui", 24)
FONT_TINY = pygame.font.SysFont("segoeui", 18)

# =============== STATES ===============
STATE_MAIN_MENU = "MAIN_MENU"
STATE_CREATE_PLAYER = "CREATE_PLAYER"
STATE_PATH_SELECT = "PATH_SELECT"
STATE_SKIP_COLLEGE_DECISION = "SKIP_COLLEGE_DECISION"

STATE_COLLEGE_MENU = "COLLEGE_MENU"
STATE_COLLEGE_RECRUITING = "COLLEGE_RECRUITING"
STATE_COLLEGE_YEAR1 = "COLLEGE_YEAR1"
STATE_COLLEGE_YEAR2 = "COLLEGE_YEAR2"
STATE_COLLEGE_SUMMARY = "COLLEGE_SUMMARY"

STATE_COMBINE_MENU = "COMBINE_MENU"
STATE_COMBINE_MINIGAME = "COMBINE_MINIGAME"

STATE_DRAFT = "DRAFT"

STATE_MLB_CAREER_MENU = "MLB_CAREER_MENU"
STATE_MLB_SEASON = "MLB_SEASON"
STATE_MLB_HITTING_MINIGAME = "MLB_HITTING_MINIGAME"
STATE_MLB_FIELDING_MINIGAME = "MLB_FIELDING_MINIGAME"
STATE_MLB_SEASON_SUMMARY = "MLB_SEASON_SUMMARY"

STATE_CAREER_SUMMARY = "CAREER_SUMMARY"

state = STATE_MAIN_MENU

# =============== DATA ===============
player = {
    "name": "",
    "position": "P",
    "archetype": "Balanced",
    "bat_hand": "R",
    "throw_hand": "R",
    "height_in": 72,
    "weight_lb": 190,
    "number": 27,
    "hometown_state": "Ohio",
    "hometown_city": "Berlin",
    "college": None,
    "years_played": 0,
    "draft_round": None,
    "draft_team": None,
    "mlb_years": 0,
}

ratings = {
    "contact": 50,
    "power": 50,
    "speed": 50,
    "arm": 50,
    "fielding": 50,
    "overall": 50,
    "draft_stock": 50,
}

positions = ["P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF"]
archetypes = ["Balanced", "Power", "Contact", "Speed", "Fielding"]
bat_hands = ["R", "L", "S"]
throw_hands = ["R", "L"]

states_list = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
    "Wisconsin", "Wyoming"
]

default_cities = {
    "Ohio": ["Berlin", "Columbus", "Cleveland", "Cincinnati", "Toledo"],
    "California": ["Los Angeles", "San Diego", "San Jose", "San Francisco"],
    "Texas": ["Houston", "Dallas", "Austin", "San Antonio"],
}

college_offers = [
    {"name": "Ohio State", "prestige": 85},
    {"name": "Texas Longhorns", "prestige": 90},
    {"name": "UCLA Bruins", "prestige": 88},
    {"name": "Small D1 School", "prestige": 70},
]

combine_drills = [
    "60-Yard Dash",
    "Exit Velocity",
    "Arm Strength",
    "Fielding Workout",
]

create_name_text = ""
create_name_active = True
create_focus_name = True

create_selected_position = "P"
create_selected_archetype = "Balanced"
create_selected_bat = "R"
create_selected_throw = "R"
create_height_in = 72
create_weight_lb = 190
create_number = 27
create_state_index = states_list.index("Ohio")
create_city_index = 0

combine_current_drill = 0
combine_score = 0
college_year = 1
college_year_results = []

mlb_season_games = 162
mlb_season_stats = {
    "avg": 0.250,
    "hr": 0,
    "rbi": 0,
    "errors": 0,
    "hits": 0,
    "ab": 0,
}
mlb_career_stats = {
    "avg": 0.000,
    "hr": 0,
    "rbi": 0,
    "errors": 0,
    "hits": 0,
    "ab": 0,
}
mlb_season_game_count = 0
current_mlb_season = 1

clock = pygame.time.Clock()

# =============== HELPERS ===============
def draw_text(text, font, color, x, y, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    WIN.blit(surf, rect)


def draw_button(rect, text, hovered=False, font=FONT_MED):
    color = COLOR_PANEL
    border = COLOR_ACCENT_HOVER if hovered else COLOR_ACCENT
    pygame.draw.rect(WIN, color, rect, border_radius=8)
    pygame.draw.rect(WIN, border, rect, 2, border_radius=8)
    draw_text(text, font, COLOR_TEXT, rect.centerx, rect.centery - 2, center=True)


def draw_input_box(rect, text, focused=False, placeholder="", font=FONT_MED):
    pygame.draw.rect(WIN, COLOR_INPUT_BG, rect, border_radius=6)
    border_col = COLOR_INPUT_BORDER_FOCUS if focused else COLOR_INPUT_BORDER
    pygame.draw.rect(WIN, border_col, rect, 2, border_radius=6)

    if text:
        draw_text(text, font, COLOR_TEXT, rect.x + 10, rect.y + rect.height // 2 - 14)
    elif placeholder:
        draw_text(placeholder, font, COLOR_TEXT_DIM, rect.x + 10, rect.y + rect.height // 2 - 14)


def clamp(val, lo, hi):
    return max(lo, min(hi, val))


def random_team_name():
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Atlanta", "Seattle", "Miami", "Boston"]
    mascots = ["Stars", "Hawks", "Tigers", "Knights", "Sharks", "Bulls", "Thunder", "Caps"]
    return f"{random.choice(cities)} {random.choice(mascots)}"


# =============== SCREENS ===============
def screen_main_menu(events):
    global state
    WIN.fill(COLOR_BG)
    draw_text("Baseball Career Mode", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 150, center=True)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)

    start_rect = pygame.Rect(WIDTH // 2 - 150, 350, 300, 70)
    hovered = start_rect.collidepoint(mouse_pos)
    draw_button(start_rect, "New Career", hovered, FONT_MED)

    if mouse_clicked and hovered:
        state = STATE_CREATE_PLAYER


def screen_create_player(events):
    global state
    global create_name_text, create_name_active, create_focus_name
    global create_selected_position, create_selected_archetype
    global create_selected_bat, create_selected_throw
    global create_height_in, create_weight_lb, create_number
    global create_state_index, create_city_index
    global player, ratings

    WIN.fill(COLOR_BG)
    draw_text("Create Your Player", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 70, center=True)

    left_x = 200
    mid_x = WIDTH // 2
    right_x = WIDTH - 450
    top_y = 140
    line_gap = 70

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True
        if event.type == pygame.KEYDOWN and create_name_active:
            if event.key == pygame.K_BACKSPACE:
                create_name_text = create_name_text[:-1]
            elif event.key == pygame.K_RETURN:
                create_name_active = False
                create_focus_name = False
            else:
                if len(create_name_text) < 20:
                    create_name_text += event.unicode

    # Name
    name_rect = pygame.Rect(left_x, top_y, 500, 50)
    draw_text("Name", FONT_SMALL, COLOR_TEXT_DIM, name_rect.x, name_rect.y - 28)
    name_focused = create_focus_name
    if mouse_clicked and name_rect.collidepoint(mouse_pos):
        create_focus_name = True
        create_name_active = True
        name_focused = True
    elif mouse_clicked and not name_rect.collidepoint(mouse_pos):
        create_focus_name = False
        create_name_active = False
        name_focused = False
    draw_input_box(name_rect, create_name_text, focused=name_focused, placeholder="Type your name...")

    # Position
    pos_y = top_y + line_gap + 10
    draw_text("Position", FONT_SMALL, COLOR_TEXT_DIM, left_x, pos_y - 28)
    pos_buttons = []
    px = left_x
    py = pos_y
    for i, pos in enumerate(positions):
        rect = pygame.Rect(px, py, 80, 40)
        hovered = rect.collidepoint(mouse_pos)
        selected = (create_selected_position == pos)
        border = COLOR_ACCENT_HOVER if hovered or selected else COLOR_ACCENT
        pygame.draw.rect(WIN, COLOR_PANEL, rect, border_radius=6)
        pygame.draw.rect(WIN, border, rect, 2, border_radius=6)
        draw_text(pos, FONT_SMALL, COLOR_TEXT, rect.centerx, rect.centery - 2, center=True)
        pos_buttons.append((rect, pos))
        px += 90
        if (i + 1) % 5 == 0:
            px = left_x
            py += 50
    if mouse_clicked:
        for rect, pos in pos_buttons:
            if rect.collidepoint(mouse_pos):
                create_selected_position = pos

    # Archetype
    arch_y = pos_y + 120
    draw_text("Archetype", FONT_SMALL, COLOR_TEXT_DIM, left_x, arch_y - 28)
    arch_buttons = []
    ax = left_x
    ay = arch_y
    for arch in archetypes:
        rect = pygame.Rect(ax, ay, 150, 40)
        hovered = rect.collidepoint(mouse_pos)
        selected = (create_selected_archetype == arch)
        border = COLOR_ACCENT_HOVER if hovered or selected else COLOR_ACCENT
        pygame.draw.rect(WIN, COLOR_PANEL, rect, border_radius=6)
        pygame.draw.rect(WIN, border, rect, 2, border_radius=6)
        draw_text(arch, FONT_SMALL, COLOR_TEXT, rect.centerx, rect.centery - 2, center=True)
        arch_buttons.append((rect, arch))
        ay += 50
    if mouse_clicked:
        for rect, arch in arch_buttons:
            if rect.collidepoint(mouse_pos):
                create_selected_archetype = arch

    # Bat hand
    bt_y = top_y
    draw_text("Bat Hand", FONT_SMALL, COLOR_TEXT_DIM, mid_x, bt_y - 28)
    bat_rects = []
    bx = mid_x
    for bh in bat_hands:
        rect = pygame.Rect(bx, bt_y, 80, 40)
        hovered = rect.collidepoint(mouse_pos)
        selected = (create_selected_bat == bh)
        border = COLOR_ACCENT_HOVER if hovered or selected else COLOR_ACCENT
        pygame.draw.rect(WIN, COLOR_PANEL, rect, border_radius=6)
        pygame.draw.rect(WIN, border, rect, 2, border_radius=6)
        draw_text(bh, FONT_SMALL, COLOR_TEXT, rect.centerx, rect.centery - 2, center=True)
        bat_rects.append((rect, bh))
        bx += 90
    if mouse_clicked:
        for rect, bh in bat_rects:
            if rect.collidepoint(mouse_pos):
                create_selected_bat = bh

    # Throw hand
    bt_y2 = bt_y + line_gap
    draw_text("Throw Hand", FONT_SMALL, COLOR_TEXT_DIM, mid_x, bt_y2 - 28)
    throw_rects = []
    tx = mid_x
    for th in throw_hands:
        rect = pygame.Rect(tx, bt_y2, 80, 40)
        hovered = rect.collidepoint(mouse_pos)
        selected = (create_selected_throw == th)
        border = COLOR_ACCENT_HOVER if hovered or selected else COLOR_ACCENT
        pygame.draw.rect(WIN, COLOR_PANEL, rect, border_radius=6)
        pygame.draw.rect(WIN, border, rect, 2, border_radius=6)
        draw_text(th, FONT_SMALL, COLOR_TEXT, rect.centerx, rect.centery - 2, center=True)
        throw_rects.append((rect, th))
        tx += 90
    if mouse_clicked:
        for rect, th in throw_rects:
            if rect.collidepoint(mouse_pos):
                create_selected_throw = th

    # Height / Weight / Number
    hw_y = bt_y2 + line_gap + 10

    # Height
    draw_text("Height", FONT_SMALL, COLOR_TEXT_DIM, mid_x, hw_y - 28)
    height_rect = pygame.Rect(mid_x, hw_y, 160, 40)
    pygame.draw.rect(WIN, COLOR_PANEL, height_rect, border_radius=6)
    pygame.draw.rect(WIN, COLOR_ACCENT, height_rect, 2, border_radius=6)
    feet = create_height_in // 12
    inches = create_height_in % 12
    draw_text(f"{feet}'{inches}\"", FONT_SMALL, COLOR_TEXT, height_rect.centerx, height_rect.centery - 2, center=True)

    h_minus = pygame.Rect(height_rect.x - 50, hw_y, 40, 40)
    h_plus = pygame.Rect(height_rect.right + 10, hw_y, 40, 40)
    draw_button(h_minus, "-", h_minus.collidepoint(mouse_pos), FONT_SMALL)
    draw_button(h_plus, "+", h_plus.collidepoint(mouse_pos), FONT_SMALL)

    # Weight
    w_y = hw_y + 60
    draw_text("Weight (lb)", FONT_SMALL, COLOR_TEXT_DIM, mid_x, w_y - 28)
    weight_rect = pygame.Rect(mid_x, w_y, 160, 40)
    pygame.draw.rect(WIN, COLOR_PANEL, weight_rect, border_radius=6)
    pygame.draw.rect(WIN, COLOR_ACCENT, weight_rect, 2, border_radius=6)
    draw_text(str(create_weight_lb), FONT_SMALL, COLOR_TEXT, weight_rect.centerx, weight_rect.centery - 2, center=True)

    w_minus = pygame.Rect(weight_rect.x - 50, w_y, 40, 40)
    w_plus = pygame.Rect(weight_rect.right + 10, w_y, 40, 40)
    draw_button(w_minus, "-", w_minus.collidepoint(mouse_pos), FONT_SMALL)
    draw_button(w_plus, "+", w_plus.collidepoint(mouse_pos), FONT_SMALL)

    # Number
    n_y = w_y + 60
    draw_text("Jersey Number", FONT_SMALL, COLOR_TEXT_DIM, mid_x, n_y - 28)
    num_rect = pygame.Rect(mid_x, n_y, 160, 40)
    pygame.draw.rect(WIN, COLOR_PANEL, num_rect, border_radius=6)
    pygame.draw.rect(WIN, COLOR_ACCENT, num_rect, 2, border_radius=6)
    draw_text(str(create_number), FONT_SMALL, COLOR_TEXT, num_rect.centerx, num_rect.centery - 2, center=True)

    n_minus = pygame.Rect(num_rect.x - 50, n_y, 40, 40)
    n_plus = pygame.Rect(num_rect.right + 10, n_y, 40, 40)
    draw_button(n_minus, "-", n_minus.collidepoint(mouse_pos), FONT_SMALL)
    draw_button(n_plus, "+", n_plus.collidepoint(mouse_pos), FONT_SMALL)

    if mouse_clicked:
        if h_minus.collidepoint(mouse_pos):
            create_height_in = clamp(create_height_in - 1, 66, 80)
        if h_plus.collidepoint(mouse_pos):
            create_height_in = clamp(create_height_in + 1, 66, 80)
        if w_minus.collidepoint(mouse_pos):
            create_weight_lb = clamp(create_weight_lb - 1, 150, 260)
        if w_plus.collidepoint(mouse_pos):
            create_weight_lb = clamp(create_weight_lb + 1, 150, 260)
        if n_minus.collidepoint(mouse_pos):
            create_number = (create_number - 1) % 100
        if n_plus.collidepoint(mouse_pos):
            create_number = (create_number + 1) % 100

    # Hometown
    ht_y = top_y
    right_x = WIDTH - 450
    draw_text("Hometown State", FONT_SMALL, COLOR_TEXT_DIM, right_x, ht_y - 28)
    state_rect = pygame.Rect(right_x, ht_y, 260, 40)
    pygame.draw.rect(WIN, COLOR_PANEL, state_rect, border_radius=6)
    pygame.draw.rect(WIN, COLOR_ACCENT, state_rect, 2, border_radius=6)
    draw_text(states_list[create_state_index], FONT_SMALL, COLOR_TEXT, state_rect.centerx, state_rect.centery - 2, center=True)

    s_down = pygame.Rect(state_rect.x - 50, ht_y, 40, 40)
    s_up = pygame.Rect(state_rect.right + 10, ht_y, 40, 40)
    draw_button(s_down, "<", s_down.collidepoint(mouse_pos), FONT_SMALL)
    draw_button(s_up, ">", s_up.collidepoint(mouse_pos), FONT_SMALL)

    if mouse_clicked:
        if s_down.collidepoint(mouse_pos):
            create_state_index = (create_state_index - 1) % len(states_list)
            create_city_index = 0
        if s_up.collidepoint(mouse_pos):
            create_state_index = (create_state_index + 1) % len(states_list)
            create_city_index = 0

    current_state = states_list[create_state_index]
    cities = default_cities.get(current_state, [f"{current_state} City A", f"{current_state} City B"])
    create_city_index = clamp(create_city_index, 0, len(cities) - 1)

    city_y = ht_y + line_gap
    draw_text("Hometown City", FONT_SMALL, COLOR_TEXT_DIM, right_x, city_y - 28)
    city_rect = pygame.Rect(right_x, city_y, 260, 40)
    pygame.draw.rect(WIN, COLOR_PANEL, city_rect, border_radius=6)
    pygame.draw.rect(WIN, COLOR_ACCENT, city_rect, 2, border_radius=6)
    draw_text(cities[create_city_index], FONT_SMALL, COLOR_TEXT, city_rect.centerx, city_rect.centery - 2, center=True)

    c_down = pygame.Rect(city_rect.x - 50, city_y, 40, 40)
    c_up = pygame.Rect(city_rect.right + 10, city_y, 40, 40)
    draw_button(c_down, "<", c_down.collidepoint(mouse_pos), FONT_SMALL)
    draw_button(c_up, ">", c_up.collidepoint(mouse_pos), FONT_SMALL)

    if mouse_clicked:
        if c_down.collidepoint(mouse_pos):
            create_city_index = (create_city_index - 1) % len(cities)
        if c_up.collidepoint(mouse_pos):
            create_city_index = (create_city_index + 1) % len(cities)

    # Continue button
    cont_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 120, 300, 60)
    hovered = cont_rect.collidepoint(mouse_pos)
    draw_button(cont_rect, "Continue", hovered, FONT_MED)

    if mouse_clicked and cont_rect.collidepoint(mouse_pos):
        player["name"] = create_name_text if create_name_text.strip() else "Prospect"
        player["position"] = create_selected_position
        player["archetype"] = create_selected_archetype
        player["bat_hand"] = create_selected_bat
        player["throw_hand"] = create_selected_throw
        player["height_in"] = create_height_in
        player["weight_lb"] = create_weight_lb
        player["number"] = create_number
        player["hometown_state"] = current_state
        player["hometown_city"] = cities[create_city_index]

        base = 50
        ratings["contact"] = base
        ratings["power"] = base
        ratings["speed"] = base
        ratings["arm"] = base
        ratings["fielding"] = base

        if create_selected_archetype == "Power":
            ratings["power"] += 10
        elif create_selected_archetype == "Contact":
            ratings["contact"] += 10
        elif create_selected_archetype == "Speed":
            ratings["speed"] += 10
        elif create_selected_archetype == "Fielding":
            ratings["fielding"] += 10

        ratings["overall"] = int(
            (ratings["contact"] + ratings["power"] + ratings["speed"] +
             ratings["arm"] + ratings["fielding"]) / 5
        )
        ratings["draft_stock"] = ratings["overall"]

        state = STATE_PATH_SELECT


def screen_path_select(events):
    global state

    WIN.fill(COLOR_BG)
    draw_text("Where Does Your Journey Begin?", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 150, center=True)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)

    college_rect = pygame.Rect(WIDTH // 2 - 250, 350, 500, 70)
    skip_rect = pygame.Rect(WIDTH // 2 - 250, 450, 500, 70)

    draw_button(college_rect, "Go To College", college_rect.collidepoint(mouse_pos))
    draw_button(skip_rect, "Skip College (Go Pro)", skip_rect.collidepoint(mouse_pos))

    if mouse_clicked:
        if college_rect.collidepoint(mouse_pos):
            state = STATE_COLLEGE_MENU
        if skip_rect.collidepoint(mouse_pos):
            state = STATE_SKIP_COLLEGE_DECISION


def screen_skip_college_decision(events):
    global state

    WIN.fill(COLOR_BG)
    draw_text("Skip College?", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 150, center=True)
    draw_text("Do you want to participate in the MLB Combine?", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 230, center=True)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)

    yes_rect = pygame.Rect(WIDTH // 2 - 250, 350, 500, 70)
    no_rect = pygame.Rect(WIDTH // 2 - 250, 450, 500, 70)

    draw_button(yes_rect, "Yes — Enter Combine", yes_rect.collidepoint(mouse_pos))
    draw_button(no_rect, "No — Go Straight to Draft", no_rect.collidepoint(mouse_pos))

    if mouse_clicked:
        if yes_rect.collidepoint(mouse_pos):
            state = STATE_COMBINE_MENU
        if no_rect.collidepoint(mouse_pos):
            state = STATE_DRAFT


# =============== COLLEGE SYSTEM ===============
def screen_college_menu(events):
    global state

    WIN.fill(COLOR_BG)
    draw_text("College Path", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 150, center=True)
    draw_text("Choose how you want to start your college career.", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 220, center=True)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)

    recruit_rect = pygame.Rect(WIDTH // 2 - 250, 350, 500, 70)
    back_rect = pygame.Rect(WIDTH // 2 - 250, 450, 500, 70)

    draw_button(recruit_rect, "View College Offers", recruit_rect.collidepoint(mouse_pos))
    draw_button(back_rect, "Back to Path Select", back_rect.collidepoint(mouse_pos))

    if mouse_clicked:
        if recruit_rect.collidepoint(mouse_pos):
            state = STATE_COLLEGE_RECRUITING
        if back_rect.collidepoint(mouse_pos):
            state = STATE_PATH_SELECT


def screen_college_recruiting(events):
    global state, player, ratings, college_year

    WIN.fill(COLOR_BG)
    draw_text("College Recruiting", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 100, center=True)
    draw_text("Choose a school to commit to.", FONT_SMALL, COLOR_TEXT_DIM, WIDTH // 2, 160, center=True)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)

    start_y = 230
    buttons = []
    for i, offer in enumerate(college_offers):
        rect = pygame.Rect(WIDTH // 2 - 350, start_y + i * 80, 700, 60)
        hovered = rect.collidepoint(mouse_pos)
        text = f"{offer['name']}  (Prestige: {offer['prestige']})"
        draw_button(rect, text, hovered, FONT_SMALL)
        buttons.append((rect, offer))

    if mouse_clicked:
        for rect, offer in buttons:
            if rect.collidepoint(mouse_pos):
                player["college"] = offer["name"]
                college_year = 1
                player["years_played"] = 0
                state = STATE_COLLEGE_YEAR1


def college_year_minigame(year):
    performance = random.randint(40, 95)
    delta = (performance - 60) // 4
    ratings["contact"] = clamp(ratings["contact"] + delta, 30, 99)
    ratings["power"] = clamp(ratings["power"] + delta, 30, 99)
    ratings["speed"] = clamp(ratings["speed"] + delta, 30, 99)
    ratings["arm"] = clamp(ratings["arm"] + delta, 30, 99)
    ratings["fielding"] = clamp(ratings["fielding"] + delta, 30, 99)
    ratings["overall"] = int(
        (ratings["contact"] + ratings["power"] + ratings["speed"] +
         ratings["arm"] + ratings["fielding"]) / 5
    )
    ratings["draft_stock"] = clamp(ratings["draft_stock"] + delta * 2, 30, 99)
    return performance, delta


def screen_college_year(events, year):
    global state, college_year, college_year_results, player

    WIN.fill(COLOR_BG)
    title = "Freshman Year" if year == 1 else "Sophomore Year"
    draw_text(title, FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)
    draw_text(f"{player['college']}", FONT_MED, COLOR_TEXT_DIM, WIDTH // 2, 180, center=True)

    draw_text("Press SPACE to simulate your season performance.", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 260, center=True)

    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)
    keys = pygame.key.get_pressed()

    sim_rect = pygame.Rect(WIDTH // 2 - 200, 320, 400, 70)
    hovered = sim_rect.collidepoint(pygame.mouse.get_pos())
    draw_button(sim_rect, "Simulate Season", hovered, FONT_MED)

    if (mouse_clicked and hovered) or keys[pygame.K_SPACE]:
        perf, delta = college_year_minigame(year)
        college_year_results.append((year, perf, delta))
        player["years_played"] += 1
        if year == 1:
            state = STATE_COLLEGE_YEAR2
        else:
            state = STATE_COLLEGE_SUMMARY

    y = 430
    draw_text("Current Ratings:", FONT_SMALL, COLOR_TEXT, WIDTH // 2, y, center=True)
    y += 40
    draw_text(f"OVR: {ratings['overall']}  Draft Stock: {ratings['draft_stock']}", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, y, center=True)


def screen_college_summary(events):
    global state

    WIN.fill(COLOR_BG)
    draw_text("College Summary", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)
    draw_text(f"{player['college']} — {player['years_played']} Years", FONT_MED, COLOR_TEXT_DIM,
              WIDTH // 2, 180, center=True)

    y = 240
    for year, perf, delta in college_year_results:
        txt = f"Year {year}: Performance {perf}, Rating Change {delta:+}"
        draw_text(txt, FONT_SMALL, COLOR_TEXT, WIDTH // 2, y, center=True)
        y += 40

    draw_text("Press SPACE to enter the MLB Draft.", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, y + 40, center=True)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        state = STATE_DRAFT


# =============== COMBINE SYSTEM ===============
def screen_combine_menu(events):
    global state, combine_current_drill, combine_score

    WIN.fill(COLOR_BG)
    draw_text("MLB Combine", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)
    draw_text("Show scouts what you can do.", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 180, center=True)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)

    start_rect = pygame.Rect(WIDTH // 2 - 250, 320, 500, 70)
    skip_rect = pygame.Rect(WIDTH // 2 - 250, 420, 500, 70)

    draw_button(start_rect, "Start Combine Drills", start_rect.collidepoint(mouse_pos))
    draw_button(skip_rect, "Skip to Draft", skip_rect.collidepoint(mouse_pos))

    if mouse_clicked:
        if start_rect.collidepoint(mouse_pos):
            combine_current_drill = 0
            combine_score = 0
            state = STATE_COMBINE_MINIGAME
        if skip_rect.collidepoint(mouse_pos):
            state = STATE_DRAFT


def screen_combine_minigame(events):
    global state, combine_current_drill, combine_score, ratings

    WIN.fill(COLOR_BG)
    drill_name = combine_drills[combine_current_drill]
    draw_text("Combine Drill", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)
    draw_text(drill_name, FONT_MED, COLOR_TEXT_DIM, WIDTH // 2, 180, center=True)

    draw_text("Press SPACE to run the drill.", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 260, center=True)

    keys = pygame.key.get_pressed()
    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)

    start_rect = pygame.Rect(WIDTH // 2 - 200, 320, 400, 70)
    hovered = start_rect.collidepoint(pygame.mouse.get_pos())
    draw_button(start_rect, "Run Drill", hovered, FONT_MED)

    if (mouse_clicked and hovered) or keys[pygame.K_SPACE]:
        perf = random.randint(50, 100)
        combine_score += perf
        delta = (perf - 70) // 3
        ratings["draft_stock"] = clamp(ratings["draft_stock"] + delta, 30, 99)

        combine_current_drill += 1
        if combine_current_drill >= len(combine_drills):
            state = STATE_DRAFT
        else:
            pygame.time.delay(300)

    y = 430
    draw_text(f"Draft Stock: {ratings['draft_stock']}", FONT_SMALL, COLOR_TEXT, WIDTH // 2, y, center=True)


# =============== DRAFT & MLB CAREER ===============
def screen_draft(events):
    global state, player, ratings

    WIN.fill(COLOR_BG)
    draw_text("MLB Draft", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)

    if player["draft_round"] is None:
        stock = ratings["draft_stock"]
        if stock >= 85:
            rnd = random.randint(1, 2)
        elif stock >= 75:
            rnd = random.randint(2, 4)
        elif stock >= 65:
            rnd = random.randint(4, 7)
        else:
            rnd = random.randint(8, 15)
        player["draft_round"] = rnd
        player["draft_team"] = random_team_name()

    draw_text(f"{player['name']} has been drafted!", FONT_MED, COLOR_TEXT,
              WIDTH // 2, 200, center=True)
    draw_text(f"Team: {player['draft_team']}", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 260, center=True)
    draw_text(f"Round: {player['draft_round']}", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 300, center=True)
    draw_text(f"Final Draft Stock: {ratings['draft_stock']}", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 340, center=True)

    draw_text("Press SPACE to begin your MLB career.", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 420, center=True)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        state = STATE_MLB_CAREER_MENU


def screen_mlb_career_menu(events):
    global state

    WIN.fill(COLOR_BG)
    draw_text("MLB Career", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)
    draw_text(f"Team: {player['draft_team']}", FONT_MED, COLOR_TEXT_DIM, WIDTH // 2, 180, center=True)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)

    season_rect = pygame.Rect(WIDTH // 2 - 250, 320, 500, 70)
    summary_rect = pygame.Rect(WIDTH // 2 - 250, 420, 500, 70)

    draw_button(season_rect, "Play MLB Season", season_rect.collidepoint(mouse_pos))
    draw_button(summary_rect, "Skip to Career Summary", summary_rect.collidepoint(mouse_pos))

    if mouse_clicked:
        if season_rect.collidepoint(mouse_pos):
            start_new_mlb_season()
            state = STATE_MLB_SEASON
        if summary_rect.collidepoint(mouse_pos):
            state = STATE_CAREER_SUMMARY


def start_new_mlb_season():
    global mlb_season_stats, mlb_season_game_count
    mlb_season_stats = {
        "avg": 0.250,
        "hr": 0,
        "rbi": 0,
        "errors": 0,
        "hits": 0,
        "ab": 0,
    }
    mlb_season_game_count = 0


def update_career_stats_from_game(hits, ab, hr, rbi, errors):
    global mlb_career_stats
    mlb_career_stats["hits"] += hits
    mlb_career_stats["ab"] += ab
    mlb_career_stats["hr"] += hr
    mlb_career_stats["rbi"] += rbi
    mlb_career_stats["errors"] += errors
    if mlb_career_stats["ab"] > 0:
        mlb_career_stats["avg"] = mlb_career_stats["hits"] / mlb_career_stats["ab"]
    else:
        mlb_career_stats["avg"] = 0.0


def screen_mlb_season(events):
    global state, mlb_season_game_count, player

    WIN.fill(COLOR_BG)
    draw_text("MLB Regular Season", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)
    draw_text(f"Season {current_mlb_season}", FONT_MED, COLOR_TEXT_DIM, WIDTH // 2, 170, center=True)
    draw_text(f"Game {mlb_season_game_count + 1} of {mlb_season_games}", FONT_MED, COLOR_TEXT_DIM,
              WIDTH // 2, 210, center=True)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)

    hit_rect = pygame.Rect(WIDTH // 2 - 300, 320, 280, 70)
    field_rect = pygame.Rect(WIDTH // 2 + 20, 320, 280, 70)
    sim_rect = pygame.Rect(WIDTH // 2 - 150, 420, 300, 70)

    draw_button(hit_rect, "Hitting Minigame", hit_rect.collidepoint(mouse_pos))
    draw_button(field_rect, "Fielding Minigame", field_rect.collidepoint(mouse_pos))
    draw_button(sim_rect, "Simulate Game", sim_rect.collidepoint(mouse_pos))

    if mouse_clicked:
        if hit_rect.collidepoint(mouse_pos):
            state = STATE_MLB_HITTING_MINIGAME
        elif field_rect.collidepoint(mouse_pos):
            state = STATE_MLB_FIELDING_MINIGAME
        elif sim_rect.collidepoint(mouse_pos):
            simulate_full_game()
            mlb_season_game_count += 1
            if mlb_season_game_count >= mlb_season_games:
                player["mlb_years"] += 1
                state = STATE_MLB_SEASON_SUMMARY

    y = 520
    draw_text(
        f"Season AVG: {mlb_season_stats['avg']:.3f}  HR: {mlb_season_stats['hr']}  RBI: {mlb_season_stats['rbi']}  ERR: {mlb_season_stats['errors']}",
        FONT_SMALL, COLOR_TEXT, WIDTH // 2, y, center=True)
    y += 30
    draw_text(
        f"Career AVG: {mlb_career_stats['avg']:.3f}  HR: {mlb_career_stats['hr']}  RBI: {mlb_career_stats['rbi']}  ERR: {mlb_career_stats['errors']}",
        FONT_SMALL, COLOR_TEXT_DIM, WIDTH // 2, y, center=True)


def simulate_full_game():
    global mlb_season_stats, ratings
    contact_factor = ratings["contact"] / 100
    power_factor = ratings["power"] / 100
    field_factor = ratings["fielding"] / 100

    hits = random.choices([0, 1, 2, 3, 4], weights=[40, 35, 15, 7, 3])[0]
    at_bats = random.randint(3, 5)
    hr = 1 if random.random() < 0.05 + power_factor * 0.1 else 0
    rbi = hits + hr * 2
    errors = 1 if random.random() > field_factor + 0.7 else 0

    mlb_season_stats["hits"] += hits
    mlb_season_stats["ab"] += at_bats
    if mlb_season_stats["ab"] > 0:
        mlb_season_stats["avg"] = mlb_season_stats["hits"] / mlb_season_stats["ab"]
    mlb_season_stats["hr"] += hr
    mlb_season_stats["rbi"] += rbi
    mlb_season_stats["errors"] += errors

    update_career_stats_from_game(hits, at_bats, hr, rbi, errors)

    ratings["contact"] = clamp(ratings["contact"] + (hits - 1), 30, 99)
    ratings["power"] = clamp(ratings["power"] + hr, 30, 99)
    ratings["fielding"] = clamp(ratings["fielding"] - errors, 30, 99)
    ratings["overall"] = int(
        (ratings["contact"] + ratings["power"] + ratings["speed"] +
         ratings["arm"] + ratings["fielding"]) / 5
    )


def screen_mlb_hitting_minigame(events):
    global state, mlb_season_stats, ratings, mlb_season_game_count

    WIN.fill(COLOR_BG)
    draw_text("Hitting Minigame", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)
    draw_text("Press SPACE when the ball crosses the plate!", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 180, center=True)

    bar_rect = pygame.Rect(WIDTH // 2 - 300, 260, 600, 20)
    pygame.draw.rect(WIN, COLOR_PANEL, bar_rect)
    target_x = random.randint(bar_rect.x + 150, bar_rect.x + 450)
    pygame.draw.rect(WIN, COLOR_ACCENT, (target_x - 10, bar_rect.y - 10, 20, 40))

    keys = pygame.key.get_pressed()
    mouse_clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)

    swing_rect = pygame.Rect(WIDTH // 2 - 150, 340, 300, 70)
    hovered = swing_rect.collidepoint(pygame.mouse.get_pos())
    draw_button(swing_rect, "Swing (SPACE / Click)", hovered, FONT_MED)

    if (mouse_clicked and hovered) or keys[pygame.K_SPACE]:
        timing = random.randint(-50, 50)
        if abs(timing) < 10:
            hits = 1
            at_bats = 1
            hr = 1 if random.random() < 0.2 else 0
            rbi = 1 + hr
        elif abs(timing) < 25:
            hits = 1
            at_bats = 1
            hr = 0
            rbi = 1
        else:
            hits = 0
            at_bats = 1
            hr = 0
            rbi = 0

        mlb_season_stats["hits"] += hits
        mlb_season_stats["ab"] += at_bats
        if mlb_season_stats["ab"] > 0:
            mlb_season_stats["avg"] = mlb_season_stats["hits"] / mlb_season_stats["ab"]
        mlb_season_stats["hr"] += hr
        mlb_season_stats["rbi"] += rbi

        update_career_stats_from_game(hits, at_bats, hr, rbi, 0)

        ratings["contact"] = clamp(ratings["contact"] + hits, 30, 99)
        ratings["power"] = clamp(ratings["power"] + hr, 30, 99)
        ratings["overall"] = int(
            (ratings["contact"] + ratings["power"] + ratings["speed"] +
             ratings["arm"] + ratings["fielding"]) / 5
        )

        mlb_season_game_count += 1
        if mlb_season_game_count >= mlb_season_games:
            player["mlb_years"] += 1
            state = STATE_MLB_SEASON_SUMMARY
        else:
            state = STATE_MLB_SEASON

    draw_text("Result is applied automatically to your stats.", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 440, center=True)


def screen_mlb_fielding_minigame(events):
    global state, mlb_season_stats, ratings, mlb_season_game_count

    WIN.fill(COLOR_BG)
    draw_text("Fielding Minigame", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)
    draw_text("Move with ARROWS and press SPACE to field.", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 180, center=True)

    player_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT // 2 - 25, 50, 50)
    ball_rect = pygame.Rect(random.randint(200, WIDTH - 200), random.randint(250, HEIGHT - 200), 30, 30)

    keys = pygame.key.get_pressed()
    speed = 10
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed

    pygame.draw.rect(WIN, COLOR_ACCENT, player_rect, 2)
    pygame.draw.rect(WIN, COLOR_ACCENT_HOVER, ball_rect)

    if keys[pygame.K_SPACE]:
        if player_rect.colliderect(ball_rect):
            errors = 0
        else:
            errors = 1

        mlb_season_stats["errors"] += errors
        update_career_stats_from_game(0, 0, 0, 0, errors)

        ratings["fielding"] = clamp(ratings["fielding"] - errors, 30, 99)
        ratings["overall"] = int(
            (ratings["contact"] + ratings["power"] + ratings["speed"] +
             ratings["arm"] + ratings["fielding"]) / 5
        )

        mlb_season_game_count += 1
        if mlb_season_game_count >= mlb_season_games:
            player["mlb_years"] += 1
            state = STATE_MLB_SEASON_SUMMARY
        else:
            state = STATE_MLB_SEASON

    draw_text("Result is applied automatically to your stats.", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, 440, center=True)


def screen_mlb_season_summary(events):
    global state, current_mlb_season

    WIN.fill(COLOR_BG)
    draw_text("MLB Season Summary", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)
    draw_text(f"Season {current_mlb_season}", FONT_MED, COLOR_TEXT_DIM, WIDTH // 2, 170, center=True)

    y = 220
    draw_text(f"Season AVG: {mlb_season_stats['avg']:.3f}", FONT_SMALL, COLOR_TEXT, WIDTH // 2, y, center=True)
    y += 30
    draw_text(f"Season HR: {mlb_season_stats['hr']}  RBI: {mlb_season_stats['rbi']}", FONT_SMALL, COLOR_TEXT,
              WIDTH // 2, y, center=True)
    y += 30
    draw_text(f"Season Errors: {mlb_season_stats['errors']}", FONT_SMALL, COLOR_TEXT, WIDTH // 2, y, center=True)
    y += 50

    draw_text(f"Career AVG: {mlb_career_stats['avg']:.3f}", FONT_SMALL, COLOR_TEXT_DIM, WIDTH // 2, y, center=True)
    y += 30
    draw_text(f"Career HR: {mlb_career_stats['hr']}  RBI: {mlb_career_stats['rbi']}", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, y, center=True)
    y += 30
    draw_text(f"Career Errors: {mlb_career_stats['errors']}", FONT_SMALL, COLOR_TEXT_DIM, WIDTH // 2, y, center=True)
    y += 50

    if current_mlb_season >= 5:
        draw_text("Press R to retire, or N to play another season.", FONT_SMALL, COLOR_TEXT,
                  WIDTH // 2, y, center=True)
    else:
        draw_text("Press SPACE to play another season.", FONT_SMALL, COLOR_TEXT,
                  WIDTH // 2, y, center=True)

    keys = pygame.key.get_pressed()
    if current_mlb_season >= 5:
        if keys[pygame.K_r]:
            state = STATE_CAREER_SUMMARY
        elif keys[pygame.K_n]:
            current_mlb_season += 1
            start_new_mlb_season()
            state = STATE_MLB_SEASON
    else:
        if keys[pygame.K_SPACE]:
            current_mlb_season += 1
            start_new_mlb_season()
            state = STATE_MLB_SEASON


# =============== CAREER SUMMARY ===============
def screen_career_summary(events):
    global state

    WIN.fill(COLOR_BG)
    draw_text("Career Summary", FONT_LARGE, COLOR_TEXT, WIDTH // 2, 120, center=True)

    y = 180
    draw_text(f"Name: {player['name']}", FONT_SMALL, COLOR_TEXT, WIDTH // 2, y, center=True)
    y += 30
    draw_text(f"Position: {player['position']}  Archetype: {player['archetype']}", FONT_SMALL, COLOR_TEXT,
              WIDTH // 2, y, center=True)
    y += 30
    draw_text(f"Hometown: {player['hometown_city']}, {player['hometown_state']}", FONT_SMALL, COLOR_TEXT,
              WIDTH // 2, y, center=True)
    y += 40

    college_txt = player["college"] if player["college"] else "Skipped College"
    draw_text(f"College: {college_txt}", FONT_SMALL, COLOR_TEXT_DIM, WIDTH // 2, y, center=True)
    y += 30
    draw_text(f"Years Played in College: {player['years_played']}", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, y, center=True)
    y += 30
    draw_text(f"MLB Seasons Played: {player['mlb_years']}", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, y, center=True)
    y += 40

    draw_text(f"Final Ratings — OVR: {ratings['overall']}  Draft Stock: {ratings['draft_stock']}",
              FONT_SMALL, COLOR_TEXT, WIDTH // 2, y, center=True)
    y += 40

    draw_text(f"Drafted by: {player['draft_team']} (Round {player['draft_round']})",
              FONT_SMALL, COLOR_TEXT, WIDTH // 2, y, center=True)
    y += 40

    draw_text(f"Career AVG: {mlb_career_stats['avg']:.3f}  HR: {mlb_career_stats['hr']}  RBI: {mlb_career_stats['rbi']}  ERR: {mlb_career_stats['errors']}",
              FONT_SMALL, COLOR_TEXT, WIDTH // 2, y, center=True)
    y += 60

    draw_text("Press ESC to quit, or ENTER to restart a new career.", FONT_SMALL, COLOR_TEXT_DIM,
              WIDTH // 2, y, center=True)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    if keys[pygame.K_RETURN]:
        reset_career()


def reset_career():
    global state, player, ratings, create_name_text, create_name_active, create_focus_name
    global create_selected_position, create_selected_archetype, create_selected_bat, create_selected_throw
    global create_height_in, create_weight_lb, create_number, create_state_index, create_city_index
    global college_year_results, combine_current_drill, combine_score
    global mlb_season_stats, mlb_season_game_count, mlb_career_stats, current_mlb_season

    player.update({
        "name": "",
        "position": "P",
        "archetype": "Balanced",
        "bat_hand": "R",
        "throw_hand": "R",
        "height_in": 72,
        "weight_lb": 190,
        "number": 27,
        "hometown_state": "Ohio",
        "hometown_city": "Berlin",
        "college": None,
        "years_played": 0,
        "draft_round": None,
        "draft_team": None,
        "mlb_years": 0,
    })

    ratings.update({
        "contact": 50,
        "power": 50,
        "speed": 50,
        "arm": 50,
        "fielding": 50,
        "overall": 50,
        "draft_stock": 50,
    })

    create_name_text = ""
    create_name_active = True
    create_focus_name = True
    create_selected_position = "P"
    create_selected_archetype = "Balanced"
    create_selected_bat = "R"
    create_selected_throw = "R"
    create_height_in = 72
    create_weight_lb = 190
    create_number = 27
    create_state_index = states_list.index("Ohio")
    create_city_index = 0

    college_year_results = []
    combine_current_drill = 0
    combine_score = 0

    mlb_season_stats = {
        "avg": 0.250,
        "hr": 0,
        "rbi": 0,
        "errors": 0,
        "hits": 0,
        "ab": 0,
    }
    mlb_career_stats = {
        "avg": 0.000,
        "hr": 0,
        "rbi": 0,
        "errors": 0,
        "hits": 0,
        "ab": 0,
    }
    mlb_season_game_count = 0
    current_mlb_season = 1

    state = STATE_MAIN_MENU


# =============== MAIN LOOP ===============
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if state == STATE_MAIN_MENU:
        screen_main_menu(events)
    elif state == STATE_CREATE_PLAYER:
        screen_create_player(events)
    elif state == STATE_PATH_SELECT:
        screen_path_select(events)
    elif state == STATE_SKIP_COLLEGE_DECISION:
        screen_skip_college_decision(events)
    elif state == STATE_COLLEGE_MENU:
        screen_college_menu(events)
    elif state == STATE_COLLEGE_RECRUITING:
        screen_college_recruiting(events)
    elif state == STATE_COLLEGE_YEAR1:
        screen_college_year(events, 1)
    elif state == STATE_COLLEGE_YEAR2:
        screen_college_year(events, 2)
    elif state == STATE_COLLEGE_SUMMARY:
        screen_college_summary(events)
    elif state == STATE_COMBINE_MENU:
        screen_combine_menu(events)
    elif state == STATE_COMBINE_MINIGAME:
        screen_combine_minigame(events)
    elif state == STATE_DRAFT:
        screen_draft(events)
    elif state == STATE_MLB_CAREER_MENU:
        screen_mlb_career_menu(events)
    elif state == STATE_MLB_SEASON:
        screen_mlb_season(events)
    elif state == STATE_MLB_HITTING_MINIGAME:
        screen_mlb_hitting_minigame(events)
    elif state == STATE_MLB_FIELDING_MINIGAME:
        screen_mlb_fielding_minigame(events)
    elif state == STATE_MLB_SEASON_SUMMARY:
        screen_mlb_season_summary(events)
    elif state == STATE_CAREER_SUMMARY:
        screen_career_summary(events)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
