# SurgT Event Types and Annotation Guidelines

This document defines the event types used in the **SurgT-Challenge-Event-Annotations** repository and provides annotation guidelines for tracking target points (defined as the center of each bounding box).

These annotations were created to enable **event-aware evaluation** of laparoscopic tracking methods and support the analysis of the **IMI-Tracker** method presented in:

*"IMI-Tracker: A Real-Time Two-Stage Tracker with Motion Inpainting for Soft Tissue Tracking under Instrument Occlusion."*

---

## General Annotation Principles
- Events are labeled with respect to the target point (defined as the center of each bounding box).
- Events are labeled by their **start and end frames**.
- If an event occurs in any view (left or right), the frame is labeled as containing that event.
- Only **challenging frames** are annotated; absence of an event does not imply ideal conditions.
- Events may **overlap in time** (e.g., instrument occlusion while the target is partially out of frame).
- Frame indices are **zero-based** and `start_frame` and `end_frame` are **inclusive**.

---

## Event Taxonomy

| Code  | Name                  | Definition                                                                                 | Notes / Edge Cases                                 |
|-------|----------------------|--------------------------------------------------------------------------------------------|---------------------------------------------------|
| `i_o` | Instrument Occlusion  | Partial or full occlusion of the target point by surgical instruments                     | Excludes occlusion caused primarily by tissue or needle |
| `g_o` | Gauze Occlusion       | Occlusion of the target point caused by a gauze                                           |                                                   |
| `n_o` | Needle Occlusion      | Occlusion of the target point by a surgical needle or suture material                     |                                                   |
| `o_o` | Organ Occlusion       | Occlusion caused by anatomical structures (e.g., organs or tissue)                        |                                                   |
| `o_f` | Out of Frame          | The target point partially or fully leaves the image frame                                |                                                   |
| `f`   | Fast Movement         | Rapid motion of the camera or target causing large inter-frame displacement or motion blur |                                                   |
| `d`   | Deformation           | Significant non-rigid deformation of the target point that alters its appearance          |                                                   |
| `s`   | Smoke                 | Presence of smoke that reduces visibility of the target point                              |                                                   |
| `o`   | Other                 | Challenging conditions not covered by the predefined categories (example: specular highlights) | Use sparingly; only when no other category applies |

---

## Overlapping Events

- Events are **not mutually exclusive**.
- Multiple events can occur at the same frame interval, reflecting realistic surgical scenarios.
---

## Intended Use

These annotations are intended for:
- Robustness evaluation of tracking methods
- Ablation studies under specific challenges (e.g., occlusion, out-of-frame)
