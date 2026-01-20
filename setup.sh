#!/bin/bash
# Setup script for HealthPalAI - Run this after cloning the repository

echo "🏥 HealthPalAI Setup Script"
echo "============================"
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "✅ .env file already exists"
else
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env file and add your actual API keys!"
    echo ""
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✨ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit the .env file and add your MISTRAL_API_KEY"
echo "2. (Optional) Generate a secure SECRET_KEY with: python -c 'import secrets; print(secrets.token_hex(32))'"
echo "3. Run the application with: python app.py"
echo ""
echo "📚 For more information, see SECURITY_FIXES.md"
