#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
import requests
from datetime import datetime, timedelta
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
GITHUB_USER = os.getenv("USER") or "player"  # Замени на свой ник или передавай аргументом

def get_github_activity(username):
    """Получает количество коммитов за сегодня (энергия для игры)."""
    try:
        # GitHub API требует user-agent
        headers = {'User-Agent': 'mars1984-game'}
        url = f"https://api.github.com/users/{username}/events"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            events = response.json()
            today = datetime.now().date()
            count = 0
            for event in events:
                # Считаем только PushEvent'ы
                if event['type'] == 'PushEvent':
                    event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ').date()
                    if event_date == today:
                        # Считаем коммиты в пуше
                        count += len(event['payload']['commits'])
            return count
        else:
            return 0
    except:
        return 0

def load_map():
    """Загружает карту из файла universe/MAP.grid."""
    map_file = "universe/MAP.grid"
    if not os.path.exists(map_file):
        # Если карты нет, создаем пустую
        with open(map_file, 'w') as f:
            for _ in range(20):  # 20 строк
                f.write("." * 60 + "\n")  # 60 точек (пустая земля)
    with open(map_file, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def save_map(map_data):
    """Сохраняет карту."""
    with open("universe/MAP.grid", 'w') as f:
        for row in map_data:
            f.write(''.join(row) + '\n')

def render_map(map_data, player_pos):
    """Превращает карту в красивый Rich-текст."""
    rendered = ""
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if (x, y) == player_pos:
                rendered += "[bold white on red]@[/]"  # Игрок
            elif cell == '.':
                rendered += "[dim white].[/]"
            elif cell == 'R':
                rendered += "[red]R[/]"
            elif cell == 'S':
                rendered += "[blue]S[/]"
            elif cell == 'M':
                rendered += "[yellow]M[/]"
            else:
                rendered += cell
