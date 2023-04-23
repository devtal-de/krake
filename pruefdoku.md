Muss:
 - Verknüpfungen Inventarsysteme (1:n)
 - Doku Geräteprüfung (s.u.)
 - Auffinden Gerätestandort
 - Manual
 - Aufkleber (unique ID)
	- numerisch / alphanumerisch
	- kein P-Touch, gekaufte Sticker
	- keine URL
 - Nachrüstbarkeit (optionale Features)
 - Rechtemanagement + öffentliche Infos / Login

Kann:
 - Schema Attribute
 - Prüfautomation (Barcode-Scanner / RS232 Gossen)
 - Integritätsprüfung

Prüfdoku:
 - Zeit
 - Prüftyp (E, Leiter, ...)
 - ID
 - Schutzklasse
 - Sichtprüfung
 - Schutzleiterwiderstand
 - Ersatzableitstrom
 - Isolationswiderstand
 - Funktionstest
 - Prüfer
 - Prüfgerät
 => PDF automatisch generieren und abspeichern

User:
 - Fablab-User (fabmanager)
 - Geräte-User
 - Manager (admin Prüforganisation)
 - Prüfer (Rechte!)

Inventarsysteme:
 - Fabmanager
 - Jira Asset-Management
 - Netbox
 - Fienchen 

Schließsysteme:
 - Fabmanager
 - Roseguarden
 - /dev/tal Tür
 - Fienchen
 - Lastschlepper
 => Alles eigene Anforderungen

Anforderungen:
 * für Prüfung relevante Daten aus externem Inventarsystem extrahieren
 * bei Fehlschlag Gerät deaktivieren
