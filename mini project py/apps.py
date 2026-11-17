import json
import os
import time

FICHIER_DONNEES = "etudiants.json"
etudiants = []

# ── Bonus : Sauvegarder et Charger ──────────────────────────────────────────
def charger_donnees():   #tatchof wch kyn lfcher 
    global etudiants  #إلا كان كاين → كتقرا شنو فيه وكتحطو فـ etudiant
    if os.path.exists(FICHIER_DONNEES): #إلا كان فيه مشكل (فارغ ولا خاسر) → كتخلي etudiants = []
        with open(FICHIER_DONNEES, "r", encoding="utf-8") as f:
            try:
                etudiants = json.load(f)
            except json.JSONDecodeError:
                etudiants = []

def sauvegarder_donnees():  #وكتكتبهم فـ الملف بصيغة JSON
    with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
        json.dump(etudiants, f, indent=4, ensure_ascii=False)


# ── 1. Ajouter un étudiant ──────────────────────────────────────────────────
def ajouter_etudiant():
    print("\n── Ajouter un étudiant ──")
    nom = input("Nom de l'étudiant : ").strip()
    if nom == "":
        print("❌ Le nom ne peut pas être vide.")
        return
    for e in etudiants:
        if e["nom"].lower() == nom.lower():
            print("❌ Cet étudiant existe déjà.")
            return
            
    notes = []
    print("Entrez les notes de l'étudiant (tapez 'fin' pour terminer).")
    while True:
        saisie = input("Entrez une note : ").strip().lower()
        if saisie == "fin":
            break
        try:
            note = float(saisie)
            if 0 <= note <= 20:
                notes.append(note)
            else:
                print("❌ La note doit être entre 0 et 20.")
        except ValueError:
            print("❌ Saisie invalide, entrez un nombre ou 'fin'.")
            
    etudiants.append({"nom": nom, "notes": notes})
    print(f"✅ Étudiant '{nom}' ajouté avec {len(notes)} note(s).")
    sauvegarder_donnees()  # auto-save


# ── 2. Afficher tous les étudiants
def afficher_etudiants():
    print("\n── Liste des étudiants ──")
    if not etudiants:   #talib wch kyn wla la
        print("Aucun étudiant enregistré.")
        return
    print(f"{'Nom':<20} {'Notes':<30} {'Moy.':<8} {'Résultat'}")
    print("-" * 75)
    for e in etudiants:
        if e["notes"]:
            moyenne = sum(e["notes"]) / len(e["notes"])
            notes_str = ", ".join(f"{n:g}" for n in e["notes"])  #:g كتحيد .0 إلا كانت النقط صحيحة
            if len(notes_str) > 27:
                notes_str = notes_str[:24] + "..."
            resultat = "✅ Admis" if moyenne >= 10 else "❌ no admis"
            print(f"{e['nom']:<20} {notes_str:<30} {moyenne:<8.2f} {resultat}")
        else:
            print(f"{e['nom']:<20} {'Aucune note':<30} {'--':<8} --")


# ── 3. Rechercher un étudiant
def rechercher_etudiant():
    print("\n── Rechercher un étudiant ──")
    nom = input("Entrez le nom à rechercher : ").strip()
    for e in etudiants:
        if e["nom"].lower() == nom.lower():
            print(f"\n📋 Étudiant : {e['nom']}")
            if not e["notes"]:
                print("   Aucune note enregistrée.")
            else:
                moyenne = sum(e["notes"]) / len(e["notes"])
                notes_str = ", ".join(f"{n:g}" for n in e["notes"])
                print(f"   Notes   : {notes_str}")
                print(f"   Moyenne : {moyenne:.2f}/20")
                print("   Résultat: ✅ Admis" if moyenne >= 10 else "   Résultat: ❌ Ajourné")
            return
    print("❌ Étudiant introuvable.")


