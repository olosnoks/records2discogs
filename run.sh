#!/bin/bash
# Run vinyl record indexing and cleanup from root directory

echo ""
echo "========================================"
echo "RECORDS2DISCOGS - Vinyl Indexing"
echo "========================================"
echo ""

# Get script directory (root of repo)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_PATH="$SCRIPT_DIR/vinyl-record-indexing/app.py"
CLEANUP_PATH="$SCRIPT_DIR/indexing-output/cleanup.py"

# Check if app.py exists
if [ ! -f "$APP_PATH" ]; then
    echo "❌ Error: app.py not found at $APP_PATH"
    exit 1
fi

# Check if cleanup.py exists
if [ ! -f "$CLEANUP_PATH" ]; then
    echo "⚠️  Warning: cleanup.py not found at $CLEANUP_PATH"
    echo "Continuing without cleanup..."
    echo ""
    RUN_CLEANUP=false
else
    RUN_CLEANUP=true
fi

# Run the indexing app
echo "✅ Starting vinyl indexing..."
echo "📂 Location: $APP_PATH"
echo ""

cd "$SCRIPT_DIR/vinyl-record-indexing"
python app.py
INDEXING_EXIT_CODE=$?

# Return to root
cd "$SCRIPT_DIR"

# Run cleanup if indexing succeeded
if [ $INDEXING_EXIT_CODE -eq 0 ] && [ "$RUN_CLEANUP" = true ]; then
    echo ""
    echo "========================================"
    echo "Running Cleanup Script"
    echo "========================================"
    echo ""
    
    cd "$SCRIPT_DIR/indexing-output"
    python cleanup.py
    cd "$SCRIPT_DIR"
elif [ $INDEXING_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "⚠️  Indexing did not complete successfully. Skipping cleanup."
fi

echo ""
echo "========================================"
echo "Session complete"
echo "========================================"
echo ""
