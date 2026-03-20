#!/usr/bin/env python3
"""
Sebastian Szalinski Content Database Builder
Analyzes 291 SRT files and creates a structured content database.
"""

import os
import re
import json
import glob
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import unicodedata

# Source directory
SOURCE_DIR = "/Users/denizakin/Downloads/Sebastian Szalinski - Uploads from Sebastian Szalinski"
OUTPUT_DIR = "/Users/denizakin/.openclaw/workspace/content-engine"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Content type patterns
CONTENT_TYPE_PATTERNS = {
    "vlog": ["vlog", "tag", "morgen", "abend", "flughafen", "reise", "unterwegs", "dabei sein"],
    "tutorial": ["tutorial", "anleitung", "so geht", "wie man", "schritt", "guide", "how to", "erklär"],
    "case_study": ["case study", "fallstudie", "von ... auf", "ergebnis", "profit", "umsatz", "skalierung", "client win"],
    "interview": ["interview", "ft.", "feat.", "mit ...", "gespräch", "zusammen mit", "talk mit"],
    "keynote": ["keynote", "präsentation", "vortrag", "bühne", "stage", "live", "event", "gewinnernacht"],
    "mindset": ["mindset", "glaubenssatz", "mental", "denken", "gewinner", "erfolg", "motivation"],
    "strategy": ["strategie", "plan", "roadmap", "aufbau", "struktur", "system"],
    "team": ["team", "mitarbeiter", "einstellen", "personal", "leute", "crew"],
    "ads": ["ads", "werbung", "facebook", "meta", "native ads", "tiktok", "adspend", "creative"],
    "scaling": ["skalierung", "skalieren", "wachstum", "mehr umsatz", "8-stellig", "7-stellig", "million"]
}

# Category keywords
CATEGORY_KEYWORDS = {
    "Skalierung": ["skalierung", "skalieren", "wachstum", "mehr umsatz", "umsatz steigern", "8-stellig", "7-stellig", "million", "revenue", "profit", "umsatz"],
    "Ads & Marketing": ["ads", "werbung", "facebook", "meta", "native ads", "tiktok", "adspend", "creative", "campaign", "funnel", "conversion", "cpm", "ctr", "roas"],
    "Mindset & Erfolg": ["mindset", "glaubenssatz", "mental", "gewinner", "erfolg", "motivation", "disziplin", "fokus", "ziele", "vision", "elite", "top 1%"],
    "Team & Hiring": ["team", "mitarbeiter", "einstellen", "personal", "leute", "crew", "hr", "recruiting", "arbeitgeber", "führung"],
    "Strategie & Systeme": ["strategie", "plan", "roadmap", "aufbau", "struktur", "system", "prozess", "workflow", "automation"],
    "E-Commerce": ["ecommerce", "e-commerce", "shop", "dropshipping", "produkt", "fulfillment", "versand", "kunde", "bestellung"],
    "Business Building": ["agentur", "unternehmen", "firma", "gründung", "startup", "business", "unternehmer"],
    "Personal": ["story", "geschichte", "mein", "ich habe", "persönlich", "leben", "privat"]
}

# Hook/Quote patterns
HOOK_PATTERNS = [
    r"(?!.*\b(und|oder|aber|weil|wenn|dass)\b)^[A-ZÄÖÜ][^.!?]{10,80}[.!?]",
    r"\b\d+[.,]?\d*\s*(?:€|euro|million|tausend|k)\b[^.!?]{0,60}",
    r"\b(?:niemals|immer|jeder|keiner|alle|niemand)\b[^.!?]{15,70}[.!?]",
    r"\b(?:geheim|secret|trick|hack|tipp|wichtig|kritisch)\b[^.!?]{15,70}[.!?]",
    r"\b(?:warum|wieso|was|wie|wo|wann)\b[^.!?]{10,70}[.!?]"
]


def clean_filename(filename):
    """Extract clean title from filename."""
    # Remove .srt extension
    name = filename.replace(".srt", "")
    # Remove language tags
    name = re.sub(r"\s*\([^)]*ASR[^)]*\)", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s*\([^)]*German[^)]*\)", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s*\([^)]*English[^)]*\)", "", name, flags=re.IGNORECASE)
    # Clean up special chars
    name = name.replace(";", ":").replace("¿", "?")
    return name.strip()


