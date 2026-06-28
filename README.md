# LM2 / LZ0 Duramax 3.0 — Custom Oil Cooler Install

A reference project for designing and installing an external oil cooler on the Chevrolet Duramax 3.0 diesel engine (LM2 and LZ0 variants found in the Silverado 1500, Sierra 1500, Suburban, Tahoe, Yukon, and Escalade).

---

## Contents

- [Overview](#overview)
- [Engine Background](#engine-background)
- [Approach Options](#approach-options)
- [Oil Filter Adapter — Custom Machined](#oil-filter-adapter--custom-machined)
- [Sandwich Adapters](#sandwich-adapters)
- [Oil Cooler Core Recommendations](#oil-cooler-core-recommendations)
- [Plumbing & Hardware](#plumbing--hardware)
- [CAD Files](#cad-files)
- [Contributing](#contributing)

---

## Overview

The LM2/LZ0 3.0L inline-six diesel runs relatively hot oil under tow and performance conditions. Adding an external oil cooler extends oil life, reduces thermal degradation, and helps protect the turbocharger and emission systems that depend on oil for cooling and lubrication.

This repo covers three integration paths:

| Path | Description | Difficulty |
| ------ | ------------- | ------------ |
| Sandwich adapter | Bolt-on plate between block and filter | Easy |
| Custom machined adapter | Precision adapter replacing the OEM filter housing port | Intermediate |
| Remote filter relocation | Full relocation of the filter + cooler | Advanced |

---

## Engine Background

| Spec | LM2 | LZ0 |
| ------ | ----- | ----- |
| Displacement | 3.0L I6 | 3.0L I6 |
| Power | 277 hp | 305 hp |
| Torque | 460 lb-ft | 495 lb-ft |
| Block | Cast iron | Cast iron |
| Introduced | 2019 | 2022 |
| Filter thread | 1"-16 UNF | 1"-16 UNF |

Both engines share the same oil filter thread pitch (1"-16 UNF — the same spec used by the Ford Power Stroke 6.5) and filter housing location, making adapter designs interchangeable between the two variants.

---

## Approach Options

### 1. Sandwich Adapter (simplest)

A sandwich-style adapter installs between the engine block oil filter boss and the existing oil filter. It adds two AN fittings for feed and return lines to an external cooler. No machining required.

### 2. Custom Machined Adapter (this repo's primary focus)

A billet aluminum adapter replaces or augments the OEM filter boss interface. This allows for:

- Larger port sizing
- Integrated thermostat ports
- Precise AN fitting placement
- Cleaner routing with no stacking height issues

See the [CAD Files](#cad-files) section for drawings and specs.

### 3. Remote Filter Relocation

Full relocation moves the filter away from the block entirely. Useful when clearance is tight or when combining an oil cooler with an upgraded remote filter.

---

## Oil Filter Adapter — Custom Machined

The custom adapter is designed to thread onto the OEM 1"-16 UNF filter boss and provide dual AN-10 ports for external cooler lines.

### Design Requirements

- Thread: **1"-16 UNF** male (mates to block boss)
- Female thread: **1"-16 UNF** to accept OEM-spec filter
- Port size: **-10 AN** (minimum; -12 AN preferred for low restriction)
- Material: **6061-T6 or 7075-T6 billet aluminum**
- O-ring seat: OEM-compatible (Viton recommended)
- Pressure rating: minimum **150 PSI**
- Integrated check valve port: optional but recommended

### Machining Notes

- Face seal on block side must be flat to within **0.002"**
- Port placement should allow hose routing away from the exhaust and turbo
- Anodize or hard-coat finish recommended for heat and corrosion resistance
- CAD files provided in `/cad/` as `.step` and `.dxf` formats

---

## Sandwich Adapters

Off-the-shelf sandwich adapters that fit the LM2/LZ0 1"-16 UNF thread:

| Brand | Model | Ports | Thermostat | Notes |
| ------- | ------- | ------- | ------------ | ------- |
| Mocal | SO7/1 | -8 AN | Optional | Popular, well-proven |
| Setrab | SAN812 | -8 AN | No | Budget option |
| Derale | 25750 | -8 AN | No | Widely available |
| Earls | AT1099ERL | -10 AN | No | Larger ports |
| Mishimoto | MMOC-UA | -10 AN | No | Good fitment on 1500 trucks |

> **Tip:** Prefer adapters with a built-in thermostat bypass or add a separate inline thermostat. Sending cold oil through an external cooler at startup increases wear.

---

## Oil Cooler Core Recommendations

### Sizing Guidelines

| Use Case | Recommended Core Size |
| ---------- | ----------------------- |
| Daily driver / light tow | 13-row, 4" wide |
| Regular towing (≤80% GCWR) | 19-row, 4" wide |
| Heavy tow / competition | 25-row or stacked-plate |

### Recommended Cores

| Brand | Model | Rows | Port Size | Type |
| ------- | ------- | ------ | ----------- | ------ |
| Setrab | 50-series 6119 | 19-row | -10 AN | Tube & fin |
| Mocal | OC-19 | 19-row | -8 AN | Tube & fin |
| Derale | 15503 | 25-row | -8 AN | Tube & fin |
| CSF | 8178 | Stacked plate | -10 AN | High efficiency |
| Mishimoto | MMOC-25 | 25-row | -10 AN | Tube & fin |

### Placement Notes

- Mount in airflow path — ahead of the AC condenser or in a functional bumper opening
- Avoid mounting directly behind the radiator where heat soak will reduce efficiency
- Allow at least 1" clearance from any surface for airflow
- Orient ports to minimize hose length and avoid tight bends

---

## Plumbing & Hardware

- **Hose:** -10 AN braided stainless / PTFE-lined (Earl's, Fragola, or Goodridge)
- **Fittings:** Straight and 45° -10 AN at the adapter; 90° at the core to ease routing
- **Inline thermostat:** Mocal TK222 or Davies Craig unit — opens at ~180°F (82°C)
- **Mounting:** Vibration-isolating rubber mounts for the core; avoid rigid direct mounts
- **Lines:** Keep total line length under 48" each way to minimize volume and pressure drop

---

## CAD Files

> CAD files will be added to the `/cad/` directory.

Planned deliverables:

- [ ] Custom adapter — STEP file
- [ ] Custom adapter — DXF (2D drawing with tolerances)
- [ ] Custom adapter — PDF drawing (print-ready for machinist)
- [ ] Sandwich adapter drilling template
- [ ] Core mount bracket — STEP file

---

## Contributing

PRs and issues welcome. If you have dyno data, install photos, or machining feedback, open an issue or submit a pull request.
