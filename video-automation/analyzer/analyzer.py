#!/usr/bin/env python3
"""
Video Analyzer - Phase 1
Nutzt WhisperX für:
- Transkription
- Wort-finales Timing
- Pausen-Detection
- Szenen-Klassifizierung
"""

import whisperx
import json
import torch
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path

@dataclass
class Pause:
    start: float
    end: float
    duration: float

@dataclass
class Word:
    word: str
    start: float
    end: float
    confidence: float

@dataclass
class Scene:
    type: str  # "talking", "pause", "broll_opportunity"
    start: float
    end: float
    confidence: float
    keywords: List[str]

@dataclass
class VideoAnalysis:
    transcript: str
    words: List[Dict]
    pauses: List[Dict]
    scenes: List[Dict]
    keywords: List[str]
    mood: str
    duration: float
    language: str

class VideoAnalyzer:
    def __init__(self, 
                 model_size: str = "large-v2",
                 device: str = None,
                 compute_type: str = "float16"):
        """
        Initialize Analyzer
        
        Args:
            model_size: "tiny", "base", "small", "medium", "large-v1", "large-v2"
            device: "cuda" or "cpu" (auto-detected if None)
            compute_type: "float16" (fast) or "int8" (slower, less memory)
        """
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.device = device
        self.compute_type = compute_type
        
        print(f"🔄 Lade WhisperX Model ({model_size}) auf {device}...")
        self.model = whisperx.load_model(
            model_size,
            device=device,
            compute_type=compute_type,
            language="de"  # Default German, auto-detect if needed
        )
        print("✅ Model geladen!")
    
    def analyze(self, video_path: str, 
                pause_threshold: float = 0.5,
                min_pause_duration: float = 0.3) -> VideoAnalysis:
        """
        Analysiert ein Video komplett
        
        Args:
            video_path: Pfad zum Video
            pause_threshold: Sekunden Stille = Pause
            min_pause_duration: Minimale Pausen-Länge
        """
        print(f"\n🎬 Analysiere: {video_path}")
        
        # 1. Audio laden
        print("📥 Lade Audio...")
        audio = whisperx.load_audio(video_path)
        
        # 2. Transkribieren
        print("🎯 Transkribiere...")
        result = self.model.transcribe(audio)
        language = result.get("language", "de")
        
        # 3. Wort-finales Timing (Alignment)
        print("⏱️ Berechne exaktes Timing...")
        model_a, metadata = whisperx.load_align_model(
            language_code=language, 
            device=self.device
        )
        result = whisperx.align(
            result["segments"], 
            model_a, 
            metadata, 
            audio, 
            self.device
        )
        
        # 4. Pausen finden
        print("🔍 Suche Pausen...")
        pauses = self._detect_pauses(
            result["word_segments"], 
            threshold=min_pause_duration
        )
        
        # 5. Szenen klassifizieren
        print("🎭 Klassifiziere Szenen...")
        scenes = self._classify_scenes(
            result["word_segments"],
            pauses,
            result["segments"]
        )
        
        # 6. Keywords extrahieren
        print("💡 Extrahiere Keywords...")
        keywords = self._extract_keywords(result["text"])
        
        # 7. Stimmung erkennen
        print("🎨 Analysiere Stimmung...")
        mood = self._detect_mood(result["text"])
        
        # 8. Gesamtdauer
        duration = result["segments"][-1]["end"] if result["segments"] else 0
        
        analysis = VideoAnalysis(
            transcript=result["text"],
            words=[{
                "word": w["word"],
                "start": w["start"],
                "end": w["end"],
                "confidence": w.get("score", 0.0)
            } for w in result.get("word_segments", [])],
            pauses=[asdict(p) for p in pauses],
            scenes=[asdict(s) for s in scenes],
            keywords=keywords,
            mood=mood,
            duration=duration,
            language=language
        )
        
        print(f"✅ Analyse komplett!")
        print(f"   - Dauer: {duration:.1f}s")
        print(f"   - Wörter: {len(analysis.words)}")
        print(f"   - Pausen: {len(analysis.pauses)}")
        print(f"   - Szenen: {len(analysis.scenes)}")
        print(f"   - Sprache: {language}")
        
        return analysis
    
    def _detect_pauses(self, words: List[Dict], 
                       threshold: float = 0.3) -> List[Pause]:
        """Findet Pausen zwischen Wörtern"""
        pauses = []
        
        for i in range(len(words) - 1):
            current_end = words[i]["end"]
            next_start = words[i + 1]["start"]
            gap = next_start - current_end
            
            if gap >= threshold:
                pauses.append(Pause(
                    start=current_end,
                    end=next_start,
                    duration=gap
                ))
        
        return pauses
    
    def _classify_scenes(self, words: List[Dict], 
                         pauses: List[Pause],
                         segments: List[Dict]) -> List[Scene]:
        """Klassifiziert Szenen-Typen"""
        scenes = []
        
        if not words:
            return scenes
        
        current_pos = 0
        
        # Erste Szene: Anfang bis erste Pause oder 5 Sekunden
        for pause in pauses:
            if pause.start > current_pos:
                # Prüfe ob es eine "talking" Szene ist
                scene_words = [w for w in words 
                              if current_pos <= w["start"] < pause.start]
                
                if scene_words:
                    density = len(scene_words) / (pause.start - current_pos)
                    
                    if density > 2:  # Mehr als 2 Wörter pro Sekunde
                        scene_type = "talking"
                    else:
                        scene_type = "slow_talking"
                    
                    scenes.append(Scene(
                        type=scene_type,
                        start=current_pos,
                        end=pause.start,
                        confidence=0.8,
                        keywords=[w["word"] for w in scene_words[:5]]
                    ))
                
                # Die Pause selbst als Szene
                scenes.append(Scene(
                    type="broll_opportunity" if pause.duration > 1.0 else "pause",
                    start=pause.start,
                    end=pause.end,
                    confidence=min(pause.duration, 1.0),
                    keywords=[]
                ))
                
                current_pos = pause.end
        
        # Letzte Szene (nach letzter Pause)
        if current_pos < words[-1]["end"]:
            scene_words = [w for w in words if w["start"] >= current_pos]
            scenes.append(Scene(
                type="talking",
                start=current_pos,
                end=words[-1]["end"],
                confidence=0.8,
                keywords=[w["word"] for w in scene_words[:5]]
            ))
        
        return scenes
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrahiert wichtige Keywords (einfache Version)"""
        # TODO: Mit spaCy oder GPT verbessern
        words = text.lower().split()
        
        # Filtere Füllwörter
        stopwords = {"der", "die", "das", "ein", "eine", "und", "oder", 
                     "aber", "mit", "für", "von", "zu", "ist", "sind"}
        
        keywords = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Zähle Häufigkeit
        from collections import Counter
        top_keywords = Counter(keywords).most_common(10)
        
        return [kw for kw, count in top_keywords]
    
    def _detect_mood(self, text: str) -> str:
        """Erkennt Stimmung (einfache Keyword-Matching)"""
        text_lower = text.lower()
        
        excited_words = ["super", "toll", "amazing", "wow", "genial", "mega"]
        calm_words = ["schön", "gut", "entspannt", "ruhig", "gemütlich"]
        urgent_words = ["jetzt", "sofort", "limited", "nur noch", "schnell"]
        
        excited_score = sum(1 for w in excited_words if w in text_lower)
        calm_score = sum(1 for w in calm_words if w in text_lower)
        urgent_score = sum(1 for w in urgent_words if w in text_lower)
        
        scores = {
            "excited": excited_score,
            "calm": calm_score,
            "urgent": urgent_score,
            "neutral": 1  # Default
        }
        
        return max(scores, key=scores.get)
    
    def save_analysis(self, analysis: VideoAnalysis, output_path: str):
        """Speichert Analyse als JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(analysis), f, indent=2, ensure_ascii=False)
        print(f"💾 Gespeichert: {output_path}")


# Test
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <video_file>")
        print("Example: python analyzer.py test_video.mp4")
        sys.exit(1)
    
    video_file = sys.argv[1]
    
    if not os.path.exists(video_file):
        print(f"❌ Datei nicht gefunden: {video_file}")
        sys.exit(1)
    
    # Analyzer initialisieren
    analyzer = VideoAnalyzer(
        model_size="base",  # Schneller für Tests, "large-v2" für Produktion
        device="cpu"        # "cuda" wenn GPU verfügbar
    )
    
    # Analysieren
    analysis = analyzer.analyze(video_file)
    
    # Speichern
    output_file = video_file.replace('.mp4', '_analysis.json')
    analyzer.save_analysis(analysis, output_file)
    
    # Kurze Zusammenfassung
    print(f"\n📊 Zusammenfassung:")
    print(f"   Transkript: {analysis.transcript[:100]}...")
    print(f"   Stimmung: {analysis.mood}")
    print(f"   Top Keywords: {', '.join(analysis.keywords[:5])}")
