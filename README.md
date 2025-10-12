# 🪄 Gemini-Powered Meme Generator

A powerful and intelligent meme generator powered by Google's Gemini AI. Upload any image and let AI automatically generate witty, contextual captions - or add your own custom text. Built with Streamlit for a seamless web experience.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

## ✨ Features

- **🤖 AI-Powered Captions**: Automatically generate funny, contextual meme captions using Google's Gemini AI
- **🎨 Custom Text**: Add your own bottom text or override AI-generated captions
- **🔄 Multiple AI Models**: Choose from Gemini 2.0 Flash, Gemini 1.5 Pro, Gemini 1.5 Flash, or Gemini 1.0 Pro
- **📐 Smart Text Fitting**: Automatic text wrapping and sizing to ensure captions never go out of bounds
- **🎭 Professional Styling**: Impact font with bold white text and black stroke for maximum readability
- **🌫️ Background Coverage**: Optional semi-transparent background behind text to cover existing text
- **📥 Download**: Save your generated memes instantly as JPEG files
- **🔒 Secure**: API keys stored securely using Streamlit secrets management
- **☁️ Deploy Ready**: One-click deployment to Streamlit Cloud

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Patil-Nitish/meme_generator.git
   cd meme_generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**
   
   Create a `.streamlit/secrets.toml` file in the project root:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key_here"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 🎯 Usage

1. **Upload an Image**: Click on "Upload an image (jpg/png)" and select your image file
2. **Select AI Model**: Choose your preferred Gemini model from the sidebar (default: gemini-2.0-flash)
3. **Toggle Background**: Enable/disable the semi-transparent background behind text
4. **Add Custom Text**: (Optional) Enter custom text for the bottom of the meme
5. **Generate**: Click "✨ Generate Meme with Gemini" button
6. **Download**: Save your meme using the "📥 Download Meme" button

## ☁️ Deployment to Streamlit Cloud

1. **Push your code** to GitHub (without the secrets.toml file)

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Create a new app** and connect your GitHub repository

4. **Add secrets** in the app settings:
   - Navigate to "Settings" → "Secrets"
   - Add your Gemini API key:
     ```toml
     GEMINI_API_KEY = "your_actual_gemini_api_key_here"
     ```

5. **Deploy** and share your meme generator with the world! 🎉

## 📁 Project Structure

```
meme_generator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── impact.ttf            # Impact font file for meme text
├── .streamlit/
│   └── secrets.toml      # API key configuration (not committed)
└── README.md             # This file
```

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[Google Gemini AI](https://ai.google.dev/)** - AI-powered caption generation
- **[Pillow (PIL)](https://pillow.readthedocs.io/)** - Image processing and text rendering
- **Python 3.8+** - Core programming language

## 🎨 Features in Detail

### Smart Text Rendering
- Automatic text wrapping to fit image width
- Dynamic font sizing based on image dimensions
- Maintains 4% margin from image edges
- Maximum 28% of image height for text blocks

### Professional Meme Styling
- Classic meme format with top and bottom text
- Impact font (with fallbacks to DejaVu Sans Bold or Liberation Sans Bold)
- White text with black stroke outline
- All-caps text for authentic meme aesthetic

### Security Best Practices
- API keys stored in `.streamlit/secrets.toml` (not in code)
- Secrets.toml excluded from version control
- Compatible with Streamlit Cloud's secrets management

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is available under the MIT License. Feel free to use, modify, and distribute as needed.

## 🙏 Acknowledgments

- Google Gemini AI for providing the powerful caption generation API
- Streamlit for the amazing web application framework
- The meme community for inspiration

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub or contact the repository owner.

---

**Powered by Google Gemini** 