def parse_srt(filepath):
    """Parse SRT file and extract clean text."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Remove SRT block numbers and timestamps
    # Pattern: block number, then timestamp line, then text
    blocks = re.split(r'\n\n+', content)
    
    texts = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 2:
            # Skip block number and timestamp lines
            # Timestamp pattern: 00:00:00,000 --> 00:00:03,020
            text_lines = []
            for line in lines:
                if re.match(r'^\d+$', line.strip()):  # Block number
                    continue
                if re.match(r'^\d{2}:\d{2}:\d{2}[,.]\d+\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d+', line.strip()):  # Timestamp
                    continue
                text_lines.append(line)
            
            text = ' '.join(text_lines).strip()
            # Remove music and sound indicators
            text = re.sub(r'\[Musik\]', '', text, flags=re.IGNORECASE)
            text = re.sub(r'\[.*?\]', '', text)  # Remove all [bracket] content
            text = re.sub(r'\(.*?\)', '', text)  # Remove all (parenthesis) content
            if text and len(text) > 3:
                texts.append(text)
    
    return ' '.join(texts)


def detect_content_type(title, text):
    """Detect content type based on title and text."""
    title_lower = title.lower()
    text_lower = text.lower()
    
    scores = defaultdict(int)
    
    for content_type, patterns in CONTENT_TYPE_PATTERNS.items():
        for pattern in patterns:
            if pattern in title_lower:
                scores[content_type] += 3
            if pattern in text_lower[:5000]:  # Check first 5000 chars
                scores[content_type] += 1
    
    if scores:
        return max(scores, key=scores.get)
    return "other"


def detect_categories(title, text):
    """Detect categories based on keywords."""
    title_lower = title.lower()
    text_lower = text.lower()
    text_sample = text_lower[:10000]  # Check first 10000 chars
    
    categories = []
    scores = {}
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in title_lower:
                score += 3
            count = text_sample.count(keyword)
            score += count
        if score > 0:
            scores[category] = score
    
    # Get top categories
    sorted_cats = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    categories = [cat for cat, score in sorted_cats[:3]]  # Top 3
    
    if not categories:
        categories = ["Allgemein"]
    
    return categories


def extract_key_insights(text, num_insights=5):
    """Extract key insights/quotes from text."""
    insights = []
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Score sentences
    scored_sentences = []
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 20 or len(sent) > 200:
            continue
        
        score = 0
        sent_lower = sent.lower()
        
        # Boost for strong statements
        if re.search(r'\b\d+[.,]?\d*\s*(?:€|euro|million|tausend|k)\b', sent_lower):
            score += 5
        if re.search(r'\b(?:niemals|immer|jeder|keiner|alle|niemand|muss|wichtig|kritisch|geheim)\b', sent_lower):
            score += 3
        if re.search(r'\b(?:warum|wieso|was|wie)\b.*\?', sent_lower):
            score += 2
        if re.search(r'\b(?:erfolg|gewinnen|profit|umsatz|skalieren|wachstum)\b', sent_lower):
            score += 2
        
        # Penalize filler
        if '[Musik]' in sent or len(sent.split()) < 5:
            score -= 10
        
        if score > 0:
            scored_sentences.append((sent, score))
    
    # Sort by score and get top
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    
    # Deduplicate similar sentences
    seen_words = set()
    for sent, score in scored_sentences:
        words = set(sent.lower().split()[:5])  # First 5 words
        if not words & seen_words:  # If no overlap
            insights.append(sent)
            seen_words.update(words)
        if len(insights) >= num_insights:
            break
    
    return insights[:num_insights]


def extract_concepts(text):
    """Extract important concepts and terms."""
    concepts = set()
    text_lower = text.lower()
    
    # Common business/ecom terms
    concept_patterns = [
        r'\b(native ads|facebook ads|meta ads|tiktok ads|google ads)\b',
        r'\b(ctr|cpm|cpc|roas|cpa|conversion rate)\b',
        r'\b(funnel|landing page|checkout|upsell|crossell)\b',
        r'\b(shopify|woocommerce|magento|prestashop)\b',
        r'\b(dropshipping|fulfillment|lager|versand)\b',
        r'\b(creative|hook|angle|copy|headline)\b',
        r'\b(skalierung|scaling|wachstum|growth)\b',
        r'\b(agentur|unternehmen|business|startup)\b',
        r'\b(team|mitarbeiter|hiring|recruiting)\b',
        r'\b(mentor|coach|berater|experte)\b',
        r'\b(ecom|e-commerce|ecommerce|online shop)\b',
        r'\b(7-stellig|8-stellig|million|multi-million)\b',
        r'\b(adspend|budget|investment|roi)\b',
        r'\b(aov|ltv|cac|customer value)\b'
    ]
    
    for pattern in concept_patterns:
        matches = re.findall(pattern, text_lower)
        concepts.update(matches)
    
    return sorted(list(concepts))


def extract_hooks(text, title):
    """Extract potential hooks and strong openers."""
    hooks = []
    
    # Get first few sentences
    sentences = re.split(r'(?<=[.!?])\s+', text[:2000])
    
    for sent in sentences[:5]:
        sent = sent.strip()
        if len(sent) > 15 and len(sent) < 150:
            if '[Musik]' not in sent:
                hooks.append(sent)
    
    # Also look for strong statements throughout
    strong_patterns = [
        r'[^.!?]*\b\d+[.,]?\d*\s*(?:€|euro|million|tausend)\b[^.!?]*[.!?]',
        r'[^.!?]*\b(?:der größte|das wichtigste|die beste)\b[^.!?]*[.!?]',
        r'[^.!?]*\b(?:niemals|aufhören|nie)\b[^.!?]*[.!?]',
    ]
    
    for pattern in strong_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches[:3]:
            match = match.strip()
            if match not in hooks and len(match) < 150:
                hooks.append(match)
    
    return hooks[:5]


def process_all_srt_files():
    """Main processing function."""
    print("🔍 Suche nach SRT-Dateien...")
    
    srt_files = glob.glob(os.path.join(SOURCE_DIR, "*.srt"))
    print(f"📁 {len(srt_files)} SRT-Dateien gefunden")
    
    database = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "source": "Sebastian Szalinski - YouTube Uploads",
            "total_videos": len(srt_files),
            "version": "1.0"
        },
        "videos": []
    }
    
    all_hooks = []
    theme_stats = defaultdict(lambda: {"count": 0, "videos": [], "concepts": set()})
    
    for i, filepath in enumerate(sorted(srt_files), 1):
        filename = os.path.basename(filepath)
        print(f"\n[{i}/{len(srt_files)}] Verarbeite: {filename[:60]}...")
        
        # Extract clean title
        title = clean_filename(filename)
        
        # Parse SRT content
        text = parse_srt(filepath)
        
        if not text or len(text) < 100:
            print(f"   ⚠️  Zu wenig Text, überspringe...")
            continue
        
        # Analyze content
        content_type = detect_content_type(title, text)
        categories = detect_categories(title, text)
        insights = extract_key_insights(text)
        concepts = extract_concepts(text)
        hooks = extract_hooks(text, title)
        
        # Create video entry
        video_entry = {
            "id": i,
            "filename": filename,
            "title": title,
            "content_type": content_type,
            "categories": categories,
            "key_insights": insights,
            "concepts": concepts,
            "hooks": hooks,
            "text_length": len(text),
            "text_preview": text[:500] + "..." if len(text) > 500 else text
        }
        
        database["videos"].append(video_entry)
        
        # Collect for theme analysis
        for cat in categories:
            theme_stats[cat]["count"] += 1
            theme_stats[cat]["videos"].append({
                "title": title,
                "insights": insights[:2]
            })
            theme_stats[cat]["concepts"].update(concepts)
        
        # Collect hooks
        for hook in hooks:
            all_hooks.append({
                "hook": hook,
                "source": title,
                "category": categories[0] if categories else "Allgemein"
            })
        
        print(f"   ✅ Typ: {content_type} | Kategorien: {', '.join(categories)}")
        print(f"   📝 Insights: {len(insights)} | Konzepte: {len(concepts)} | Hooks: {len(hooks)}")
    
    # Save JSON database
    json_path = os.path.join(OUTPUT_DIR, "sebastian-szalinski-database.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    print(f"\n💾 JSON-Datenbank gespeichert: {json_path}")
    
    # Generate Hooks Library Markdown
    hooks_md = generate_hooks_markdown(all_hooks)
    hooks_path = os.path.join(OUTPUT_DIR, "hooks-library.md")
    with open(hooks_path, 'w', encoding='utf-8') as f:
        f.write(hooks_md)
    print(f"💾 Hooks-Library gespeichert: {hooks_path}")
    
    # Generate Themes Markdown
    themes_md = generate_themes_markdown(theme_stats, database["videos"])
    themes_path = os.path.join(OUTPUT_DIR, "themes-and-concepts.md")
    with open(themes_path, 'w', encoding='utf-8') as f:
        f.write(themes_md)
    print(f"💾 Themen-Übersicht gespeichert: {themes_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 ZUSAMMENFASSUNG")
    print("="*60)
    print(f"Videos verarbeitet: {len(database['videos'])}")
    print(f"Content-Typen: {len(set(v['content_type'] for v in database['videos']))}")
    print(f"Hooks extrahiert: {len(all_hooks)}")
    print(f"Themen-Kategorien: {len(theme_stats)}")
    print("\nTop Themen:")
    for theme, data in sorted(theme_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
        print(f"  • {theme}: {data['count']} Videos")
    print("="*60)


def generate_hooks_markdown(hooks):
    """Generate hooks library markdown."""
    md = """# 🎣 Hooks Library - Sebastian Szalinski

