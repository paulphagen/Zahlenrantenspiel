import streamlit as st
import random
import pandas as pd


# ---------------------------------
# RESET FUNKTION
# ---------------------------------
def neues_spiel():
    st.session_state.zahl = random.randint(1, 100)
    st.session_state.versuche = 0
    st.session_state.verlauf = []
    st.session_state.min_grenze = 1
    st.session_state.max_grenze = 100


# ---------------------------------
# SESSION INITIALISIERUNG
# ---------------------------------
if "zahl" not in st.session_state:
    neues_spiel()
    st.session_state.einsatz = 0.0
    st.session_state.spiel_aktiv = False


st.title("🎮 Zahlenratespiel Web Edition")


# ---------------------------------
# SPIEL STARTEN
# ---------------------------------
if not st.session_state.spiel_aktiv:

    einsatz = st.number_input(
        "Wie viel möchtest du setzen?",
        min_value=1.0,
        step=1.0
    )

    if st.button("Spiel starten"):
        st.session_state.einsatz = float(einsatz)
        st.session_state.spiel_aktiv = True
        st.rerun()


# ---------------------------------
# SPIEL LÄUFT
# ---------------------------------
if st.session_state.spiel_aktiv:

    st.markdown(f"### 🔢 Versuche: {st.session_state.versuche}")

    with st.form("rate_form", clear_on_submit=True):
        tipp_text = st.text_input("Dein Tipp (1-100)")
        submitted = st.form_submit_button("Raten (Enter drücken)")

    if submitted:

        if tipp_text.strip() == "":
            st.warning("Bitte eine Zahl eingeben!")

        else:
            try:
                tipp = int(tipp_text)

                if 1 <= tipp <= 100:

                    st.session_state.versuche += 1

                    if tipp < st.session_state.zahl:
                        st.info("📈 Größer!")
                        st.session_state.min_grenze = max(
                            st.session_state.min_grenze, tipp + 1
                        )
                        ergebnis = "Zu klein"

                    elif tipp > st.session_state.zahl:
                        st.info("📉 Kleiner!")
                        st.session_state.max_grenze = min(
                            st.session_state.max_grenze, tipp - 1
                        )
                        ergebnis = "Zu groß"

                    else:
                        st.success("🎉 Richtig!")
                        ergebnis = "Richtig"

                    st.session_state.verlauf.append({
                        "Versuch": st.session_state.versuche,
                        "Tipp": tipp,
                        "Ergebnis": ergebnis
                    })

                else:
                    st.warning("Zahl muss zwischen 1 und 100 liegen!")

            except ValueError:
                st.error("Bitte eine gültige ganze Zahl eingeben!")

    # ---------------------------------
    # BEREICH & FORTSCHRITT (JETZT RICHTIG PLATZIERT)
    # ---------------------------------
    st.markdown(
        f"### 📏 Aktueller Bereich: "
        f"{st.session_state.min_grenze} – {st.session_state.max_grenze}"
    )

    gesamtbereich = 100
    aktueller_bereich = (
        st.session_state.max_grenze - st.session_state.min_grenze
    )

    progress = 1 - (aktueller_bereich / gesamtbereich)
    st.progress(progress)

    # ---------------------------------
    # GEWINN LOGIK
    # ---------------------------------
    if st.session_state.verlauf:
        letzter = st.session_state.verlauf[-1]

        if letzter["Ergebnis"] == "Richtig":

            if st.session_state.versuche > 6:
                rueckgeld = st.session_state.einsatz * 0.5
            elif st.session_state.versuche < 6:
                rueckgeld = st.session_state.einsatz * 1.5
            else:
                rueckgeld = st.session_state.einsatz

            st.write(f"💰 Auszahlung: {rueckgeld:.2f} €")

            if st.button("Neues Spiel starten"):
                neues_spiel()
                st.rerun()

    # ---------------------------------
    # VERLAUF
    # ---------------------------------
    if st.session_state.verlauf:

        st.subheader("📊 Spielverlauf")
        df = pd.DataFrame(st.session_state.verlauf)

        def farbe(val):
            if val == "Richtig":
                return "background-color: lightgreen"
            elif val == "Zu klein":
                return "background-color: lightblue"
            elif val == "Zu groß":
                return "background-color: lightcoral"
            return ""

        styled_df = df.style.applymap(farbe, subset=["Ergebnis"])
        st.dataframe(styled_df, use_container_width=True)
