# Problem Statement

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
> "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
> "OPTIONAL" in this document are to be interpreted as described in
> [BCP 14](https://www.rfc-editor.org/info/bcp14)
> [[RFC 2119]](https://datatracker.ietf.org/doc/html/rfc2119)
> [[RFC 8174]](https://datatracker.ietf.org/doc/html/rfc8174)
> when, and only when, they appear in all capitals, as shown here.

---

## Background

Chevrolet's 3.0L inline-six diesel — the LM2 (2019–2021) and its refined successor the LZ0 (2022–present) — is a well-engineered powertrain for a half-ton and three-quarter-ton light truck platform. Shared across the Silverado 1500, Sierra 1500, Suburban, Tahoe, Yukon, and Escalade, it delivers diesel efficiency and torque in a package that competes directly with gasoline V8s on towing capability and significantly outpaces them on fuel economy.

The engineering is sound. The concerns documented here are not a critique of the platform — they are observations about sustained thermal loads under real-world conditions that Chevrolet's factory calibration and cooling infrastructure appear to have treated as acceptable, but that a conscientious long-term owner SHOULD treat as elevated.

---

## Test Vehicles

This work is grounded in direct ownership experience across two vehicles:

| Vehicle | Year | Trim | Engine | Transmission |
| ------- | ---- | ---- | ------ | ------------ |
| Chevrolet Silverado 1500 | 2023 | LTZ | 3.0L Duramax LZ0 | 10L80E |
| Chevrolet Suburban | 2025 | Z71 | 3.0L Duramax LZ0 | 10L80E |

Both vehicles are monitored continuously with a **Banks iDash** data monitor tracking:

- **EOT** — Engine Oil Temperature
- **TRNST** — Transmission Fluid Temperature
- **EGT** — Exhaust Gas Temperature (multiple channels)
- **Soot Load** — diesel particulate filter loading percentage
- **Regen Status** — active DPF regeneration state and frequency

EGT and regen monitoring are used to confirm that DPF regenerations are completing within specification and to identify any indication of a hung or leaking injector contributing to uncontrolled regeneration events.

---

## The Thermal Problem

### Engine Oil Temperature (EOT)

Under non-towing, highway conditions on flat terrain in Florida — even during winter months when ambient temperatures are mild — EOT on both vehicles consistently hovers near **240°F**. This is not under load. This is not towing. This is steady-state cruising on a flat road in relatively cool ambient conditions.

The Duramax LZ0 does not ship with an external engine oil cooler from the factory. Oil cooling is handled entirely through the internal water-cooled oil cooler integrated into the engine block. At sustained highway speeds, this system reaches thermal equilibrium at temperatures that sit at the upper boundary of what most synthetic oil manufacturers consider normal operating range, and well above what many consider optimal for long-term viscosity stability and additive life.

### Transmission Temperature (TRNST)

The 10-speed automatic transmission in these vehicles — the GM 10L80E, co-developed with Ford — is known within the enthusiast community as a unit that runs hot. Under the same non-towing, flat highway conditions described above, TRNST on both vehicles runs between **200°F and 220°F**. Under light tow loads, temperatures climb further.

GM's factory transmission cooling system routes fluid through the radiator. This is adequate for most conditions, but the radiator is already managing coolant for the engine, and in warm ambient conditions the thermal margin available to the transmission cooler circuit is limited.

---

## Observed Operating Temperature Matrix

The table below captures observed steady-state temperatures across representative operating conditions, both before and after the thermal management modifications described in this repository.

Conditions represent typical Florida driving unless otherwise noted. All temperatures in °F.

### EOT — Observed Readings

| Condition | Ambient | Stock EOT | Target EOT | Status |
| --------- | ------- | --------- | ---------- | ------ |
| Idle / parking lot | Any | 180–200 | 180–200 | Normal |
| Highway cruise, flat, no load | 55–75°F | ~240 | 200–220 | **Elevated** |
| Highway cruise, flat, no load | 85–95°F | 245–255 | 200–220 | **High** |
| Light tow (≤50% GCWR), flat | 75–85°F | 255–265 | 210–230 | **High** |
| Heavy tow (≥75% GCWR) or grades | Any | 265–285+ | 220–240 | **Concerning** |

### TRNST — Observed Readings

| Condition | Ambient | Stock TRNST | After Mods TRNST | Target | Status (Stock) |
| --------- | ------- | ----------- | ---------------- | ------ | -------------- |
| Idle / parking lot | Any | 160–180 | 160–175 | 160–185 | Normal |
| Highway cruise, flat, no load | 55–75°F | 200–220 | 175–195 | 175–200 | **Elevated** |
| Highway cruise, flat, no load | 85–95°F | 215–235 | 180–200 | 175–200 | **High** |
| Light tow (≤50% GCWR), flat | 75–85°F | 225–245 | 185–210 | 185–210 | **High** |
| Heavy tow (≥75% GCWR) or grades | Any | 250–270+ | 200–225 | 185–215 | **Concerning** |

> **Note on cold-weather operation:** Both the transmission thermostat bypass and the external oil cooler thermostat are designed to hold fluid in the bypass circuit until the fluid reaches operating temperature. Neither modification sacrifices cold-weather warm-up time.

---

## Why This Matters

Engine oil at sustained 240°F+ degrades faster than at 210–220°F — the difference is not linear. For every 18°F above optimal operating temperature, oil oxidation rate approximately doubles. At 240°F steady-state, a 7,500-mile oil change interval effectively carries the thermal load of a significantly shorter interval at lower temperatures. For vehicles used for regular towing or operated in warm climates year-round, this has compounding long-term consequences for engine wear.

Transmission fluid is under similar pressure. The 10L80E is not a fragile transmission, but high sustained fluid temperatures accelerate clutch pack wear and friction material degradation — failures that are expensive and, in a platform this new, poorly documented in long-term reliability data.

---

## Transmission Solution — What Was Done

The transmission thermal problem was addressed on both vehicles using a cobbled-together but effective combination of off-the-shelf parts:

1. **PPE Deep Transmission Pan** — adds approximately four quarts of fluid volume over factory, increasing thermal mass and heat dissipation surface area.
   [PPE Deep Pan at Demon Workshop](https://www.demonworkshop.com/collections/3-0-duramax-diesel-lm2-lz0)

2. **PPE Transmission Thermal Bypass Valve** — replaces the factory thermostat with a unit that opens earlier, routing fluid to the external cooler at lower temperatures.
   [PPE Thermal Bypass at Demon Workshop](https://www.demonworkshop.com/products/2020-2025-gm-3-0l-w-10l80-transmission-transmission-fluid-thermal-bypass-valve)

3. **Mishimoto External Transmission Cooler** — front-mounted cooler providing dedicated transmission cooling independent of the radiator:
   - Suburban (2025): [MMTC-T1-21](https://www.mishimoto.com/fits/chevrolet/suburban/2025/p/MMTC-T1-21/transmission-cooler-chevy-tahoe-gmc-yukon-2021.html)
   - Silverado 1500 (2023): [MMTC-T1-19](https://www.mishimoto.com/fits/chevrolet/silverado-1500/2023/p/MMTC-T1-19/transmission-cooler-chevy-silverado-1500-2019.html)

4. **Amsoil Signature Series ULV Synthetic ATF** — full synthetic fluid with a higher film strength and broader temperature stability range than the factory fill.
   [Amsoil ULV ATF](https://www.amsoil.com/p/amsoil-signature-series-ulv-100-synthetic-automatic-transmission-fluid-ulv/?code=ULVPK-EA)

The result is a meaningful and measurable reduction in TRNST across all operating conditions (see matrix above). The parts are readily available, fitment is straightforward, and the combination works.

---

## Engine Oil Cooling — The Gap This Repo Fills

No equivalent plug-and-play oil cooler solution existed for the LM2/LZ0 at the time this work began. Unlike the transmission, which had documented aftermarket support, the engine oil cooling problem required starting from the adapter up.

This repository documents:

1. A **sandwich plate adapter** approach using off-the-shelf adapters on the OEM filter boss — the simplest path to an external oil cooler.
2. A **custom-machined billet adapter** for a cleaner, more permanent installation with better port sizing and routing options.
3. Core selection, plumbing, thermostat integration, and mounting recommendations specific to the LM2/LZ0 platform.

The goal is a documented, repeatable solution that any LM2 or LZ0 owner can replicate without starting from scratch.
