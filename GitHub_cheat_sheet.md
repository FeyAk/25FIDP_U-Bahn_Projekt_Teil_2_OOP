# GitHub-Workflow

Zusammenstellung der **wichtigsten GitHub Begriffe** und eine kurze **Workflow-Anleitung**, wie wir in dem Bilderkenner-Projekt arbeiten wollen:

---

Fork:=
Eine **Kopie eines Repositories**, die unabhängig vom Original entwickelt werden kann. Wird oft genutzt, um Änderungen vorzuschlagen oder eigene Experimente durchzuführen, ohne das Originalprojekt zu verändern.

Origin:=
**dein eigener Remote** — das Repo, das du geklont hast und die Qulle für deine Branches

Upstream:=
**das Repo, von dem man Updates bezieht** (meist das Hauptprojekt, nicht der eigene Fork).

Branch:=
**Arbeitsbereich** in dem neue **Features** erstellt werden --> wird via pull-request (PR) zum Upstream gebracht.

Pull Request:=
**Eine Anfrage**, um **Änderungen aus einem Branch** in einen anderen (meist Upstream) **zu übernehmen**. Er ermöglicht Code-Review, Diskussion und automatische Tests, bevor der Code gemerged wird.

Merge:=
**Das Zusammenführen** von Änderungen aus einem Branch in einen anderen. Dabei kombiniert Git die unterschiedlichen Versionsstände und erstellt bei Bedarf einen neuen Merge-Commit.

Squash:=
Das **Zusammenfassen mehrerer Commits** zu einem einzigen Commit, um eine aufgeräumte und übersichtliche Versionsgeschichte zu erhalten. (man braucht nicht jedes detailierte Update der Entwicklung, wenn man ein neues Feature in main bringt)

Rebase:=
Ein Vorgang, bei dem die Basis eines Branches auf einen anderen Commit verschoben wird, um eine lineare, saubere Historie zu erzeugen. **Achtung!** Hier kann man die Historie verändern und das Repos unbrauchbar machen!

Cherripicking:=
Das gezielte Übernehmen einzelner Commits aus einem Branch in einen anderen, ohne alle Änderungen des Quell-Branches zu mergen. Meist nur bei komplexen Kollaborationen mit verschiedenen Versionen.

Add:=
file aus dem lokalen Arbeitsverzeichnis wird dem Repository zum tracken hinzugefügt

Tracken:= 
Verknüpfung zwischen lokalem und Remote-Branch zur Synchronisation.

Commit:= 
Eine **gespeicherte Änderung im Git-Repository**, die den aktuellen Stand von Dateien zusammen mit einer Nachricht dokumentiert. Jeder Commit hat eine eindeutige Kennung (Hash) und bildet einen Punkt in der **Versionsgeschichte**.

---

# Workflow:

1️. Fork Original-Repo → origin, lokal clonen  
2️. Branch erstellen: 
	`git switch -c feature-xyz`  
3️. Änderungen committen & pushen:  
	`git add . && git commit -m "feat: msg" && git push -u origin feature-xyz`  
4️. PR erstellen: feature-branch → upstream/main, reviewen  
5️. Nach Merge: Feature-Branch löschen:  
	`git branch -d feature-xyz && git push origin --delete feature-xyz`  
6️. Fork aktuell halten:  
	`git fetch upstream && git checkout main && git merge upstream/main && git push origin main`  
   
Best Practices: 1 Branch = 1 Feature, main sauber halten, PRs klein & übersichtlich


**Quellen:**
 - [Merge-Rebase-Cherrypicking](https://www.youtube.com/watch?v=pgibfECuS2Y)
 - [Branch-Strategien](https://www.youtube.com/watch?v=yFs7SzirMQs)
 - [How Git Works: Explained in 4 Minutes](https://www.youtube.com/watch?v=e9lnsKot_SQ "https://www.youtube.com/watch?v=e9lnskot_sq")