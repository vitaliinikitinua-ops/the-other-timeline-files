# UGC_CREATOR — студія UGC-реклами ($0)

## Як працює (варіант 1: справжня зйомка + автоматичний монтаж)
1. **Інтерв'ю** → Claude ставить питання по одному (стиль, локація, образ, настрій, CTA).
2. **Дослідження продукту** → `projects/<id>/research/product_facts.md` (лише перевірені факти).
3. **Сценарій + план зйомки** → `projects/<id>/scripts/` (затвердження перед зйомкою).
4. **Зйомка** → модель знімає кліпи на телефон (вертикально, 4K/1080p, 30 fps) за планом.
5. **Кліпи** → кладемо в `projects/<id>/raw_footage/`.
6. **Монтаж** → `python3 scripts/ugc_build.py projects/<id>/project.json`
7. **Результат** → `projects/<id>/final/`: MP4, мініатюра, QC-звіт; `subtitles/`: .srt + .ass.

## Інструменти (усі безкоштовні)
| Задача | Інструмент |
|---|---|
| Монтаж, кадрування 9:16, експорт H.264 | FFmpeg |
| Субтитри з точним таймінгом | faster-whisper (CPU) + вирівнювання зі сценарієм |
| Український голос (запасний) | Piper TTS, голос `uk_UA-tetiana-high` (офлайн, без лімітів) |
| Преміум-голос (опційно) | ElevenLabs free tier (~10 000 симв./міс) → `"audio": "file"` |
| Картки продукту | оригінальне фото (етикетка не генерується AI) |

Встановлення: `pip install piper-tts faster-whisper pillow numpy`;
голос: `models/piper/uk_UA-tetiana-high.onnx` з huggingface.co/rhasspy/piper-voices.

## project.json — типи сцен
- `"visual": {"type": "video", "src": "raw_footage/01.mp4", "in": 2.0, "dur": 4.5, "focus": "center"}`
- `"visual": {"type": "photo", "src": "...jpg", "move": "in"|"out", "focus_y": 0.3}`
- `"visual": {"type": "product", "src": "...jpg"}` — картка з оригінального фото продукту
- `"audio": "clip"` (живий голос із кліпу) | `"tts"` (Piper) | `"file"` + `"audio_file"` | `"none"`
- `"line"` — текст репліки (субтитри беруть правопис звідси, таймінг — з розпізнавання)
- `"overlays": [{"text": "20 г білка", "style": "badge"|"top"|"cta", "at": 0.3}]`
- `"music": {"file": "...mp3", "volume_db": -18}` — автоматично стишується під голос

## Мови
Мова задається текстом сценарію + `language` для whisper (зараз `uk`). Для польської:
голос Piper `pl_PL-*`, whisper `language="pl"`.

## Приватність
Фото моделі, сирі кліпи та готові відео в git не потрапляють (`.gitignore`).
