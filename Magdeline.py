# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 20:19:13 2026

@author: user
"""

import streamlit as st
import random
import time


def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))


st.set_page_config(page_title="👾 Dodger Game", layout="centered")

# ------------------ CSS ------------------
st.markdown("""
<style>
.game {
    position: relative;
    width: 300px;
    height: 400px;
    background: black;
    border-radius: 12px;
    overflow: hidden;
    margin: auto;
}

.player {
    position: absolute;
    bottom: 10px;
    font-size: 30px;
    transition: left 0.1s;
}

.enemy {
    position: absolute;
    font-size: 26px;
}
</style>
""", unsafe_allow_html=True)


if "last_score_time" not in st.session_state:
    st.session_state.last_score_time = time.time()

if "explosion" not in st.session_state:
    st.session_state.explosion = False
    

# ------------------ Start Game & Music Button ------------------
# ------------------ Background Music ------------------
if "music_playing" not in st.session_state:
    st.session_state.music_playing = False

# Only start music when user clicks the start button
if not st.session_state.music_playing:
    if st.button("▶️ Start Game & Music"):
        st.session_state.music_playing = True

# Display audio player (persistent, not affected by reruns)
if st.session_state.music_playing:
   st.audio("background.mp3", format="audio/mp3", start_time=0)

# ------------------ State ------------------
if "player_x" not in st.session_state:
    st.session_state.player_x = 140
    st.session_state.enemies = []
    st.session_state.score = 0
    st.session_state.speed = 4
    st.session_state.game_over = False
    st.session_state.explosion = False

    # ⬇️ ADD THIS LINE
    st.session_state.high_score = load_high_score()

    # Initialize paused independently so it always exists
if "paused" not in st.session_state:
    st.session_state.paused = False

# ------------------ Controls ------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️"):
        st.session_state.player_x = max(0, st.session_state.player_x - 30)

with col3:
    if st.button("➡️"):
        st.session_state.player_x = min(260, st.session_state.player_x + 30)

# ------------------ Game Loop ------------------
#if not st.session_state.game_over:
    # Add enemies    
if not st.session_state.get('game_over', False) and not st.session_state.get('paused', False):
    st.write("Game is running...")
# ------------------ Time-based scoring ------------------
now = time.time()
if now - st.session_state.last_score_time >= 0.05:  # same as frame rate
    st.session_state.score += 1
    st.session_state.last_score_time = now

    # Add enemies, move enemies, check collisions, etc.    
    if random.random() < 0.08:
        st.session_state.enemies.append({
            "x": random.randint(0, 260),
            "y": 0,
            "scored": False 
        })

    # Move enemies
    for e in st.session_state.enemies:
        e["y"] += st.session_state.speed

    # ------------------ Collision detection ------------------
PLAYER_Y = 360        # visual top of rocket
PLAYER_WIDTH = 30
ENEMY_SIZE = 26

for e in st.session_state.enemies:
    hit_x = abs(e["x"] - st.session_state.player_x) < PLAYER_WIDTH
    hit_y = PLAYER_Y < e["y"] + ENEMY_SIZE and e["y"] < PLAYER_Y + 30

    if hit_x and hit_y:
        st.session_state.game_over = True
        st.session_state.explosion = True  # 👈 show explosion


    # Remove off-screen enemies
    # ------------------ Scoring (enemy dodged) ------------------
for e in st.session_state.enemies:
    if not e["scored"] and e["y"] > 380:
        #st.session_state.score += 1
        e["scored"] = True

    st.session_state.enemies = [
        e for e in st.session_state.enemies if e["y"] < 420
    ]

if "last_speed_score" not in st.session_state:
    st.session_state.last_speed_score = 0

    # Score + difficulty
if (
    st.session_state.score > 0
    and st.session_state.score % 200 == 0
    and st.session_state.score != st.session_state.last_speed_score
):
    st.session_state.speed += 1
    st.session_state.last_speed_score = st.session_state.score

# ------------------ Render ------------------
html = '<div class="game">'

if st.session_state.explosion:
    html += f'<div class="player" style="left:{st.session_state.player_x}px; bottom:10px">💥</div>'
else:
    html += f'<div class="player" style="left:{st.session_state.player_x}px; bottom:10px">🚀</div>'

for e in st.session_state.enemies:
    html += f'<div class="enemy" style="left:{e["x"]}px; top:{e["y"]}px">💣</div>'

html += '</div>'
st.markdown(html, unsafe_allow_html=True)


st.write(f"### 🏆 Score: {st.session_state.score}")
st.write(f"### 🥇 Highest Score: {st.session_state.high_score}")

# ------------------ Pause / Resume ------------------
if not st.session_state.game_over:  # Only show during play
    if st.session_state.paused:
        if st.button("▶️ Resume"):
            st.session_state.paused = False
    else:
        if st.button("⏸️ Pause"):
            st.session_state.paused = True


# ------------------ Game Over ------------------
if st.session_state.game_over:

    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score
        save_high_score(st.session_state.high_score)
        st.success("🏆 NEW HIGH SCORE!")
        #st.session_state.music_playing = False

    st.error("💥 GAME OVER")

    if st.button("🔄 Restart"):
        # Reset ONLY the game variables
        st.session_state.player_x = 140
        st.session_state.enemies = []
        st.session_state.score = 0
        st.session_state.speed = 4
        st.session_state.game_over = False
        st.session_state.explosion = False
        # High score stays intact
        st.rerun()




# ------------------ Frame Delay ------------------
time.sleep(0.05)
if not st.session_state.game_over and not st.session_state.paused:
    st.rerun()
