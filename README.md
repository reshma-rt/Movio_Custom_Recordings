# Movio Custom Speech Recording Guide

This README defines the **required folder structure, file naming
convention, recording assignment, metadata format, and GitHub upload
commands** for the Movio custom speech dataset.

> **Please follow the naming exactly. Do not create your own filename
> format.**

------------------------------------------------------------------------

## 1. Dataset Plan

The custom evaluation set contains **200 recordings from 5 speakers**.

Each speaker records exactly **40 sentences**:

  Category                                 Per Speaker   Total (5 Speakers)
  -------------------------------------- ------------- --------------------
  Tamil (`TA`)                                       8                   40
  English (`EN`)                                     8                   40
  Tanglish / Code-mixed (`TG`)                      12                   60
  Transportation / Entity-heavy (`TR`)              12                   60
  **Total**                                     **40**              **200**

Each teammate should record **only the 40 prompts assigned to their
speaker ID**.

------------------------------------------------------------------------

## 2. Final Repository Structure

``` text
Movio_Custom_Recordings/
│
├── public/
│   ├── tamil_openslr65/
│   │   ├── audio/
│   │   │   ├── female/
│   │   │   │   ├── PUB_TA_F_001.wav
│   │   │   │   └── ... PUB_TA_F_050.wav
│   │   │   └── male/
│   │   │       ├── PUB_TA_M_001.wav
│   │   │       └── ... PUB_TA_M_050.wav
│   │   └── metadata.csv
│   │
│   └── english/
│       ├── audio/
│       │   ├── female/
│       │   └── male/
│       └── metadata.csv
│
├── custom/
│   ├── prompts/
│   │   └── transportation_voice_test_sentences_200.txt
│   │
│   ├── speaker_01/
│   │   └── 40 WAV recordings
│   │
│   ├── speaker_02/
│   │   └── 40 WAV recordings
│   │
│   ├── speaker_03/
│   │   └── 40 WAV recordings
│   │
│   ├── speaker_04/
│   │   └── 40 WAV recordings
│   │
│   ├── speaker_05/
│   │   └── 40 WAV recordings
│   │
│   └── metadata_custom.csv
│
└── metadata_master.csv
```

------------------------------------------------------------------------

## 3. Speaker IDs

Use only these speaker IDs:

  Person      Speaker ID   GitHub Folder
  ----------- ------------ ----------------------
  Speaker 1   `S01`        `custom/speaker_01/`
  Speaker 2   `S02`        `custom/speaker_02/`
  Speaker 3   `S03`        `custom/speaker_03/`
  Speaker 4   `S04`        `custom/speaker_04/`
  Speaker 5   `S05`        `custom/speaker_05/`

**Do not use personal names in WAV filenames.**

------------------------------------------------------------------------

## 4. File Naming Rule

Every custom recording must follow:

``` text
CUS_<SPEAKER_ID>_<PROMPT_ID>.wav
```

Example:

``` text
CUS_S01_TA001.wav
```

Meaning:

``` text
CUS   = Custom recording
S01   = Speaker 01
TA001 = Original prompt ID
```

### Prompt prefixes

  Prefix   Meaning
  -------- -------------------------------------
  `TA`     Tamil
  `EN`     English
  `TG`     Tanglish / Tamil-English code-mixed
  `TR`     Transportation / entity-heavy

### Correct examples

``` text
CUS_S01_TA001.wav
CUS_S01_EN006.wav
CUS_S01_TG021.wav
CUS_S01_TR012.wav

CUS_S02_TA009.wav
CUS_S03_EN025.wav
CUS_S04_TG052.wav
CUS_S05_TR060.wav
```

### Incorrect examples

``` text
audio1.wav
recording.wav
Reshma_1.wav
Tamil001.wav
S1_TA1.wav
CUS_S1_TA1.wav
CUS_S01_TA_001.wav
```

Do not change `TA001` into `TA_001`. The prompt ID must remain exactly
as assigned.

------------------------------------------------------------------------

## 5. Before Recording

Each teammate must know:

1.  Their speaker ID (`S01`--`S05`).
2.  Their assigned 40 prompt IDs.
3.  The exact sentence corresponding to each prompt ID.
4.  The recording order.

Record in the **same order as the assigned prompt list**.

Do not skip a prompt. If a recording is bad, record that sentence again
before continuing or clearly mark the retake.

------------------------------------------------------------------------

## 6. Recording Recommendations

For consistency:

