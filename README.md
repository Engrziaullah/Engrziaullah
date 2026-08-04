<div align="center">

# Hi, I'm Zia Ullah 👋

### AI/ML Engineer · Generative AI & Agentic AI · Computer Vision · Software Engineering Student

I build practical AI systems — from multi-agent pipelines that turn raw conversation into structured clinical documentation, to computer-vision applications people can actually run and click through, not just notebooks. Currently completing a BS in Software Engineering at the **University of Malakand**, Pakistan, while specializing in **LLM-based agents, applied deep learning, and computer vision**.

<a href="mailto:ziaullahbj9@gmail.com"><img src="https://img.shields.io/badge/Email-ziaullahbj9%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>
<a href="https://www.linkedin.com/in/engr-ziaullah-innovation"><img src="https://img.shields.io/badge/LinkedIn-Zia%20Ullah-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="https://www.kaggle.com/ziaullah299"><img src="https://img.shields.io/badge/Kaggle-Profile-20BEFF?style=flat-square&logo=kaggle&logoColor=white" /></a>

<img src="https://komarev.com/ghpvc/?username=Engrziaullah&label=Profile%20Views&color=0e75b6&style=flat-square" />

</div>

<br>

## About Me

- 🎓 BS Software Engineering student, University of Malakand, Pakistan
- 🤖 Specializing in **Generative AI, Agentic AI (multi-agent pipelines with LangGraph), and applied Computer Vision**
- 🩺 Particular interest in **AI for clinical/healthcare workflows** — see the flagship project below
- 🛠️ Comfortable across the full ML lifecycle: data preprocessing → model development → deployable, real-world applications (Flask, Streamlit, Docker)
- 📐 Approach AI as an engineering discipline — reproducible pipelines and shippable systems over one-off notebooks

<br>

## Current Focus

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
<img src="https://skillicons.dev/icons?i=python,cpp,java,php,html,css,js&theme=dark" />
<br>
SQL

**AI / Machine Learning**
<br>
<img src="https://skillicons.dev/icons?i=pytorch,tensorflow,opencv,scikitlearn&theme=dark" />
<br>
Keras · Pandas · NumPy · model evaluation & optimization

**Generative AI / Agentic AI**
- Multi-agent orchestration with **LangGraph**
- LLM inference via **Groq** (Llama 3.x)
- Prompt engineering & structured/validated outputs
- Human-in-the-loop review design

**Computer Vision**
- OpenCV · MediaPipe
- CNN-based image classification (TensorFlow/Keras)

**Data Visualization**
- Matplotlib · Seaborn · Plotly

**Web & Deployment**
<br>
<img src="https://skillicons.dev/icons?i=flask,docker,postgresql,mysql,git,github,vscode&theme=dark" />
<br>
Streamlit · REST APIs

**Tools**
- Git & GitHub · Jupyter Notebook · VS Code · Docker

<br>

## Featured Projects

### 🚀 Auto-Form-Filling-Agent
**Multi-agent clinical documentation system** — the flagship project.

Doctors manually transcribing patient conversations into intake forms and prescriptions is slow and error-prone. This project automates that path end-to-end: a doctor-patient conversation is captured by microphone, transcribed **entirely offline**, and pushed through a **6-stage LangGraph agent pipeline** that extracts clinical entities, resolves references, normalizes terminology, builds a structured intake form, recommends diagnostic tests by urgency, and applies a human-in-the-loop confidence check — before rendering a formatted prescription image.

**Tech:** Python · Vosk (offline speech-to-text) · LangGraph · Groq (Llama 3.3 70B) · Pillow

**Highlights:**
- Six chained agents: entity extraction → coreference resolution → context normalization → form mapping/validation → AI-driven test ordering → human-in-the-loop review
- Auto-approves output once a completeness score crosses 60%, otherwise flags it for manual review
- Fully offline speech recognition — no cloud STT dependency for the audio pipeline

[View Repository →](https://github.com/Engrziaullah/Auto-Form-Filling-Agent/tree/master)
<sub>Note: the working code lives on the `master` branch of this repository.</sub>

---

### 🤸 Kinetra — Real-Time Human Pose Estimation
A Flask + MediaPipe web app that detects **33 body landmarks** across three real workflows: photo upload, background-threaded video processing with a live progress bar, and live webcam streaming — plus joint-angle calculation and CSV landmark export.

**Tech:** Python · Flask · MediaPipe · OpenCV · Docker · Gunicorn

**Highlights:**
- Three distinct inference modes (image / video / live) sharing one processing core, not three separate scripts
- Background-threaded video jobs with polling-based progress so the UI never blocks
- Documented system architecture (request flow + sequence diagrams) and a pinned dependency chain for reproducible builds

[View Repository →](https://github.com/Engrziaullah/pose-estimation)

<br>

<table>
<tr>
<td width="50%" valign="top">

**🏥 MediBot — AI Healthcare Assistant**
<br>
Domain-restricted medical Q&A chatbot with content guardrails that keep responses health-focused and filter out off-topic queries.
<br><br>
**Tech:** Python · Flask · JavaScript · LLM API
<br>
[View Repository →](https://github.com/Engrziaullah/AI-Powered-Healthcare-Assistant)

</td>
<td width="50%" valign="top">

**🐾 PetVision — Cat vs Dog Classifier**
<br>
CNN-based image classifier deployed as an interactive Streamlit dashboard with real-time confidence scores.
<br><br>
**Tech:** TensorFlow · Keras · Streamlit
<br>
[View Repository →](https://github.com/Engrziaullah/PetVision-AI-Cat-vs-Dog-Classifier-Streamlit-App-)

</td>
</tr>
<tr>
<td width="50%" valign="top">

**💬 Multi-Label Emotion Recognition from Text**
<br>
NLP pipeline classifying multi-label emotions (joy, sadness, anger, etc.) using SenticNet lexicon + TF-IDF features with BRkNN classifiers, negation handling, and 10-fold cross-validation.
<br><br>
**Tech:** Python · scikit-learn · NLP
<br>
[View Repository →](https://github.com/Engrziaullah/Multi-Label-Emotion-Recognition-from-Text)

</td>
<td width="50%" valign="top">

**📊 Customer Segmentation & Clustering**
<br>
Unsupervised segmentation on marketing campaign data using K-Means and Hierarchical clustering with PCA dimensionality reduction.
<br><br>
**Tech:** scikit-learn · PCA · Seaborn · Plotly
<br>
[View Repository →](https://github.com/Engrziaullah/customer-segmentation-clustering)

</td>
</tr>
</table>

<br>

## GitHub Activity

<div align="center">
<img src="https://streak-stats.demolab.com?user=Engrziaullah&theme=tokyonight&hide_border=true" />
</div>

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

## Connect With Me

<a href="mailto:ziaullahbj9@gmail.com"><img src="https://img.shields.io/badge/Email-ziaullahbj9%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white" /></a>
<a href="https://www.linkedin.com/in/engr-ziaullah-innovation"><img src="https://img.shields.io/badge/LinkedIn-Zia%20Ullah-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
<a href="https://www.kaggle.com/ziaullah299"><img src="https://img.shields.io/badge/Kaggle-Profile-20BEFF?style=flat-square&logo=kaggle&logoColor=white" /></a>
<a href="https://github.com/Engrziaullah"><img src="https://img.shields.io/badge/GitHub-Engrziaullah-181717?style=flat-square&logo=github&logoColor=white" /></a>

<br>

<div align="center">

> I build AI systems designed to run, not just demo.
> If you're a recruiter, researcher, or team working on applied AI — let's talk.

</div>
