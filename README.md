# Spec-Driven Development with Antigravity & the Elephant-Goldfish Model (EGM)

Hands-on workshop and presentation materials for **Spec-Driven Development (SDD)** using **Google Antigravity** and the open-source **[Elephant-Goldfish Model (EGM)](https://github.com/google/elephant-goldfish-model)** plugin.

---

## 🚀 Live Interactive Codelab

Follow the interactive, step-by-step Google Codelab in your browser:

* **Cloud Run Codelab**: [https://sdd-egm-codelab-1010474272420.southamerica-east1.run.app](https://sdd-egm-codelab-1010474272420.southamerica-east1.run.app)
* **GitHub Pages Codelab**: [https://alvardev.github.io/sdlc-egm/](https://alvardev.github.io/sdlc-egm/)

---

## 📂 Repository Structure

```text
sdlc-egm/
├── README.md                  # Repository overview & live Codelab links
├── docs/                      # Compiled interactive HTML Codelab (GitHub Pages & Cloud Run)
│   └── index.html
├── codelab/                   # Codelab Markdown source & Cloud Run static Go server
│   ├── codelab.md             # Google Codelabs (claat) Markdown source
│   ├── Dockerfile             # Multi-stage Google Distroless Dockerfile
│   ├── go.mod                 # Go module definition
│   └── server.go              # Go standard-library static HTTP server
├── guides/                    # Markdown guides for attendees and speaker
│   ├── WORKSHOP_GUIDE.md      # Step-by-step GitHub Markdown backup for attendees
│   └── SPEAKER_GUIDE.md       # 30-min presentation outline & 60-min facilitator runbook
└── reference-app/             # Golden reference checkpoint of the "RetroPulse" app
    ├── docs/
    │   └── designs/
    │       └── retropulse.md  # Approved EGM design specification
    ├── main.py                # FastAPI backend (Python + uv)
    ├── static/
    │   └── index.html         # 3-column vanilla HTML/CSS/JS frontend
    └── Dockerfile             # Multi-stage Python + uv Distroless Dockerfile
```

---

## 📖 Quick Links

* **[Attendee Step-by-Step Guide (Markdown Backup)](./guides/WORKSHOP_GUIDE.md)**
* **[Speaker & Facilitator Guide (30m Talk + 60m Workshop)](./guides/SPEAKER_GUIDE.md)**
* **[Codelab Source (`claat` Markdown)](./codelab/codelab.md)**
* **[Golden Reference App (`RetroPulse`)](./reference-app/)**