-   Record in a quiet room.
-   Keep approximately the same microphone distance.
-   Speak naturally and clearly.
-   Do not intentionally exaggerate pronunciation.
-   Avoid background music, fans, TV, and other voices.
-   Avoid cutting off the beginning or end of words.
-   Prefer WAV output.
-   Do not edit the sentence wording.
-   Read the assigned sentence exactly.
-   Check the recording before uploading.

Keep an untouched copy of the original recordings until the dataset has
been verified.

------------------------------------------------------------------------

## 7. Recommended Local Raw Folder

Before uploading to GitHub, keep the recordings locally:

``` text
D:\TTS_Datasets\Custom_Raw\
│
├── speaker_01\
├── speaker_02\
├── speaker_03\
├── speaker_04\
└── speaker_05\
```

For example:

``` text
D:\TTS_Datasets\Custom_Raw\speaker_03\
```

may initially contain:

``` text
001.wav
002.wav
003.wav
...
040.wav
```

Do not delete these raw files after renaming. Keep them as backup.

------------------------------------------------------------------------

## 8. Renaming Using a Mapping File

Because every speaker receives a mixture of `TA`, `EN`, `TG`, and `TR`
prompts, use a mapping file rather than guessing filenames.

Create:

``` text
mapping.csv
```

inside your raw speaker folder.

Example:

``` csv
old_name,prompt_id
001.wav,TA001
002.wav,TA006
003.wav,TA011
004.wav,EN001
005.wav,EN006
006.wav,TG001
007.wav,TG006
008.wav,TR001
```

The actual prompt IDs must match the prompts assigned to that speaker.

### Speaker 1 rename command

Open PowerShell:

``` powershell
$folder = "D:\TTS_Datasets\Custom_Raw\speaker_01"
$speaker = "S01"

$mapping = Import-Csv "$folder\mapping.csv"

foreach ($row in $mapping) {
    $oldPath = Join-Path $folder $row.old_name
    $newName = "CUS_${speaker}_$($row.prompt_id).wav"
    $newPath = Join-Path $folder $newName

    if (-not (Test-Path $oldPath)) {
        Write-Host "MISSING: $($row.old_name)" -ForegroundColor Red
        continue
    }

    if (Test-Path $newPath) {
        Write-Host "TARGET ALREADY EXISTS: $newName" -ForegroundColor Yellow
        continue
    }

    Rename-Item -LiteralPath $oldPath -NewName $newName
    Write-Host "$($row.old_name) -> $newName"
}
```

For another speaker, change only:

``` powershell
$folder = "D:\TTS_Datasets\Custom_Raw\speaker_02"
$speaker = "S02"
```

Use `S03`, `S04`, or `S05` as appropriate.

------------------------------------------------------------------------

## 9. Verify the Renaming

Check all WAV filenames:

``` powershell
Get-ChildItem "D:\TTS_Datasets\Custom_Raw\speaker_01" -Filter "*.wav" |
Select-Object Name
```

Check the count:

``` powershell
(Get-ChildItem "D:\TTS_Datasets\Custom_Raw\speaker_01" -Filter "*.wav").Count
```

Expected:

``` text
40
```

If the result is not `40`, **do not upload yet**.

------------------------------------------------------------------------

## 10. Clone the GitHub Repository

A teammate only needs to clone the repository once.

