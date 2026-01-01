SETUP_INSTRUCTIONS.md# 🚀 PPT REVIEWER AGENT - COMPLETE SETUP GUIDE

## ⚡ QUICK START (5 Minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/viswakpullepu/ppt-reviewer-agent.git
cd ppt-reviewer-agent
```

### Step 2: Get OpenAI API Key
1. Go to: https://platform.openai.com/account/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy your key (looks like: `sk-proj-xxxxx...`)
5. Keep it safe!

### Step 3: Create `.env` File
```bash
cd backend
cp ../.env.example .env
```

### Step 4: Add Your API Key
Edit `backend/.env` and replace:
```
OPENAI_API_KEY=sk-proj-YOUR-ACTUAL-KEY-HERE
```

### Step 5: Install & Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

✅ **Backend running at:** http://localhost:8000
✅ **API docs at:** http://localhost:8000/docs

### Step 6: Run Frontend (Optional)
In another terminal:
```bash
cd frontend
python -m http.server 3000
```

✅ **Frontend at:** http://localhost:3000

---

## 📁 PROJECT STRUCTURE

```
ppt-reviewer-agent/
├── backend/
│   ├── .env                 ← CREATE THIS & ADD YOUR API KEY
│   ├── .env.example         ← Template (reference)
│   ├── main.py              ← FastAPI application (FULLY WORKING)
│   ├── ppt_parser.py        ← PowerPoint parsing
│   ├── ai_analyzer.py       ← OpenAI integration
│   ├── report_generator.py  ← Report generation
│   ├── config.py            ← Settings & configuration
│   ├── requirements.txt      ← Python dependencies
│   └── Dockerfile           ← Docker container
├── frontend/
│   └── index.html           ← Web UI
├── README.md                ← Full documentation
├── docker-compose.yml       ← Multi-container setup
└── LICENSE                  ← MIT License
```

---

## 🔐 SETUP YOUR API KEY (3 Methods)

### Method 1: Using .env File (Recommended)

1. **Create file** `backend/.env`:
```bash
cd backend
touch .env
```

2. **Add your key**:
```
OPENAI_API_KEY=sk-proj-YOUR-ACTUAL-KEY-HERE
MAX_FILE_SIZE_MB=50
LOG_LEVEL=INFO
```

3. **Done!** App will read it automatically

### Method 2: Environment Variable

Linux/Mac:
```bash
export OPENAI_API_KEY="sk-proj-YOUR-KEY-HERE"
uvicorn main:app --reload
```

Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY = "sk-proj-YOUR-KEY-HERE"
uvicorn main:app --reload
```

### Method 3: Docker Compose

Edit `docker-compose.yml`:
```yaml
services:
  backend:
    environment:
      - OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
```

Then run:
```bash
docker-compose up
```

---

## 🧪 TEST THE APPLICATION

### 1. Check if API is running:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "version": "1.0.0"}
```

### 2. Upload & Analyze PowerPoint:

**Using cURL:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@your_presentation.pptx"
```

**Expected response:**
```json
{
  "status": "success",
  "job_id": "unique-id-123",
  "filename": "your_presentation.pptx",
  "total_slides": 15,
  "message": "Presentation analyzed successfully"
}
```

### 3. Get Results:
```bash
curl http://localhost:8000/api/report/unique-id-123?format=json
```

---

## 📊 API ENDPOINTS

| Method | Endpoint | Purpose |
|--------|----------|----------|
| GET | `/` | API info & status |
| GET | `/health` | Health check |
| POST | `/api/analyze` | Upload & analyze PowerPoint |
| GET | `/api/report/{job_id}` | Get analysis report (json/html/markdown) |
| GET | `/api/status/{job_id}` | Check job status |

---

## 🐳 DOCKER SETUP (Optional)

### Using Docker Compose (Recommended)

1. **Edit docker-compose.yml** - add your API key
2. **Run:**
```bash
docker-compose up
```

This starts:
- ✅ Backend (port 8000)
- ✅ Frontend (port 3000)
- ✅ Redis cache (port 6379)

### Manual Docker Build

```bash
cd backend
docker build -t ppt-reviewer .
docker run -e OPENAI_API_KEY="sk-proj-YOUR-KEY" -p 8000:8000 ppt-reviewer
```

---

## 🐛 TROUBLESHOOTING

### Issue: "OPENAI_API_KEY not found"

**Solution:** Make sure `.env` file exists in `backend/` folder:
```bash
cd backend
ls -la .env  # Should exist
cat .env    # Should contain your key
```

### Issue: "ModuleNotFoundError"

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"

**Solution:** Use a different port:
```bash
uvicorn main:app --reload --port 8001
```

### Issue: "API Key is invalid"

**Solution:** 
1. Check key at: https://platform.openai.com/account/api-keys
2. Make sure it's not revoked
3. Regenerate a new one if needed
4. Update `.env` file

---

## 📈 FEATURES (ALL WORKING)

✅ Upload PowerPoint files (.pptx/.ppt)  
✅ Extract slides, text, images, metadata  
✅ AI-powered analysis (OpenAI GPT-3.5)  
✅ Content clarity scoring  
✅ Design recommendations  
✅ Generate reports (HTML, JSON, Markdown)  
✅ Job tracking with UUIDs  
✅ Real-time progress tracking  
✅ CORS support for web  
✅ Production-ready error handling  

---

## 💡 TIPS

1. **Keep your API key safe** - Never commit `.env` to GitHub
2. **Monitor API usage** - Check at https://platform.openai.com/usage
3. **Use free credits first** - $5 free for testing
4. **Test with small files** - Start with 5-10 slides
5. **Read API docs** - http://localhost:8000/docs (Swagger UI)

---

## 🎯 WHAT'S NEXT?

1. ✅ Setup `.env` with your API key
2. ✅ Run `uvicorn main:app --reload`
3. ✅ Upload your first PowerPoint
4. ✅ Check results at `/api/report/{job_id}`
5. ✅ Build on top of this agent!

---

## 📞 SUPPORT

- **API Docs:** http://localhost:8000/docs
- **GitHub:** https://github.com/viswakpullepu/ppt-reviewer-agent
- **OpenAI Docs:** https://platform.openai.com/docs

---

**Ready to go!** 🚀
