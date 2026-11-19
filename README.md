# Spec-Driven Development with Antigravity & the Elephant-Goldfish Model (EGM)

Hands-on workshop and presentation materials for **Spec-Driven Development (SDD)** using **Google Antigravity** and the open-source **[Elephant-Goldfish Model (EGM)](https://github.com/google/elephant-goldfish-model)** plugin.

---

## 🚀 Live Interactive Codelab & Demo App

Follow the interactive, step-by-step Google Codelabs in your browser:

* **Workshop 1 — Spec-Driven Development & EGM**: [https://alvardev.github.io/sdlc-egm/](https://alvardev.github.io/sdlc-egm/)
* **Workshop 2 — GitLab CI/CD with Antigravity SDK & EGM**: [https://alvardev.github.io/sdlc-egm/gitlab-ci/](https://alvardev.github.io/sdlc-egm/gitlab-ci/)

Try the live **RetroPulse** application on Cloud Run (`southamerica-east1`):

* **RetroPulse v1 (Step 5 Spec)**: [https://retropulse-demo-1010474272420.southamerica-east1.run.app/](https://retropulse-demo-1010474272420.southamerica-east1.run.app/)
* **RetroPulse v2 (Step 6 + Author & Clear Board)**: [https://retropulse-demo-1010474272420.southamerica-east1.run.app/v2](https://retropulse-demo-1010474272420.southamerica-east1.run.app/v2)

---

## 📂 Repository Structure

```text
sdlc-egm/
├── README.md                  # Repository overview & live Codelab links
├── docs/                      # Compiled interactive HTML Codelabs (GitHub Pages)
│   ├── index.html             # Workshop 1: SDD & EGM Codelab
│   └── gitlab-ci/
│       └── index.html         # Workshop 2: GitLab CI/CD & Antigravity SDK Codelab
├── codelab/                   # Codelab Markdown sources & local preview Go server
│   ├── codelab.md             # Workshop 1 (claat) Markdown source
│   ├── gitlab-ci.md           # Workshop 2 (claat) Markdown source
│   ├── Dockerfile             # Multi-stage Google Distroless Dockerfile
│   ├── go.mod                 # Go module definition
│   └── server.go              # Go standard-library static HTTP server
├── guides/                    # Markdown guides for attendees and speaker
│   ├── WORKSHOP_GUIDE.md             # Workshop 1 attendee backup
│   ├── SPEAKER_GUIDE.md              # Workshop 1 facilitator runbook
│   ├── GITLAB_CI_WORKSHOP_GUIDE.md   # Workshop 2 attendee backup
│   └── GITLAB_CI_SPEAKER_GUIDE.md    # Workshop 2 facilitator runbook & GitLab cheat sheet
├── reference-app/             # Workshop 1 golden reference ("RetroPulse")
├── retropulse-starter/        # Workshop 2 clean starter repo for GitLab import
└── reference-gitlab-ci/       # Workshop 2 golden reference (.gitlab-ci.yml + ci/ai_gate.py)
```

---

## 📖 Quick Links

* **Workshop 1 (SDD & EGM)**: [Attendee Guide](./guides/WORKSHOP_GUIDE.md) · [Speaker Guide](./guides/SPEAKER_GUIDE.md) · [Codelab Source](./codelab/codelab.md) · [Reference App](./reference-app/)
* **Workshop 2 (GitLab CI/CD & Antigravity SDK)**: [Attendee Guide](./guides/GITLAB_CI_WORKSHOP_GUIDE.md) · [Speaker Guide & GitLab Cheat Sheet](./guides/GITLAB_CI_SPEAKER_GUIDE.md) · [Codelab Source](./codelab/gitlab-ci.md) · [Starter Repo](./retropulse-starter/) · [Reference Pipeline](./reference-gitlab-ci/)
