# Interactive LLM-Powered Quiz Generator

An interactive quiz generation system powered by Google's Gemini AI, built with Streamlit. The system enables dynamic quiz creation with customizable parameters and supports multiple question types.

## System Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌────────────────┐
│  Streamlit UI   │────▶│  Quiz Engine │────▶│   Gemini API   │
└─────────────────┘     └──────────────┘     └────────────────┘
        ▲                      │                      │
        │                      ▼                      │
        │              ┌──────────────┐              │
        └──────────────│ Parser/Format│◀─────────────┘
                       └──────────────┘
```

### Architectural Components

1. **Frontend Layer (Streamlit)**
   - Interactive form-based parameter collection
   - Real-time quiz preview
   - Interactive quiz taking interface
   - Dynamic result visualization
   - Session state management
   - Error handling and user feedback

2. **Quiz Engine Layer**
   - Parameter validation and preprocessing
   - Dynamic prompt construction
   - Response validation
   - Quiz state management
   - Error handling and fallback mechanisms

3. **LLM Integration Layer (Gemini)**
   - Model: Gemini 1.5 Flash
   - API integration and error handling
   - Response processing
   - Fallback to mock data on failure

4. **Parser Layer**
   - Regular expression-based parsing
   - Format validation
   - Structure normalization
   - Error recovery

## Technical Implementation

### Model Details
```python
Model: Gemini 1.5 Flash
Purpose: Text Generation & Understanding
Context Window: ~1000 tokens
Response Format: Structured Text
Features:
- Multi-format question generation
- Context-aware responses
- Format adherence
- Error resilience
```

### Data Flow Process

1. **Input Processing**
   ```python
   User Input → Parameter Validation → Quiz Configuration
   │
   ├── Topic Selection
   ├── Difficulty Level
   ├── Question Count
   ├── Question Types
   └── Optional Parameters
       ├── Subtopics
       ├── Keywords
       ├── Target Audience
       └── Language
   ```

2. **Prompt Engineering**
   ```python
   Configuration → Prompt Template → Final Prompt
   │
   ├── Template Selection
   │   ├── Multiple Choice Format
   │   ├── True/False Format
   │   └── Short Answer Format
   │
   ├── Parameter Injection
   └── Format Validation
   ```

3. **LLM Integration**
   ```python
   Prompt → Gemini API → Raw Response
   │
   ├── API Configuration
   │   ├── Model: gemini-1.5-flash
   │   └── Parameters:
   │       ├── Temperature
   │       └── Max Tokens
   │
   ├── Error Handling
   │   ├── Connection Issues
   │   ├── Rate Limiting
   │   └── Invalid Responses
   │
   └── Mock Data Fallback
   ```

4. **Response Processing**
   ```python
   Raw Response → Parser → Structured Quiz
   │
   ├── Text Splitting
   ├── Format Detection
   ├── Content Extraction
   └── JSON Construction
   ```

### Session Management

```python
Session State
├── Quiz Data
│   ├── Questions
│   ├── Answers
│   └── Explanations
│
├── User State
│   ├── Current Answers
│   ├── Submission Status
│   └── Score
│
└── UI State
    ├── Selected Tab
    ├── Form Values
    └── Display Flags
```

### Quiz Interaction Flow

```
                 ┌────────────────┐
User Input ─────▶│ Quiz Creation  │
                 └───────┬────────┘
                        │
                        ▼
                 ┌────────────────┐
                 │ Question       │
                 │ Generation     │
                 └───────┬────────┘
                        │
                        ▼
                 ┌────────────────┐
                 │ Answer         │
                 │ Collection     │
                 └───────┬────────┘
                        │
                        ▼
                 ┌────────────────┐
                 │ Validation &   │
                 │ Scoring        │
                 └────────────────┘
```

## Features and Capabilities

### Question Types
1. **Multiple Choice**
   - 4 options per question
   - Single correct answer
   - Option randomization
   - Letter-based selection (a, b, c, d)

2. **True/False**
   - Binary choice questions
   - Statement validation
   - Clear formatting

3. **Short Answer**
   - Free text input
   - Case-insensitive matching
   - Basic answer validation

### Validation System
```python
Validation Levels
├── Input Validation
│   ├── Required Fields
│   ├── Format Checking
│   └── Range Validation
│
├── Response Validation
│   ├── Format Compliance
│   ├── Content Completeness
│   └── Structure Verification
│
└── Answer Validation
    ├── Type-Specific Checking
    ├── Score Calculation
    └── Feedback Generation
```

## Development and Extension

### Adding New Features
1. **New Question Types**
   ```python
   1. Update Prompt Template
   2. Extend Parser Logic
   3. Add UI Components
   4. Update Validation System
   5. Test Integration
   ```

2. **Model Updates**
   ```python
   1. Update API Configuration
   2. Adjust Prompt Structure
   3. Modify Response Parsing
   4. Update Error Handling
   5. Verify Compatibility
   ```

## Future Enhancements

1. **Technical Improvements**
   - Advanced answer validation
   - Response quality metrics
   - Performance optimization
   - Caching system

2. **Feature Additions**
   - Image-based questions
   - Multi-language support
   - Question difficulty adjustment
   - Advanced analytics

## Setup and Installation

1. Clone and install dependencies:
   ```powershell
   git clone <repository-url>
   cd quiz-generator
   pip install -r requirements.txt
   ```

2. Configure Gemini API:
   ```powershell
   $env:GEMINI_API_KEY="your-api-key-here"
   ```

3. Run the application:
   ```powershell
   streamlit run llm_quiz_app.py
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.


