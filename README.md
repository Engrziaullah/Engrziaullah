<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Engrziaullah/Engrziaullah/main/assets/dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Engrziaullah/Engrziaullah/main/assets/light.svg">
  <img alt="Zia Ullah — AI/ML Engineer, Generative AI & Agentic AI, Computer Vision" src="https://raw.githubusercontent.com/Engrziaullah/Engrziaullah/main/assets/light.svg" width="100%">
</picture>

<br><br>

I build practical AI systems — multi-agent pipelines that turn raw conversation into structured clinical documentation, and computer-vision applications people can actually run, not just notebooks. Final-year Software Engineering student at the **University of Malakand**, Pakistan, specializing in **agentic AI, applied deep learning, and computer vision**.

<br>

<a href="mailto:ziaullahbj9@gmail.com"><img src="https://img.shields.io/badge/Email-ziaullahbj9%40gmail.com-6366F1?style=for-the-badge&labelColor=0B0F19&logo=gmail&logoColor=white" /></a>
<a href="https://www.linkedin.com/in/engr-ziaullah-innovation"><img src="https://img.shields.io/badge/LinkedIn-Zia%20Ullah-6366F1?style=for-the-badge&labelColor=0B0F19&logo=linkedin&logoColor=white" /></a>
<a href="https://www.kaggle.com/ziaullah299"><img src="https://img.shields.io/badge/Kaggle-ziaullah299-6366F1?style=for-the-badge&labelColor=0B0F19&logo=kaggle&logoColor=white" /></a>
<a href="https://github.com/Engrziaullah"><img src="https://img.shields.io/badge/GitHub-Engrziaullah-6366F1?style=for-the-badge&labelColor=0B0F19&logo=github&logoColor=white" /></a>

</div>

<br>

## About Me

- 🎓 Final-year BS Software Engineering student, University of Malakand, Pakistan
- 🤖 Specializing in **Generative AI, Agentic AI** (multi-agent pipelines with LangGraph), and applied **Computer Vision**
- 🩺 Particular interest in **AI for clinical/healthcare workflows** — see the flagship project below
- 🛠️ Comfortable across the full ML lifecycle: data preprocessing → model development → deployable, real-world applications (Flask, Streamlit, Docker)
- 📐 Treat AI as an engineering discipline — reproducible pipelines and shippable systems over one-off notebooks

<br>

## Currently Focused On

- 🤖 **Machine Learning & Deep Learning** — CNNs, transfer learning, model evaluation
- 🧠 **Generative AI & LLM Applications** — Groq-hosted LLMs, structured outputs
- 🔗 **Agentic AI & Multi-Agent Workflows** — LangGraph pipelines, human-in-the-loop review
- 👁️ **Computer Vision** — MediaPipe, OpenCV, real-time inference
- 📚 **NLP & Applied Text Classification** — feature engineering, multi-label models
- 🌐 **Deployable AI Applications** — Flask / Streamlit / Docker

<br>

## Tech Stack

**Languages**
<br>
<img src="https://skillicons.dev/icons?i=python,cpp,java,php,html,css,js&theme=dark" /><br>
SQL

**AI / ML**
<br>
<img src="https://skillicons.dev/icons?i=pytorch,tensorflow,opencv,scikitlearn&theme=dark" /><br>
Keras · Pandas · NumPy · model evaluation & optimization

**GenAI & Agentic**
- Multi-agent orchestration with **LangGraph**
- LLM inference via **Groq** (Llama 3.x)
- Prompt engineering & structured/validated outputs
- Human-in-the-loop review design

**Computer Vision**
- OpenCV · MediaPipe
- CNN-based image classification (TensorFlow/Keras)

**Data Viz**
- Matplotlib · Seaborn · Plotly

**Deployment**
<br>
<img src="https://skillicons.dev/icons?i=flask,docker,postgresql,mysql,git,github,vscode&theme=dark" /><br>
Streamlit · REST APIs

**Tools**
- Git & GitHub · Jupyter Notebook · VS Code · Docker

<br>

## Featured Projects

### 🚀 Auto-Form-Filling-Agent
**Multi-agent clinical documentation system** — the flagship project.

Doctors manually transcribing patient conversations into intake forms and prescriptions is slow and error-prone. This automates that path end-to-end: a doctor-patient conversation is captured by microphone, transcribed **entirely offline**, and pushed through a **6-stage LangGraph agent pipeline** that extracts clinical entities, resolves references, normalizes terminology, builds a structured intake form, recommends diagnostic tests by urgency, and applies a human-in-the-loop confidence check — before rendering a formatted prescription image.

