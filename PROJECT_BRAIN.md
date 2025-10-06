# 🧠 PROJECT BRAIN - NFL Social Content Generator

**Central Intelligence Hub | Living Documentation | Development Log**

---

## 📋 TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Current Status](#current-status)
3. [Architecture](#architecture)
4. [Development Phases](#development-phases)
5. [Change Log](#change-log)
6. [Technical Notes](#technical-notes)
7. [Deployment Info](#deployment-info)
8. [Future Roadmap](#future-roadmap)
9. [Known Issues](#known-issues)
10. [Quick Reference](#quick-reference)

---

## 🎯 PROJECT OVERVIEW

### What This Is
An automated social media content generator that transforms NFL futures odds movement data into engaging, ready-to-post tweet drafts for the Novig sports betting platform.

### The Problem We're Solving
- **Manual Process**: Creating social content from odds data is time-consuming
- **Consistency**: Need uniform quality and format across all posts
- **Timeliness**: Markets move fast, content needs to be generated quickly
- **Context**: Raw odds changes need NFL context to be compelling

### The Solution
A web-based tool that:
1. Ingests CSV data of NFL futures odds (week-over-week)
2. Identifies the biggest movers (configurable threshold)
3. Generates multiple tweet variations with proper context
4. Provides copy-paste ready content with character counts

### Success Metrics
- **Speed**: Generate 10+ tweet drafts in under 30 seconds
- **Quality**: 80%+ of tweets usable with minimal editing
- **Accuracy**: 100% data accuracy from CSV to output
- **Flexibility**: Support all major NFL futures markets

---

## 🚦 CURRENT STATUS

**Phase**: 1 - MVP (Completed)
**Version**: 1.0.0
**Deployment**: Web-hosted (Vercel)
**Last Updated**: 2025-01-XX

### ✅ What's Working
- CSV upload and validation
- Movement analysis with configurable thresholds
- Template-based tweet generation (3 variations per mover)
- Web interface with 4-step workflow
- JSON export functionality
- Character count validation
- Copy-to-clipboard feature

### 🚧 In Progress
- Web hosting setup (GitHub + Vercel)
- Production environment configuration
- Continuous deployment pipeline

### ⏳ Not Yet Implemented
- Automated NFL data fetching (Phase 2)
- AI-powered tweet variations (Phase 3)
- Image generation (Phase 4)
- Direct Twitter posting (Phase 4)

---

## 🏗️ ARCHITECTURE

### Tech Stack
```
Frontend: HTML5, CSS3, Vanilla JavaScript
Backend: Python 3.8+, Flask 3.0.0
Data Processing: Pandas 2.1.4
Deployment: Vercel (serverless)
Version Control: Git + GitHub
```

### File Structure
```
nfl-social-generator/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── vercel.json              # Vercel deployment config
├── requirements.txt          # Python dependencies
│
├── modules/                  # Core business logic
│   ├── csv_processor.py     # CSV import & validation
│   ├── movers_analyzer.py   # Movement analysis
│   ├── tweet_generator.py   # Tweet generation engine
│   └── templates.py         # Market-specific templates
│
├── templates/               # Flask HTML templates
│   └── index.html          # Main UI
│
├── static/                  # Static assets
│   ├── style.css           # UI styles
│   └── script.js           # Frontend logic
│
├── data/                    # Data storage
│   ├── sample_odds.csv     # Example data
│   ├── uploads/            # User uploaded CSVs
│   └── exports/            # Generated tweet exports
│
└── PROJECT_BRAIN.md        # This file
```

### Data Flow
```
1. USER UPLOADS CSV
   ↓
2. CSVProcessor validates & cleans data
   ↓
3. MoversAnalyzer identifies top movers
   ↓
4. TweetGenerator creates drafts using templates
   ↓
5. USER copies tweets or exports JSON
```

### Key Components

#### 1. CSV Processor (`modules/csv_processor.py`)
- **Purpose**: Import and validate odds data
- **Validates**: Column structure, data types, required fields
- **Cleans**: Strips whitespace, handles missing values, formats numbers
- **Returns**: Pandas DataFrame

#### 2. Movers Analyzer (`modules/movers_analyzer.py`)
- **Purpose**: Identify significant odds movements
- **Filters**: By configurable threshold (default 2%)
- **Sorts**: By absolute percentage change
- **Classifies**: Direction (up/down), magnitude (massive/significant/notable/moderate)
- **Returns**: Ranked DataFrame of movers

#### 3. Tweet Templates (`modules/templates.py`)
- **Purpose**: Store market-specific tweet formats
- **Markets Supported**:
  - Playoffs
  - MVP
  - Championships (Super Bowl, Conference)
  - Generic fallback
- **Variations**: 3 per market (Bold, Clean, Analytical)
- **Placeholders**: {team}, {odds}, {change}, {context}, {emoji}

#### 4. Tweet Generator (`modules/tweet_generator.py`)
- **Purpose**: Fill templates with mover data
- **Features**:
  - Character counting
  - Emoji toggling
  - Placeholder context (Phase 1)
  - Batch processing
- **Returns**: JSON with tweet variations + metadata

---

## 📊 DEVELOPMENT PHASES

### ✅ Phase 1: MVP (COMPLETED)
**Goal**: Core functionality with manual context

**Deliverables**:
- [x] CSV import & validation
- [x] Movement analysis
- [x] Template-based tweet generation
- [x] Web interface
- [x] Export to JSON
- [x] Sample data

**Timeline**: Initial build - January 2025

---

### 🔄 Phase 2: NFL Data Integration (PLANNED)
**Goal**: Automated context generation

**Planned Features**:
- [ ] Connect to SDQL or NFL API
- [ ] Auto-fetch recent game results
- [ ] Pull current standings
- [ ] Retrieve injury reports
- [ ] Generate contextual analysis
- [ ] Match market type to relevant stats

**Technical Decisions Needed**:
- Which NFL data source? (SDQL vs ESPN API vs API-Football)
- How to handle API rate limits?
- Caching strategy for frequently accessed data?

**Estimated Timeline**: 2-3 weeks after Phase 1 launch

---

### 🎨 Phase 3: Polish & Enhancement (PLANNED)
**Goal**: Better UX and content quality

**Planned Features**:
- [ ] OpenAI integration for creative variations
- [ ] Twitter preview styling
- [ ] Inline tweet editing
- [ ] User accounts & saved preferences
- [ ] Historical tweet performance tracking
- [ ] A/B testing framework

**Estimated Timeline**: 4-6 weeks after Phase 2

---

### 🚀 Phase 4: Advanced Features (FUTURE)
**Goal**: Full automation

**Ideas**:
- [ ] Image generation with odds charts
- [ ] Direct Twitter posting (OAuth)
- [ ] Scheduled posting queue
- [ ] Multi-platform support (Instagram, Facebook)
- [ ] Analytics dashboard

**Estimated Timeline**: TBD

---

## 📝 CHANGE LOG

### Version 1.0.0 - January 2025
**Initial Release - Phase 1 MVP**

#### Added
- CSV processor with validation
- Movers analyzer with configurable thresholds
- Template system for 4 market types
- Tweet generator with 3 variations per mover
- Flask web application
- Responsive UI with 4-step workflow
- JSON export functionality
- Sample data (20 entries covering major markets)
- Complete documentation (README.md)

#### Technical Details
- Built on Flask 3.0.0
- Uses Pandas 2.1.4 for data processing
- Vanilla JavaScript frontend (no frameworks)
- Character count validation (280 limit)
- Copy-to-clipboard integration

#### Files Created
```
14 total files:
- 4 Python modules (csv_processor, movers_analyzer, tweet_generator, templates)
- 1 Flask app (app.py)
- 1 config file (config.py)
- 1 HTML template (index.html)
- 2 static files (style.css, script.js)
- 1 sample CSV (sample_odds.csv)
- 1 requirements file
- 3 documentation files (README.md, PROJECT_BRAIN.md, .gitignore)
```

---

### Version 1.1.0 - January 2025 (In Progress)
**Web Hosting & Deployment**

#### Added
- Vercel deployment configuration (vercel.json)
- Production-ready Flask settings
- Gunicorn WSGI server
- GitHub repository integration
- .gitignore for Python/Flask
- Environment variable support (.env)
- Deployment documentation

#### Changed
- Updated requirements.txt for production
- Modified config.py for environment-based settings
- Added .gitkeep files for empty directories

#### Deployment Stack
- GitHub for version control
- Vercel for serverless hosting
- Automatic deployments on push to main

---

## 🔧 TECHNICAL NOTES

### CSV Data Format Requirements

**Required Columns**:
```
market              - String (e.g., "To Make The Playoffs")
team_player         - String (e.g., "Detroit Lions")
last_week_pct       - Float (e.g., 75.00)
this_week_pct       - Float (e.g., 81.13)
change_pct          - Float (e.g., 6.13)
last_week_american  - Int (e.g., -300)
this_week_american  - Int (e.g., -430)
```

**Data Validation Rules**:
1. All columns must be present
2. Percentage values must be numeric (0-100)
3. American odds can be positive or negative integers
4. Team/player names must be non-empty strings
5. Market names should match template categories for best results

**Common Issues**:
- Missing + sign on positive odds → Processor auto-handles
- Extra whitespace in team names → Auto-trimmed
- Inconsistent market naming → Falls back to generic template

---

### Template System Design

**Philosophy**: Market-specific templates with contextual awareness

**Template Variables**:
```python
{team}           # Team name
{player}         # Player name (for MVP markets)
{team_player}    # Generic team or player
{market}         # Market type
{last_odds}      # Previous American odds (formatted)
{this_odds}      # Current American odds (formatted)
{change}         # Percentage change
{context}        # NFL context (placeholder in Phase 1)
{emoji}          # Primary emoji
{emoji2}         # Secondary emoji
{team_emoji}     # Team-specific emoji (currently 🏈)
```

**Template Matching Logic**:
```
IF "playoff" in market_name → Use PLAYOFFS_TEMPLATES
ELIF "mvp" in market_name → Use MVP_TEMPLATES
ELIF "super bowl" OR "conference" in market_name → Use CHAMPIONSHIP_TEMPLATES
ELSE → Use GENERIC_TEMPLATES
```

**Character Count Strategy**:
- Target: 240-280 characters (leaves room for links/hashtags)
- All templates validated against 280 limit
- Over-limit tweets flagged but still shown (user can edit)

---

### State Management

**Current Approach**: In-memory global dictionary
```python
current_data = {
    'df': None,          # Pandas DataFrame
    'movers': None,      # Filtered DataFrame
    'results': None,     # Generated tweets
    'filename': None     # Source CSV name
}
```

**Limitations**:
- Not persistent (resets on server restart)
- Not multi-user (shared state)
- Not scalable

**Phase 2 Improvement Plan**:
- Use Flask sessions for user-specific data
- Redis for caching
- PostgreSQL for persistent storage

---

### Configuration System

**Current**: Single config.py file

**Settings Categories**:
1. **Analysis**: MOVEMENT_THRESHOLD, TOP_N_MOVERS
2. **Generation**: TWEET_VARIATIONS, INCLUDE_EMOJIS, CHARACTER_LIMIT
3. **Upload**: UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
4. **Flask**: DEBUG, SECRET_KEY, HOST, PORT

**Environment Variables** (Phase 2):
```
FLASK_ENV=production
SECRET_KEY=xxx
DATABASE_URL=xxx
REDIS_URL=xxx
NFL_API_KEY=xxx
```

---

## 🌐 DEPLOYMENT INFO

### Hosting Platform: Vercel

**Why Vercel?**
- Free tier for hobby projects
- Automatic HTTPS
- Global CDN
- Serverless Python support
- GitHub integration (auto-deploy on push)
- Easy environment variable management

**Deployment Process**:
1. Push code to GitHub
2. Import repository in Vercel
3. Vercel auto-detects Python + vercel.json
4. Automatic build & deploy
5. Live URL provided

**Configuration**:
- Build Command: `pip install -r requirements.txt`
- Output Directory: (not needed for Flask)
- Install Command: (handled automatically)

---

### GitHub Repository

**Repository Name**: `nfl-social-generator`
**Branch Strategy**:
- `main` → Production (auto-deploys to Vercel)
- `dev` → Development (for testing)
- Feature branches → Merge to dev → Merge to main

**Commit Message Convention**:
```
<type>: <description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance
```

---

### Environment Variables

**Production Settings** (Vercel):
```
FLASK_ENV=production
SECRET_KEY=<random-string>
DEBUG=False
```

**Local Development** (.env):
```
FLASK_ENV=development
SECRET_KEY=dev-secret-key
DEBUG=True
HOST=0.0.0.0
PORT=5000
```

---

### Monitoring & Logs

**Vercel Logs**: Access via Vercel dashboard
- Function execution logs
- Error tracking
- Performance metrics

**Application Logs**:
- Not yet implemented
- Phase 3: Add logging module
- Track: Uploads, generations, errors

---

## 🗺️ FUTURE ROADMAP

### Short-Term (Next 1-3 Months)

**Priority 1: NFL Data Integration**
- Research best API (SDQL vs alternatives)
- Implement data fetcher module
- Build context generator
- Test with real-time data

**Priority 2: User Experience**
- Add inline editing for tweets
- Improve error messages
- Add loading states
- Mobile responsiveness improvements

**Priority 3: Analytics**
- Track which tweets get used
- A/B test template variations
- User feedback collection

---

### Mid-Term (3-6 Months)

**AI Integration**
- OpenAI GPT-4 for creative variations
- Fine-tune on past successful tweets
- Sentiment analysis
- Tone adjustment controls

**Image Generation**
- Odds movement charts
- Team logos
- Branded templates
- Auto-sizing for Twitter

**Performance**
- Database integration
- Caching layer
- Batch processing improvements
- API rate limiting

---

### Long-Term (6-12 Months)

**Multi-Platform Support**
- Instagram captions
- Facebook posts
- LinkedIn content
- TikTok scripts

**Automation**
- Scheduled tweet posting
- Auto-detect odds changes
- Direct Twitter integration
- Content calendar

**Enterprise Features**
- User accounts
- Team collaboration
- Approval workflows
- Brand guidelines enforcement
- ROI tracking

---

## ⚠️ KNOWN ISSUES

### Phase 1 Issues

**Issue #1: Placeholder Context**
- **Status**: By Design (Phase 1)
- **Description**: Tweet context is generic placeholders, not real NFL data
- **Impact**: Tweets require manual editing to add actual game results/stats
- **Fix**: Phase 2 - NFL data integration

**Issue #2: Character Limit Overruns**
- **Status**: Minor
- **Description**: Some template variations exceed 280 characters
- **Workaround**: App flags over-limit tweets; user can edit before posting
- **Fix**: Refine templates in Phase 3

**Issue #3: No Multi-User Support**
- **Status**: Known Limitation
- **Description**: State is shared globally, not user-specific
- **Impact**: Concurrent users will overwrite each other's data
- **Fix**: Phase 2 - Implement sessions

**Issue #4: File Upload Size**
- **Status**: Working as Designed
- **Description**: 10MB limit may be too small for very large datasets
- **Workaround**: Split large CSVs
- **Fix**: Increase limit if needed (low priority)

---

### Vercel-Specific Considerations

**Issue #5: Serverless Cold Starts**
- **Status**: Expected Behavior
- **Description**: First request after inactivity may be slow (2-3 seconds)
- **Impact**: Minor UX delay
- **Mitigation**: Consider Vercel Pro for always-on instances

**Issue #6: Temporary File Storage**
- **Status**: Under Review
- **Description**: Uploaded files stored in /tmp, cleared on function restart
- **Impact**: Exports not persistent
- **Fix**: Phase 2 - Use cloud storage (S3/GCS)

---

## 📚 QUICK REFERENCE

### Common Commands

**Start Local Development**:
```bash
cd nfl-social-generator
python app.py
# Open http://localhost:5000
```

**Install Dependencies**:
```bash
pip install -r requirements.txt
```

**Deploy to Vercel**:
```bash
# First time: Install Vercel CLI
npm i -g vercel

# Deploy
cd nfl-social-generator
vercel
```

**Git Workflow**:
```bash
git add .
git commit -m "feat: description"
git push origin main
```

---

### API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main UI |
| `/api/upload` | POST | Upload CSV file |
| `/api/analyze` | POST | Analyze movers |
| `/api/generate` | POST | Generate tweets |
| `/api/export` | POST | Export to JSON |
| `/api/download/<filename>` | GET | Download export |
| `/api/config` | GET | Get config |

---

### File Locations

**Uploads**: `data/uploads/`
**Exports**: `data/exports/`
**Logs**: (not yet implemented)
**Config**: `config.py`
**Templates**: `modules/templates.py`

---

### Support Contacts

**Developer**: [Your Name]
**Platform**: Novig
**Repository**: github.com/[username]/nfl-social-generator
**Deployment**: [vercel-url].vercel.app

---

## 📖 NOTES & LEARNINGS

### Design Decisions

**Why Flask over FastAPI?**
- Simpler for MVP
- Better Vercel support
- More template examples available
- Team familiarity

**Why Pandas over raw CSV?**
- Built-in data validation
- Easy filtering and sorting
- Statistical functions
- DataFrame → JSON conversion

**Why template-based over AI-first?**
- Cost (no API fees in Phase 1)
- Reliability (templates always work)
- Speed (instant generation)
- Can add AI in Phase 3 as enhancement

**Why Vercel over Heroku/AWS?**
- Free tier sufficient
- Zero-config deployment
- Automatic HTTPS
- GitHub integration
- Serverless = no server management

---

### Performance Benchmarks

**Local Testing** (M1 Mac):
- CSV upload (1000 rows): ~0.5 seconds
- Movement analysis: ~0.2 seconds
- Tweet generation (10 movers): ~0.1 seconds
- Total workflow: ~1 second

**Production** (Vercel):
- TBD after deployment

---

### Security Considerations

**Current**: Basic
- File upload size limit (10MB)
- File type validation (.csv only)
- Filename sanitization
- No authentication (public tool)

**Phase 2 Improvements**:
- Add user authentication
- Rate limiting
- CSRF protection
- Input sanitization
- API key management for NFL data

---

## 🎓 DEVELOPMENT PRINCIPLES

### Code Quality
- **Readability**: Clear variable names, docstrings, comments
- **Modularity**: Separate concerns, reusable functions
- **Testability**: Pure functions where possible
- **Documentation**: Every module has purpose statement

### User Experience
- **Speed**: < 3 second response times
- **Clarity**: Clear error messages
- **Simplicity**: 4-step workflow, no complexity
- **Forgiveness**: Validate input, handle errors gracefully

### Maintainability
- **Logging**: Track errors and usage (Phase 2)
- **Monitoring**: Vercel analytics
- **Versioning**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Documentation**: Keep PROJECT_BRAIN.md updated

---

## 🔄 UPDATE PROTOCOL

**When to Update This File**:
1. After completing any phase
2. When adding/removing features
3. After fixing significant bugs
4. When making architecture changes
5. After deployment changes
6. When learning something important

**How to Update**:
1. Add entry to CHANGE LOG with version bump
2. Update relevant section (Architecture, Known Issues, etc.)
3. Update Current Status if phase changes
4. Commit with message: `docs: update PROJECT_BRAIN`

---

## 💭 SCRATCH PAD / NOTES

### Ideas to Explore
- [ ] Voice interface for hands-free content generation?
- [ ] Browser extension to pull odds directly from competitor sites?
- [ ] Slack bot integration for team notifications?
- [ ] Weekly digest email of top movers?

### Questions to Answer
- What's the ideal number of tweet variations? (Currently 3)
- Should we auto-post tweets or keep human in the loop?
- How often does odds data update? (affects caching strategy)
- Which markets get the most engagement? (informs template priority)

### Random Notes
- Consider adding "hot take" toggle for more aggressive tweet styles
- Emojis increase engagement but some users prefer clean text
- Hashtag strategy: #NFL always, #SportsBetting sometimes, team tags?
- Character count sweet spot seems to be 240-260 (not max 280)

---

**Last Updated**: January 2025
**Next Review**: After Phase 2 completion
**Maintained By**: Development Team

---

*This is a living document. Keep it updated as the project evolves.*
