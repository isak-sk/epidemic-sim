# Todo



---

## **1. Förberedelse**

* [ ] Sätt upp Python-miljö (NumPy, Matplotlib, ev. Pygame eller Streamlit)
* [ ] Definiera projektets mål: agentbaserad SIR + jämförelse med matematisk SIR

---

## **2. Agentbaserad simulering**

* [ ] Skapa `Person`-klass med:

  * position (x, y)
  * hastighet (vx, vy)
  * status: S/I/R
  * infektionstid
* [ ] Skapa population (lista med individer)
* [ ] Sätt en person som smittad (“patient zero”)
* [ ] Skriv `move()`-funktion:

  * individer rör sig i 2D-plan
  * studsar mot kanter
* [ ] Skriv `infect()`-funktion:

  * smitta sker om två individer är nära
  * använd sannolikhet (`INFECTION_PROB`)
* [ ] Skriv `update_recovery()`:

  * öka infektionstid
  * byt till R efter `RECOVERY_TIME`

---

## **3. Datainsamling**

* [ ] Räkna antal S, I, R varje tidssteg
* [ ] Spara historik för plotting
* [ ] Rita SIR-kurvor (Matplotlib)

---

## **4. Matematisk SIR-modell**

* [ ] Implementera diskret SIR-modell i Python:

  * S, I, R
  * β (smittspridning), γ (recovery rate)
* [ ] Kör samma antal steg som agent-simuleringen
* [ ] Rita kurvor överlag med agentbaserad simulering
* [ ] Diskutera skillnader mellan modellerna

---

## **5. Koppling mellan modellerna**

* [ ] Estimera γ från agent-simulering (`1/RECOVERY_TIME`)
* [ ] Estimera β från agent-simulering (nya infektioner → β ≈ N·new_infections / (S·I))
* [ ] Beräkna R₀ = β / γ
* [ ] Visa R₀ i graf/GUI

---

## **6. Visualisering / “cool faktor”**

* [ ] Rita cirklar: blå = S, röd = I, grön = R
* [ ] Lägg till live-uppdatering av SIR-graf under simulering
* [ ] (Valfritt) Använd Streamlit/Tkinter för sliders:

  * population
  * β
  * γ
  * startantal smittade
* [ ] (Valfritt) Kluster-effekt: små variationer i hastighet → smitta sprids mer naturligt

---

## **7. Analys och rapport**

* [ ] Beskriv SIR-matematik
* [ ] Visa agentbaserad simulering
* [ ] Visa SIR-kurvor från båda modellerna
* [ ] Diskutera:

  * skillnader
  * slumpens påverkan
  * varför agentmodellen ser mer realistisk ut
* [ ] Summera resultat och slutsats

---