`Python` `Vosk (offline STT)` `LangGraph` `Groq · Llama 3.3 70B` `Pillow`

- Six chained agents: entity extraction → coreference resolution → context normalization → form mapping/validation → AI-driven test ordering → human-in-the-loop review
- Auto-approves output once a completeness score crosses 60%, otherwise flags it for manual review
- Fully offline speech recognition — no cloud STT dependency for the audio pipeline

[View Repository →](https://github.com/Engrziaullah/Auto-Form-Filling-Agent/tree/master)
<sub>Working code lives on the `master` branch of this repository.</sub>

---

### 🤸 Kinetra — Real-Time Human Pose Estimation
A Flask + MediaPipe web app that detects **33 body landmarks** across three real workflows: photo upload, background-threaded video processing with a live progress bar, and live webcam streaming — plus joint-angle calculation and CSV landmark export.

`Python` `Flask` `MediaPipe` `OpenCV` `Docker` `Gunicorn`

- Three distinct inference modes (image / video / live) sharing one processing core, not three separate scripts
- Background-threaded video jobs with polling-based progress so the UI never blocks
- Documented system architecture (request flow + sequence diagrams) and a pinned dependency chain for reproducible builds

[View Repository →](https://github.com/Engrziaullah/pose-estimation)

<br>

<table>
<tr>
<td width="50%" valign="top">

**🏥 MediBot — AI Healthcare Assistant**

Domain-restricted medical Q&A chatbot with content guardrails that keep responses health-focused and filter out off-topic queries.

`Python` `Flask` `JavaScript` `LLM API`

[View Repository →](https://github.com/Engrziaullah/AI-Powered-Healthcare-Assistant)

</td>
<td width="50%" valign="top">

**🐾 PetVision — Cat vs Dog Classifier**

CNN-based image classifier deployed as an interactive Streamlit dashboard with real-time confidence scores.

`TensorFlow` `Keras` `Streamlit`

[View Repository →](https://github.com/Engrziaullah/PetVision-AI-Cat-vs-Dog-Classifier-Streamlit-App-)

</td>
</tr>
<tr>
<td width="50%" valign="top">

**💬 Multi-Label Emotion Recognition from Text**

NLP pipeline classifying multi-label emotions (joy, sadness, anger, etc.) using SenticNet lexicon + TF-IDF features with BRkNN classifiers, negation handling, and 10-fold cross-validation.

`Python` `scikit-learn` `NLP`

[View Repository →](https://github.com/Engrziaullah/Multi-Label-Emotion-Recognition-from-Text)

</td>
<td width="50%" valign="top">

**📊 Customer Segmentation & Clustering**

Unsupervised segmentation on marketing campaign data using K-Means and Hierarchical clustering with PCA dimensionality reduction.

`scikit-learn` `PCA` `Seaborn` `Plotly`

[View Repository →](https://github.com/Engrziaullah/customer-segmentation-clustering)

</td>
</tr>
</table>

<br>

## GitHub Stats

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=Engrziaullah&hide_border=true&background=0B0F19&stroke=818CF8&ring=818CF8&fire=818CF8&currStreakLabel=818CF8&sideLabels=94A3B8&currStreakNum=F8FAFC&sideNums=F8FAFC&dates=64748B&titleColor=818CF8">
  <source media="(prefers-color-scheme: light)" srcset="https://streak-stats.demolab.com/?user=Engrziaullah&hide_border=true&background=FFFFFF&stroke=4F46E5&ring=4F46E5&fire=4F46E5&currStreakLabel=4F46E5&sideLabels=475569&currStreakNum=0F172A&sideNums=0F172A&dates=64748B&titleColor=4F46E5">
  <img alt="GitHub streak stats" src="https://streak-stats.demolab.com/?user=Engrziaullah&hide_border=true&background=FFFFFF&stroke=4F46E5&ring=4F46E5&fire=4F46E5&currStreakLabel=4F46E5&sideLabels=475569&currStreakNum=0F172A&sideNums=0F172A&dates=64748B&titleColor=4F46E5">
</picture>

<!--
  ACTION REQUIRED to enable the Stats + Top Languages cards below:
  The shared public github-readme-stats.vercel.app instance is currently down
  (503 DEPLOYMENT_PAUSED as of this writing), so it's intentionally left
  disabled rather than shipping broken images.

  To enable it on your own reliable, self-owned instance (~2 minutes):
    1. Fork https://github.com/anuraghazra/github-readme-stats
    2. Go to https://vercel.com -> Add New... -> Project -> import your fork
    3. Deploy with default settings (no config needed)
    4. Vercel gives you a URL like: github-readme-stats-xxxx.vercel.app
    5. Replace YOUR-STATS-HOST below with that domain, then remove the
       HTML comment markers that wrap this block so it renders.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://YOUR-STATS-HOST.vercel.app/api?username=Engrziaullah&show_icons=true&hide_rank=true&hide_border=true&title_color=818CF8&icon_color=818CF8&text_color=94A3B8&bg_color=0B0F19">
  <source media="(prefers-color-scheme: light)" srcset="https://YOUR-STATS-HOST.vercel.app/api?username=Engrziaullah&show_icons=true&hide_rank=true&hide_border=true&title_color=4F46E5&icon_color=4F46E5&text_color=475569&bg_color=FFFFFF">
  <img alt="GitHub stats" width="49%" src="https://YOUR-STATS-HOST.vercel.app/api?username=Engrziaullah&show_icons=true&hide_rank=true&hide_border=true&title_color=4F46E5&icon_color=4F46E5&text_color=475569&bg_color=FFFFFF">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://YOUR-STATS-HOST.vercel.app/api/top-langs/?username=Engrziaullah&layout=compact&hide_border=true&title_color=818CF8&text_color=94A3B8&bg_color=0B0F19">
  <source media="(prefers-color-scheme: light)" srcset="https://YOUR-STATS-HOST.vercel.app/api/top-langs/?username=Engrziaullah&layout=compact&hide_border=true&title_color=4F46E5&text_color=475569&bg_color=FFFFFF">
  <img alt="Top languages" width="49%" src="https://YOUR-STATS-HOST.vercel.app/api/top-langs/?username=Engrziaullah&layout=compact&hide_border=true&title_color=4F46E5&text_color=475569&bg_color=FFFFFF">
</picture>
-->

</div>

<br>

## Live Projects

<div align="center">
<img width="100%" src="https://raw.githubusercontent.com/Engrziaullah/Engrziaullah/projects/projects.svg" alt="Live project stats" />
</div>

<sub>Generated every 6 hours by <a href="./.github/workflows/projects.yml">a scheduled GitHub Action</a> — pulls live stars/languages for the repos in <a href="./projects.json">projects.json</a>.</sub>

<br>

## Contribution Snake

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Engrziaullah/Engrziaullah/output/snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Engrziaullah/Engrziaullah/output/snake-light.svg">
  <img alt="Contribution snake animation" src="https://raw.githubusercontent.com/Engrziaullah/Engrziaullah/output/snake-light.svg" width="100%">
</picture>
</div>

<sub>Generated daily by <a href="./.github/workflows/snake.yml">a scheduled GitHub Action</a> — renders on first successful run of that workflow.</sub>

<br>

## Research & Learning Interests

- Agentic AI system design & multi-agent orchestration
- Retrieval-Augmented Generation (RAG)
- Applied computer vision for real-time interaction (pose/motion analysis)
- Healthcare-focused AI tooling
- NLP for structured information extraction

<br>

## Leadership & Community

**President — IEEE Student Branch, University of Malakand**
<br>
Leading technical activities and student engagement for the branch's IEEE chapter.

<br>

<div align="center">

---

<a href="mailto:ziaullahbj9@gmail.com"><img src="https://img.shields.io/badge/Email-ziaullahbj9%40gmail.com-6366F1?style=for-the-badge&labelColor=0B0F19&logo=gmail&logoColor=white" /></a>
<a href="https://www.linkedin.com/in/engr-ziaullah-innovation"><img src="https://img.shields.io/badge/LinkedIn-Zia%20Ullah-6366F1?style=for-the-badge&labelColor=0B0F19&logo=linkedin&logoColor=white" /></a>
<a href="https://www.kaggle.com/ziaullah299"><img src="https://img.shields.io/badge/Kaggle-ziaullah299-6366F1?style=for-the-badge&labelColor=0B0F19&logo=kaggle&logoColor=white" /></a>
<a href="https://github.com/Engrziaullah"><img src="https://img.shields.io/badge/GitHub-Engrziaullah-6366F1?style=for-the-badge&labelColor=0B0F19&logo=github&logoColor=white" /></a>

<br><br>

<img src="https://komarev.com/ghpvc/?username=Engrziaullah&label=Profile%20Views&color=6366F1&style=flat-square" />

<br><br>

> I build AI systems designed to run, not just demo.
> If you're a recruiter, researcher, or team working on applied AI — let's talk.

</div>
