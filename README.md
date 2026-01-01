# ppt-reviewer-agent 🤖

An **AI-powered PowerPoint analyzer** that reviews presentations and provides actionable suggestions on content, design, and engagement. Built with Python, FastAPI, and OpenAI API.

## Features

✨ **Core Features:**
- 📤 Upload & parse `.pptx` files (extract text, images, layout)
- 🧠 AI-powered content analysis (clarity, messaging, tone consistency)
- 🎨 Design review suggestions (text density, font consistency, color harmony)
- 📊 Engagement scoring (call-to-action clarity, visual hierarchy, story flow)
- 📋 Detailed reports (HTML, JSON, Markdown formats)
- ⚡ Fast processing with streaming support

## Tech Stack

**Backend:**
- Python 3.9+
- FastAPI (lightweight & fast API framework)
- python-pptx (PowerPoint parsing)
- OpenAI/Anthropic API (Claude/GPT models)
- Pydantic (data validation)

**Frontend:**
- HTML5 + Vanilla JavaScript (or React for advanced version)
- Tailwind CSS (styling)

**Deployment:**
- Docker (containerization)
- Vercel/Render (free hosting)

## Project Structure

```
ppt-reviewer-agent/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── ppt_parser.py           # Parse .pptx files
│   ├── ai_analyzer.py          # OpenAI/Claude integration
│   ├── report_generator.py     # Generate HTML/JSON reports
│   ├── requirements.txt        # Python dependencies
│   └── config.py               # Environment & API keys
├── frontend/
│   ├── index.html              # Upload form
│   ├── style.css               # Styling
│   ├── script.js               # API calls & UI logic
│   └── results.html            # Report display page
├── tests/
│   ├── test_parser.py
│   └── test_analyzer.py
├── docker-compose.yml          # Docker setup
├── .gitignore
├── README.md                   # This file
└── LICENSE
```

## MVP Features (v1.0)

✅ Upload .pptx file  
✅ Parse slides (extract text & metadata)  
✅ AI analysis (content quality scoring)  
✅ Generate HTML report with suggestions  
✅ Simple web UI with upload form  
✅ Deploy to Vercel/Render  

## Advanced Features (v2.0+)

📊 Visual design analysis (small fonts, crowded layouts)  
🎨 Color contrast checker  
📝 Presenter notes analysis  
🔄 Suggest slide restructuring  
💾 Save & compare presentations  
🔗 Jira/Slack integration  
📈 Batch processing  

## Installation

### Prerequisites
- Python 3.9 or higher
- pip or conda
- OpenAI API key (or Anthropic Claude key)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/viswakpullepu/ppt-reviewer-agent.git
cd ppt-reviewer-agent
```

2. **Set up backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. **Run the backend:**
```bash
uvicorn main:app --reload
# API will be available at http://localhost:8000
```

5. **Serve frontend:**
```bash
cd ../frontend
python -m http.server 3000  # or use `npx serve .`
# Frontend at http://localhost:3000
```

## Usage

### Web UI
1. Open `http://localhost:3000` in your browser
2. Click "Upload PowerPoint" and select a `.pptx` file
3. Wait for analysis to complete (typically 10-30 seconds)
4. Review the generated report with suggestions
5. Download report as HTML, JSON, or Markdown

### API Usage

```bash
# Upload and analyze presentation
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@presentation.pptx"

# Get analysis report
curl http://localhost:8000/api/report/{job_id}?format=json
```

## Example Output

**Report Sample:**
```json
{
  "overall_score": 78,
  "slides": [
    {
      "slide_number": 1,
      "content_score": 85,
      "design_score": 72,
      "engagement_score": 80,
      "suggestions": [
        "Title slide: Good clarity. Consider adding a subtle visual element.",
        "Too much text in subtitle (42 words). Condense to 2-3 key points."
      ]
    }
  ],
  "overall_suggestions": [
    "Use consistent font sizes across slides",
    "Add more visuals to break up text-heavy slides",
    "Improve color contrast on slide 5"
  ]
}
```

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
OPENAI_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_claude_api_key  # Optional
MAX_FILE_SIZE_MB=50
ALLOWED_FORMATS=pptx,ppt
LOG_LEVEL=INFO
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] Support for `.odp` (LibreOffice) and `.key` (Keynote) files
- [ ] Multi-language analysis support
- [ ] Export to PowerPoint with embedded suggestions
- [ ] Real-time collaboration features
- [ ] Browser extension for quick analysis
- [ ] Mobile app (iOS/Android)

## License

MIT License - see LICENSE file for details

## Author

**Viswak Pullepu**
- GitHub: [@viswakpullepu](https://github.com/viswakpullepu)
- LinkedIn: [viswakpullepu](https://linkedin.com/in/viswakpullepu)

## Support & Feedback

- 📮 Open an issue for bugs
- 💡 Suggest features in Discussions
- ⭐ Star this repo if you find it useful!

## Acknowledgments

- [python-pptx](https://python-pptx.readthedocs.io/) - PowerPoint parsing
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [OpenAI](https://openai.com/) & [Anthropic](https://www.anthropic.com/) - AI models
