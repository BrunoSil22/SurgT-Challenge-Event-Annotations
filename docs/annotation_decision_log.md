This document records annotation decisions for ambiguous or low-visibility
cases, providing the rationale for assigning the *Other* label or selecting
one event class over plausible alternatives.

---
### Instance: Validation/case_2_3
**JSON annotation file:** `annotations/Validation/case_2_3_events.json`  

- **Annotated event:** Other (frames 435-442)
- **Rationale:**
  During frames 435–442, the target point reappears after a period of occlusion caused by the instrument. The target point is a vessel intersection forming a distinct Y-shaped structure. Due to the pressure exerted by the instrument on the tissue during the occlusion, blood flow in the upper-right vessel branch is temporarily suppressed, resulting in reduced red coloration. Additionally, the close proximity of the instrument introduces surface reflections.
  For these reasons, the frames were labeled as *Other*. However, they could also reasonably be labeled as *Instrument Occlusion*, since they result from the preceding instrument interaction.

---


### Instance: Validation/case_3_1
**JSON annotation file:** `annotations/Validation/case_3_1_events.json`  

- **Annotated event:** Smoke (frames 458-463)
- **Rationale:**
   During frames 458–463, the target point is located in a region affected by smoke generated from the bipolar action. The instrument remains close to the target point, and its shadow combined with the smoke reduces the visibility of tissue features. 
  For this reason, these frames were labeled as *Smoke*. However, they could also reasonably be labeled as *Other* due to the combined effect of shadow and smoke.

---
- **Annotated event:** Other (frames 486-557)
- **Rationale:**
  During frames 486-557, the target point enters a poorly illuminated region of the scene, making it difficult to reliably distinguish tissue features.
  For this reason, these frames were labeled as *Other*.


