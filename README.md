# 🚀 KnowledgeOS

KnowledgeOS is an AI-powered knowledge management platform that enables users to organize, search, and retrieve information efficiently through a modern web interface.

## ✨ Features

- 📚 Create and manage knowledge collections
- 🔍 AI-powered semantic search
- 💬 Chat with your knowledge base
- 📄 Document upload and management
- 🔐 Secure user authentication
- ⚡ Fast and responsive UI
- 📱 Modern dashboard interface

---

## 🛠 Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- FastAPI
- Python
- PostgreSQL
- SQLAlchemy

### AI
- OpenAI API (or compatible LLM)
- Vector Search
- Embeddings

---

## 📂 Project Structure

```text
knowledgeos/
│
├── backend/
│   ├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── requirements.txt
│   └── server.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Harish-antony/knowledgeos.git

cd knowledgeos
```

---

### 2. Backend Setup

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

python server.py
```

---

### 3. Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## 🔑 Environment Variables

Create a `.env` file inside the backend folder.

Example:

```env
OPENAI_API_KEY=your_api_key

DATABASE_URL=your_database_url

SECRET_KEY=your_secret_key
```

---

## 🚀 Running the Application

Backend

```bash
python server.py
```

Frontend

```bash
npm run dev
```

Open:

```
http://localhost:5173
```

---

## 📌 Future Improvements

- Multi-user workspaces
- Role-based access control
- OCR document ingestion
- Voice interaction
- AI-generated summaries
- Export knowledge as PDF
- Mobile support

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Harish Antony**

GitHub: https://github.com/Harish-antony