# ── 4. Supprimer un étudiant ou une note 
def supprimer_etudiant():
    print("\n── Supprimer un étudiant ou une note ──")
    nom = input("Entrez le nom : ").strip()
    for i, e in enumerate(etudiants):
        if e["nom"].lower() == nom.lower():
            print(f"\nÉtudiant trouvé : {e['nom']}")
            print("  1. Supprimer l'étudiant entièrement")
            print("  2. Supprimer une note")
            print("  0. Annuler")
            choix = input("Votre choix : ").strip()

            if choix == "1":
                confirmation = input(f"Confirmer la suppression de '{e['nom']}' ? (oui/non) : ")
                if confirmation.lower() == "oui":
                    etudiants.pop(i)
                    print(f"✅ Étudiant '{nom}' supprimé.")
                    sauvegarder_donnees()
                else:
                    print("Suppression annulée.")

            elif choix == "2":
                if not e["notes"]:
                    print("❌ Cet étudiant n'a aucune note à supprimer.")
                    return
                print("Notes actuelles :")
                for idx, note in enumerate(e["notes"]):
                    print(f"  {idx}. {note:g}/20")
                try:
                    idx_note = int(input("Entrez le numéro de la note à supprimer : "))
                    if 0 <= idx_note < len(e["notes"]):
                        note_sup = e["notes"].pop(idx_note)
                        print(f"✅ Note {note_sup:g}/20 supprimée.")
                        sauvegarder_donnees()
                    else:
                        print("❌ Numéro invalide.")
                except ValueError:
                    print("❌ Entrez un numéro valide.")

            elif choix == "0":
                print("Annulé.")
            else:
                print("❌ Choix invalide.")
            return
    print("❌ Étudiant introuvable.")


# ── 5. Afficher les statistiques
def afficher_statistiques():
    print("\n── Statistiques générales ──")
    if not etudiants:
        print("Aucun étudiant enregistré.")
        return
        
    toutes_notes = []
    admis = 0
    for e in etudiants:
        toutes_notes.extend(e["notes"])
        if e["notes"] and (sum(e["notes"]) / len(e["notes"])) >= 10:
            admis += 1
            
    if not toutes_notes:
        print("Aucune note dans le système.")
        return
        
    moyenne_globale = sum(toutes_notes) / len(toutes_notes)
    
    print(f"Nombre total d'étudiants : {len(etudiants)}")
    print(f"Élèves admis             : {admis} / {len(etudiants)}")
    print(f"Nombre total de notes    : {len(toutes_notes)}")
    print(f"Moyenne globale de classe: {moyenne_globale:.2f}/20")
    print(f"Meilleure note de classe : {max(toutes_notes):g}/20")
    print(f"Pire note de classe      : {min(toutes_notes):g}/20")


# ── Menu principal
def menu():
    charger_donnees() # Charge les données au lancement
    while True:
        print("\n╔" + "═" * 45 + "╗")
        print("║       GESTION DES NOTES (MINI PROJET)       ║")
        print("╠" + "═" * 45 + "╣")
        print("║                                             ║")
        print("║  [ 1 ] Ajouter un étudiant                  ║")
        print("║  [ 2 ] Afficher tous les étudiants          ║")
        print("║  [ 3 ] Rechercher un étudiant               ║")
        print("║  [ 4 ] Supprimer un étudiant / une note     ║")
        print("║  [ 5 ] Afficher les statistiques (Bonus)    ║")
        print("║  [ 0 ] Quitter                              ║")
        print("║                                             ║")
        print("╚" + "═" * 45 + "╝")
        choix = input("👉 Votre choix : ").strip()

        if choix == "1":
            ajouter_etudiant()
        elif choix == "2":
            afficher_etudiants()
        elif choix == "3":
            rechercher_etudiant()
        elif choix == "4":
            supprimer_etudiant()
        elif choix == "5":
            afficher_statistiques()
        elif choix == "0":
            sauvegarder_donnees() # Sauvegarde finale
            print("Au revoir ! 👋")
            time.sleep(2) 
            break
        else:
            print("❌ Choix invalide, réessayez.")


# ── Lancement
if __name__ == "__main__":
    menu()