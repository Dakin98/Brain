#!/usr/bin/env python3
"""
Content Engine Builder - Analysiert SRT-Dateien und erstellt eine Datenbank
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict

# Konfiguration
INPUT_DIR = "/Users/denizakin/Downloads/Sebastian Szalinski - Uploads from Sebastian Szalinski"
OUTPUT_DIR = "/Users/denizakin/.openclaw/workspace/content-engine"

# Kategorien-Mapping
CATEGORIES = {
    "skalierung": ["skalieren", "scale", "wachstum", "wachsen", "million", "umsatz", "revenue"],
    "ads": ["ads", "werbung", "facebook", "meta", "taboola", "native", "adspend", "cpm", "ctr"],
    "mindset": ["mindset", "gewinner", "erfolg", "glaubenssatz", "mental", "denken"],
    "team": ["team", "mitarbeiter", "recruiting", "a-player", "personal"],
    "strategie": ["strategie", "system", "prozess", "workflow", "funnel"],
    "ecom": ["ecom", "e-commerce", "dropshipping", "shop", "brand", "produkt"],
    "case_study": ["case study", "breakdown", "client", "win", "ergebnis"],
}

def clean_srt(text):
    """Entfernt SRT-Timestamps und Nummern"""
    # Entferne Nummernzeilen und Zeitstempel
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        # Überspringe leere Zeilen, Nummern und Zeitstempel
        if not line or line.isdigit():
            continue
        if re.match(r'\d{2}:\d{2}:\d{2}', line):
            continue
        cleaned.append(line)
    return ' '.join(cleaned)

def extract_key_quotes(text, max_quotes=5):
    """Extrahiert die besten Zitate basierend auf Länge und Inhalt"""
    sentences = re.split(r'[.!?]+', text)
    quotes = []
    
    for sent in sentences:
        sent = sent.strip()
        # Gute Zitate sind 10-150 Zeichen lang
        if 10 < len(sent) < 150:
            # Priorisiere Sätze mit starken Wörtern
            score = 0
            strong_words = ["niemals", "immer", "richtig", "falsch", "muss", "wichtig", 
                          "erfolg", "geld", "million", "skalieren", "system", "prozess"]
            for word in strong_words:
                if word in sent.lower():
                    score += 1
            if score > 0:
                quotes.append((sent, score))
    
    # Sortiere nach Score und nimm die Top 5
    quotes.sort(key=lambda x: x[1], reverse=True)
    return [q[0] for q in quotes[:max_quotes]]

def categorize_video(text, title):
    """Bestimmt die Kategorie eines Videos"""
    text_lower = (text + " " + title).lower()
    scores = defaultdict(int)
    
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            scores[category] += text_lower.count(keyword)
    
    if scores:
        return max(scores, key=scores.get)
    return "allgemein"

def detect_content_type(title):
    """Erkennt den Content-Typ"""
    title_lower = title.lower()
    if any(x in title_lower for x in ["vlog", "miami", "tag", "woche"]):
        return "Vlog"
    elif any(x in title_lower for x in ["guide", "tutorial", "how to", "anleitung"]):
        return "Tutorial"
    elif any(x in title_lower for x in ["case study", "breakdown", "client win"]):
        return "Case Study"
    elif any(x in title_lower for x in ["interview", "ft.", "mit", "gespräch"]):
        return "Interview"
    elif any(x in title_lower for x in ["keynote", "präsentation", "live"]):
        return "Keynote"
    elif any(x in title_lower for x in ["shorts", "#", "wusstest du"]):
        return "Short"
    else:
        return "Educational"

def clean_title(filename):
    """Bereinigt den Dateinamen zum Titel"""
    title = os.path.basename(filename)
    title = title.replace("(German_ASR).srt", "").replace("(English_ASR).srt", "")
    title = title.replace(".srt", "").strip()
    return title

def analyze_video(filepath):
    """Analysiert eine einzelne SRT-Datei"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()
    except Exception as e:
        return None
    
    title = clean_title(filepath)
    text = clean_srt(raw_text)
    
    # Minimale Länge checken
    if len(text) < 50:
        return None
    
    return {
        "title": title,
        "category": categorize_video(text, title),
        "content_type": detect_content_type(title),
        "key_quotes": extract_key_quotes(text),
        "word_count": len(text.split()),
        "filepath": filepath
    }

def main():
    print("🔍 Suche nach SRT-Dateien...")
    srt_files = list(Path(INPUT_DIR).glob("*.srt"))
    print(f"📁 {len(srt_files)} Dateien gefunden")
    
    database = []
    all_hooks = []
    category_counts = defaultdict(int)
    
    for i, filepath in enumerate(srt_files, 1):
        print(f"  [{i}/{len(srt_files)}] Analysiere: {filepath.name[:50]}...")
        
        video_data = analyze_video(str(filepath))
        if video_data:
            database.append(video_data)
            all_hooks.extend(video_data["key_quotes"])
            category_counts[video_data["category"]] += 1
    
    # Sortiere nach Wortanzahl (längste zuerst = wahrscheinlich inhaltlicher)
    database.sort(key=lambda x: x["word_count"], reverse=True)
    
    # Speichere JSON-Datenbank
    json_path = os.path.join(OUTPUT_DIR, "sebastian-szalinski-database.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    print(f"\n✅ JSON-Datenbank gespeichert: {json_path}")
    
    # Erstelle Hooks-Library
    hooks_path = os.path.join(OUTPUT_DIR, "hooks-library.md")
    with open(hooks_path, 'w', encoding='utf-8') as f:
        f.write("# Hooks Library - Sebastian Szalinski\n\n")
        f.write("Die besten Zitate und Hooks für deine eigenen Scripts:\n\n")
        
        # Gruppiere nach Kategorie
        by_category = defaultdict(list)
        for video in database:
            for quote in video["key_quotes"]:
                by_category[video["category"]].append((quote, video["title"]))
        
        for category, quotes in sorted(by_category.items()):
            f.write(f"\n## {category.upper()}\n\n")
            seen = set()
            for quote, title in quotes[:20]:  # Max 20 pro Kategorie
                if quote not in seen:
                    f.write(f'- "{quote}"\n')
                    f.write(f'  → *Aus: {title}*\n\n')
                    seen.add(quote)
    print(f"✅ Hooks-Library gespeichert: {hooks_path}")
    
    # Erstelle Themen-Übersicht
    themes_path = os.path.join(OUTPUT_DIR, "themes-and-concepts.md")
    with open(themes_path, 'w', encoding='utf-8') as f:
        f.write("# Themen & Konzepte - Sebastian Szalinski Content\n\n")
        
        f.write("## Kategorie-Verteilung\n\n")
        for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{cat}**: {count} Videos\n")
        
        f.write("\n## Alle Videos nach Kategorie\n\n")
        for category in sorted(by_category.keys()):
            f.write(f"\n### {category.upper()}\n\n")
            cat_videos = [v for v in database if v["category"] == category]
            for video in cat_videos[:15]:  # Max 15 pro Kategorie
                f.write(f"- **{video['title']}** ({video['content_type']}, {video['word_count']} Wörter)\n")
    print(f"✅ Themen-Übersicht gespeichert: {themes_path}")
    
    print(f"\n🎉 FERTIG! {len(database)} Videos analysiert.")
    print(f"\nZusammenfassung:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat}: {count}")

if __name__ == "__main__":
    main()
