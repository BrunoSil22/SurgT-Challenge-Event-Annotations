# SurgT Event Annotations for Robustness Analysis

This repository provides **frame-level annotations of challenging tracking events** (e.g., occlusions, fast motion, out-of-frame, etc) for the validation and test subsets of the **SurgT dataset**. 

The annotations enable **event-aware evaluation** of laparoscopic tracking methods and were created to support the analysis of the **IMI-Tracker** method presented in:

*"IMI-Tracker: A Real-Time Two-Stage Tracker with Motion Inpainting for Soft Tissue Tracking under Instrument Occlusion."*

The repository contains:
- JSON annotation files (one per video)
- Python script to compute per-event statistics consistent with tables in the paper

The original SurgT dataset and benchmarking toolkit (“SurgT_benchmarking”) provide a standard benchmark for soft-tissue trackers.  
See the repository for dataset access and evaluation scripts:  
https://github.com/Cartucho/SurgT_benchmarking

---

## Purpose

Standard tracking metrics often average performance over heterogeneous conditions, masking failure modes such as occlusions or fast motion.  
These annotations enable **fine-grained evaluation**, allowing performance to be analyzed per event type.

Typical use cases include:
- Event-based robustness analysis
- Ablation studies under specific challenges (e.g., occlusion, out-of-frame)

---

## Repository Structure
```
.
├── annotations/
│ ├── Validation/
│ │ ├── case_1_1_events.json
│ │ └── ...
│ ├── Test/
│ │ ├── case_1_1_events.json
│ │ └── ...
├── analise_events.py
├── README.md
├── EVENTS.md
├── CITATION.cff
└── LICENSE
```
---

## Annotation Files

- One JSON file per video
- File naming convention: `<video_id>_events.json`

For detailed definitions of all event types and annotation guidelines, see [EVENTS.md](EVENTS.md).

### JSON schema (simplified)

```json
{
  "video_id": "case_x_y",
  "dataset": "SurgT",
  "anchors": [ ... ],
  "events": [
    {
      "type": "i_o",
      "start_frame": 25,
      "end_frame": 144
    }
  ]
}
```
### Notes
- If an event occurs in any view (left or right), the frame is labeled as containing that event.
- Frame indices are zero-based
- `start_frame` and `end_frame` are inclusive
- Only challenging events are annotated; absence of an event does not imply ideal conditions

---

## Event Overlap

Events are **not mutually exclusive**.

Multiple events may overlap in time (e.g., instrument occlusion occurring while the target is partially out of frame).

---
## Statistics Script

The `scripts/analise_events.py` script:
- Parses all annotation files
- Computes per-event frame counts and distributions
- Generates the statistics reported in the paper


---
## License

The annotations and scripts are released under a permissive license (see `LICENSE`).
This license applies **only to the annotation metadata**, not to SurgT video data.

---
## Citation

If you use these annotations, please cite the associated paper and this repository (see `CITATION.cff`).