> Die besten Einstiege, Zitate und Power-Sätze aus 291 Videos

---

"""
    
    # Group by category
    by_category = defaultdict(list)
    for hook in hooks:
        by_category[hook["category"]].append(hook)
    
    for category, cat_hooks in sorted(by_category.items()):
        md += f"## {category}\n\n"
        for i, hook in enumerate(cat_hooks[:20], 1):  # Top 20 per category
            md += f"**{i}.** \"{hook['hook']}\"\n"
            md += f"   → *{hook['source'][:70]}...*\n\n"
        md += "\n---\n\n"
    
    # Add all hooks section
    md += "## Alle Hooks (Chronologisch)\n\n"
    for i, hook in enumerate(hooks, 1):
        md += f"{i}. \"{hook['hook']}\"\n"
        md += f"   [{hook['category']}] - {hook['source'][:60]}\n\n"
    
    return md


def generate_themes_markdown(theme_stats, videos):
    """Generate themes and concepts markdown."""
    md = """# 📚 Themen & Konzepte - Sebastian Szalinski Content-Analyse

> Strukturierte Übersicht aller Themen aus 291 Videos

---

## 📊 Themen-Verteilung

"""
    
    # Theme distribution
    for theme, data in sorted(theme_stats.items(), key=lambda x: x[1]['count'], reverse=True):
        md += f"### {theme} ({data['count']} Videos)\n\n"
        md += "**Key Concepts:** " + ", ".join(sorted(list(data['concepts']))[:10]) + "\n\n"
        md += "**Top Videos:**\n"
        for video in data['videos'][:5]:
            md += f"- {video['title'][:80]}\n"
            if video['insights']:
                md += f"  > \"{video['insights'][0][:100]}...\"\n"
        md += "\n---\n\n"
    
    # Content type breakdown
    md += "## 🎬 Content-Typen\n\n"
    type_counts = defaultdict(int)
    for video in videos:
        type_counts[video['content_type']] += 1
    
    for content_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        md += f"- **{content_type}**: {count} Videos\n"
    
    md += "\n---\n\n"
    
    # All concepts glossary
    all_concepts = set()
    for video in videos:
        all_concepts.update(video['concepts'])
    
    md += "## 📖 Konzepte-Glossar\n\n"
    md += "### Marketing & Ads\n"
    marketing_concepts = [c for c in sorted(all_concepts) if any(x in c for x in ['ads', 'ctr', 'cpm', 'conversion', 'funnel', 'creative', 'campaign'])]
    md += ", ".join(marketing_concepts) + "\n\n"
    
    md += "### E-Commerce\n"
    ecom_concepts = [c for c in sorted(all_concepts) if any(x in c for x in ['shop', 'dropshipping', 'fulfillment', 'ecom', 'checkout'])]
    md += ", ".join(ecom_concepts) + "\n\n"
    
    md += "### Business & Skalierung\n"
    business_concepts = [c for c in sorted(all_concepts) if any(x in c for x in ['skalierung', 'team', 'agentur', 'business', 'million'])]
    md += ", ".join(business_concepts) + "\n\n"
    
    # Video index
    md += "## 🎥 Vollständige Video-Liste\n\n"
    for video in videos:
        md += f"### {video['id']}. {video['title']}\n"
        md += f"- **Typ:** {video['content_type']}\n"
        md += f"- **Kategorien:** {', '.join(video['categories'])}\n"
        md += f"- **Konzepte:** {', '.join(video['concepts'][:8])}\n"
        if video['key_insights']:
            md += f"- **Key Insight:** \"{video['key_insights'][0][:120]}...\"\n"
        md += "\n"
    
    return md


if __name__ == "__main__":
    print("="*60)
    print("🚀 Sebastian Szalinski Content Database Builder")
    print("="*60)
    process_all_srt_files()
    print("\n✅ Fertig!")
