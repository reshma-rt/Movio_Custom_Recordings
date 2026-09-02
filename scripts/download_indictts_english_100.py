from datasets import load_dataset, Audio
from pathlib import Path
import csv
import io
import soundfile as sf

DATASET_ID = "SPRINGLab/IndicTTS-English"
LIMIT = 100

OUT_DIR = Path("public/english_indictts")
AUDIO_DIR = OUT_DIR / "audio"

OUT_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

print("Loading IndicTTS-English in STREAMING mode...")
ds = load_dataset(
    DATASET_ID,
    split="train",
    streaming=True,
)

# Avoid forcing full decoded arrays when raw audio bytes are available.
try:
    ds = ds.cast_column("audio", Audio(decode=False))
except Exception as e:
    print("Audio cast warning:", e)

metadata_rows = []

count = 0

for row in ds:
    if count >= LIMIT:
        break

    audio = row["audio"]
    text = str(row.get("text", "")).strip()

    sample_id = f"INDIC_EN_{count + 1:03d}"
    wav_name = f"{sample_id}.wav"
    wav_path = AUDIO_DIR / wav_name

    saved = False

    # Hugging Face Audio(decode=False) usually provides bytes/path.
    if isinstance(audio, dict):
        audio_bytes = audio.get("bytes")
        source_path = audio.get("path")

        if audio_bytes:
            # Decode the contained audio and save consistently as WAV.
            data, sr = sf.read(io.BytesIO(audio_bytes))
            sf.write(wav_path, data, sr)
            saved = True

        elif source_path:
            data, sr = sf.read(source_path)
            sf.write(wav_path, data, sr)
            saved = True

    # Fallback for already-decoded Audio objects.
    if not saved and isinstance(audio, dict):
        array = audio.get("array")
        sr = audio.get("sampling_rate")

        if array is not None and sr is not None:
            sf.write(wav_path, array, sr)
            saved = True

    if not saved:
        print(f"Skipping row {count}: unsupported audio representation")
        continue

    metadata_rows.append({
        "sample_id": sample_id,
        "audio_path": f"public/english_indictts/audio/{wav_name}",
        "language": "en",
        "source": "IndicTTS-English",
        "transcript": text,
    })

    count += 1
    print(f"[{count:03d}/{LIMIT}] {wav_name} -> {text[:70]}")

metadata_path = OUT_DIR / "metadata.csv"

with open(metadata_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "sample_id",
            "audio_path",
            "language",
            "source",
            "transcript",
        ],
    )
    writer.writeheader()
    writer.writerows(metadata_rows)

print("\nDONE")
print("Saved recordings :", len(metadata_rows))
print("Audio directory  :", AUDIO_DIR.resolve())
print("Metadata         :", metadata_path.resolve())