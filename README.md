# 🏈 NFL Social Content Generator

Automated social media content generation for NFL futures odds movement. Built for Novig sports betting platform.

[![GitHub](https://img.shields.io/badge/GitHub-nfl--social--generator-blue?logo=github)](https://github.com/goldytalks/nfl-social-generator)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/goldytalks/nfl-social-generator)

## 🌐 Deployment

**GitHub Repository:** [github.com/goldytalks/nfl-social-generator](https://github.com/goldytalks/nfl-social-generator)

**Live Demo:** Coming soon! (Deploy via Vercel - see [DEPLOYMENT.md](DEPLOYMENT.md))

**Quick Deploy:**
```bash
# Clone the repo
git clone https://github.com/goldytalks/nfl-social-generator.git
cd nfl-social-generator

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
# Visit http://localhost:5000
```

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete deployment instructions to Vercel.

## Overview

This tool automates the process of identifying significant odds movements in NFL futures markets and generating compelling tweet drafts that showcase market intelligence. It turns raw odds data into ready-to-post social content.

## Features (Phase 1 - MVP)

✅ **CSV Import & Validation** - Upload and validate NFL futures odds data
✅ **Movement Analysis** - Identify biggest week-over-week movers with configurable thresholds
✅ **Smart Categorization** - Classify movers as risers/fallers with magnitude ratings
✅ **Template-Based Tweet Generation** - Multiple variations per market type
✅ **Clean Web Interface** - Simple, intuitive UI for the entire workflow
✅ **Export Functionality** - Save generated tweets as JSON for record-keeping

## Project Structure

```
nfl-social-generator/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── modules/
│   ├── __init__.py            # Package initialization
│   ├── csv_processor.py       # CSV import & validation
│   ├── movers_analyzer.py     # Movement analysis logic
│   ├── tweet_generator.py     # Tweet generation engine
│   └── templates.py           # Tweet templates by market type
├── data/
│   ├── sample_odds.csv        # Example odds data
│   ├── uploads/               # Uploaded CSV files
│   └── exports/               # Generated tweet exports
├── static/
│   ├── style.css              # Frontend styles
│   └── script.js              # Frontend JavaScript
└── templates/
    └── index.html             # Main web interface
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Navigate to project directory:**
```bash
cd nfl-social-generator
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Open in browser:**
```
http://localhost:5000
```

## Usage

### 1. Prepare Your CSV

Your CSV must include these columns:
- `market` - Market type (e.g., "To Make The Playoffs", "MVP")
- `team_player` - Team or player name
- `last_week_pct` - Last week's implied probability (%)
- `this_week_pct` - This week's implied probability (%)
- `change_pct` - Percentage point change
- `last_week_american` - Last week's American odds
- `this_week_american` - This week's American odds

**Example CSV format:**
```csv
market,team_player,last_week_pct,this_week_pct,change_pct,last_week_american,this_week_american
To Make The Playoffs,Detroit Lions,75.00,81.13,6.13,-300,-430
MVP,Jared Goff,5.20,8.50,3.30,+1823,+1076
```

See `data/sample_odds.csv` for a complete example.

### 2. Upload & Analyze

1. **Upload CSV** - Click "Upload CSV" and select your file
2. **Configure Settings:**
   - Movement Threshold: Minimum % change to be considered a "mover" (default: 2.0%)
   - Top N Movers: How many movers to analyze (default: 10)
3. **Analyze** - Click "Analyze Movers" to identify biggest movements

### 3. Generate Tweets

1. Click "Generate Tweets" to create drafts for all movers
2. Review multiple variations per mover
3. Each tweet includes:
   - Eye-catching hook
   - Odds movement details
   - Contextual analysis (placeholder in Phase 1)
   - Call to action
4. Copy tweets directly to clipboard

### 4. Export Results

Click "Export to JSON" to save all generated content with metadata for record-keeping.

## Configuration

Edit `config.py` to customize:

```python
MOVEMENT_THRESHOLD = 2.0      # Min % change for movers
TOP_N_MOVERS = 10             # Number of movers to analyze
TWEET_VARIATIONS = 3          # Draft versions per mover
INCLUDE_EMOJIS = True         # Toggle emoji usage
CHARACTER_LIMIT = 280         # Tweet length limit
```

## Tweet Templates

The tool includes specialized templates for different market types:

- **Playoffs Markets** - Focus on recent games, division standings
- **MVP Markets** - Highlight player performance and narrative
- **Championship Markets** - Emphasize team trends and title chances
- **Generic Fallback** - Works for any market type

Each template generates 3 variations:
- **Version A** - Bold & attention-grabbing
- **Version B** - Clean & data-focused
- **Version C** - Analytical & professional

## Example Output

### Input Data
```csv
To Make The Playoffs,Detroit Lions,75.00,81.13,6.13,-300,-430
```

### Generated Tweets

**Version A:**
```
🔥 BIGGEST MOVER: Lions playoff odds surged from -300 to -430 this week (+6.1%)

Recent wins and strong performance have boosted their postseason outlook.

Our markets are reacting. Are you? 🏈

#NFL #SportsBetting
```

**Version B:**
```
Detroit Lions just became -430 favorites to make the playoffs (was -300 last week).

Recent wins and strong performance have boosted their postseason outlook.

The market knows. 📈

#NFL
```

## API Endpoints

The application provides RESTful API endpoints:

- `POST /api/upload` - Upload CSV file
- `POST /api/analyze` - Analyze movers (with threshold/top_n params)
- `POST /api/generate` - Generate tweet drafts (with optional contexts)
- `POST /api/export` - Export results to JSON
- `GET /api/config` - Get current configuration

## Future Phases

### Phase 2 - NFL Data Integration
- [ ] Connect to SDQL or NFL data API
- [ ] Auto-fetch recent game results
- [ ] Pull current standings and records
- [ ] Retrieve injury reports
- [ ] Generate context automatically

### Phase 3 - Polish
- [ ] Advanced AI for creative variations (OpenAI integration)
- [ ] Twitter preview styling
- [ ] Inline tweet editing
- [ ] Batch processing improvements
- [ ] Performance analytics

### Phase 4 - Advanced Features
- [ ] Image generation with odds charts
- [ ] Direct Twitter posting (OAuth)
- [ ] Historical performance tracking
- [ ] A/B testing framework

## Troubleshooting

### CSV Upload Fails
- Ensure all required columns are present
- Check for proper CSV formatting
- Verify numeric values are valid

### No Movers Found
- Lower the movement threshold
- Check that `change_pct` values are calculated correctly
- Verify data contains actual movement (not all zeros)

### Character Count Over Limit
- Some templates may exceed 280 characters
- Edit the template in `modules/templates.py`
- Or manually edit before posting

## Development

### Adding New Market Templates

Edit `modules/templates.py` and add to the appropriate market dictionary:

```python
MY_MARKET_TEMPLATES = {
    'riser': [
        {
            'name': 'Version A',
            'template': 'Your template here with {placeholders}'
        }
    ]
}
```

### Modifying Tweet Format

Templates support these placeholders:
- `{team}` or `{team_player}` - Team/player name
- `{player}` - Player name (for MVP markets)
- `{market}` - Market name
- `{last_odds}` - Previous odds
- `{this_odds}` - Current odds
- `{change}` - Percentage change
- `{context}` - Contextual analysis
- `{emoji}`, `{emoji2}`, `{team_emoji}` - Emoji elements

## Contributing

This is a Phase 1 MVP. Suggestions for improvement:

1. Better placeholder context generation
2. More tweet template variations
3. UI/UX improvements
4. Performance optimizations

## License

Proprietary - Built for Novig

## Support

For issues or questions, contact the development team.

---

**Built with:** Python, Flask, Pandas, JavaScript
**Version:** 1.0.0 (Phase 1 MVP)
**Last Updated:** 2025