Choose a location, for example `D:\`:

``` powershell
cd D:\
git clone https://github.com/reshma-rt/Movio_Custom_Recordings.git
cd Movio_Custom_Recordings
```

Confirm the repository connection:

``` powershell
git remote -v
```

------------------------------------------------------------------------

## 11. Always Pull Before Adding Recordings

Before modifying the repository:

``` powershell
cd D:\Movio_Custom_Recordings
git pull origin main
```

This is important when several teammates are contributing.

------------------------------------------------------------------------

## 12. Copy Your 40 Final WAV Files

### Speaker 1

``` powershell
Copy-Item `
"D:\TTS_Datasets\Custom_Raw\speaker_01\*.wav" `
"D:\Movio_Custom_Recordings\custom\speaker_01\" `
-Force
```

### Speaker 2

``` powershell
Copy-Item `
"D:\TTS_Datasets\Custom_Raw\speaker_02\*.wav" `
"D:\Movio_Custom_Recordings\custom\speaker_02\" `
-Force
```

For Speakers 3--5, change the speaker number accordingly.

------------------------------------------------------------------------

## 13. Verify the Repository Copy

For Speaker 1:

``` powershell
(Get-ChildItem `
"D:\Movio_Custom_Recordings\custom\speaker_01\*.wav").Count
```

Expected:

``` text
40
```

Also inspect the filenames:

``` powershell
Get-ChildItem `
"D:\Movio_Custom_Recordings\custom\speaker_01\*.wav" |
Select-Object Name
```

Every file must begin with:

``` text
CUS_S01_
```

For Speaker 2 it must be `CUS_S02_`, etc.

------------------------------------------------------------------------

## 14. Upload Your Recordings to GitHub

Go to the repository:

``` powershell
cd D:\Movio_Custom_Recordings
```

Pull once more before committing:

``` powershell
git pull origin main
```

Check changes:

``` powershell
git status
```

### IMPORTANT --- Add only your own speaker folder

Speaker 1:

``` powershell
git add custom/speaker_01
```

Speaker 2:

``` powershell
git add custom/speaker_02
```

Speaker 3:

``` powershell
git add custom/speaker_03
```

Speaker 4:

``` powershell
git add custom/speaker_04
```

Speaker 5:

``` powershell
git add custom/speaker_05
```

Do **not** use `git add .` unless you know exactly what other files have
changed.

Check again:

``` powershell
git status
```

------------------------------------------------------------------------

## 15. Commit

Use a clear speaker-specific commit message.

Speaker 1:

``` powershell
git commit -m "Add S01 custom speech recordings"
```

Speaker 2:

``` powershell
git commit -m "Add S02 custom speech recordings"
```

Speaker 3:

``` powershell
git commit -m "Add S03 custom speech recordings"
```

Speaker 4:

``` powershell
git commit -m "Add S04 custom speech recordings"
```

Speaker 5:

``` powershell
git commit -m "Add S05 custom speech recordings"
```

------------------------------------------------------------------------

## 16. Push to GitHub

``` powershell
git push origin main
```

After the push succeeds, open the GitHub repository and verify that the
files appear in the correct folder.

Example for Speaker 3:

``` text
custom/
└── speaker_03/
    ├── CUS_S03_TA....wav
    ├── CUS_S03_EN....wav
    ├── CUS_S03_TG....wav
    └── CUS_S03_TR....wav
```

------------------------------------------------------------------------

## 17. If `git push` Is Rejected

Do **not** delete files or force-push.

First run:

``` powershell
git pull --rebase origin main
```

Then:

``` powershell
git push origin main
```

If Git reports a merge/rebase conflict, stop and ask the project
maintainer before changing or deleting another speaker's files.

Never use:

``` text
git push --force
```

for this shared dataset repository.

------------------------------------------------------------------------

## 18. Metadata

The project maintains:

``` text
custom/metadata_custom.csv
```

Recommended columns:

``` csv
sample_id,audio_path,speaker_id,prompt_id,category,language,transcript
```

Example:

``` csv
CUS_S01_TA001,speaker_01/CUS_S01_TA001.wav,S01,TA001,tamil,tamil,எனக்கு ஒரு கார் புக் செய்ய வேண்டும்.
```

Unless specifically assigned to update metadata, teammates should upload
their correctly named WAV files and leave the central metadata file to
the dataset maintainer. This reduces merge conflicts.

------------------------------------------------------------------------

## 19. Final Checklist Before Upload

Before pushing, verify all of the following:

-   [ ] I am using my assigned speaker ID.
-   [ ] I recorded exactly 40 assigned prompts.
-   [ ] All files are WAV.
-   [ ] Every filename follows `CUS_<SPEAKER_ID>_<PROMPT_ID>.wav`.
-   [ ] Prompt IDs have not been changed.
-   [ ] I did not use my personal name in filenames.
-   [ ] I checked that all 40 recordings play correctly.
-   [ ] I kept a backup of the original/raw recordings.
-   [ ] I ran `git pull origin main`.
-   [ ] I copied files only to my speaker folder.
-   [ ] I staged only my speaker folder.
-   [ ] I checked `git status` before committing.
-   [ ] I pushed to `main` without force-pushing.

------------------------------------------------------------------------

## Quick Upload Reference

Replace `01` with your assigned speaker number.

``` powershell
cd D:\Movio_Custom_Recordings

git pull origin main

Copy-Item `
"D:\TTS_Datasets\Custom_Raw\speaker_01\*.wav" `
".\custom\speaker_01\" `
-Force

(Get-ChildItem ".\custom\speaker_01\*.wav").Count

git status
git add custom/speaker_01
git status
git commit -m "Add S01 custom speech recordings"
git push origin main
```

Expected WAV count before upload:

``` text
40
```

------------------------------------------------------------------------

## Naming Rule to Remember

``` text
CUS_S01_TA001.wav
CUS_S02_EN001.wav
CUS_S03_TG001.wav
CUS_S04_TR001.wav
```

**Custom + Speaker ID + Original Prompt ID + `.wav`**

Keeping this convention unchanged is essential for matching recordings
with prompts and metadata during TTS evaluation.
