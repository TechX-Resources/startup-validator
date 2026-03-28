import json
import os
import hashlib
from datetime import datetime
from typing import Any

def save_data(data: Any, category: str, base_filename: str) -> str:
    """
    Save data to data/raw or data/processed as a JSON file.
    category: 'raw' or 'processed'
    base_filename: name of the tool, e.g. 'web_search'
    """
    # 1. Determine base path
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    target_dir = os.path.join(root_dir, 'data', category)
    
    # 2. Ensure target directory exists (though it should already have .gitkeep)
    os.makedirs(target_dir, exist_ok=True)
    
    # 3. Create a unique filename with timestamp and hash
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    data_str = json.dumps(data, sort_keys=True)
    data_hash = hashlib.md5(data_str.encode()).hexdigest()[:8]
    
    filename = f"{base_filename}_{timestamp}_{data_hash}.json"
    filepath = os.path.join(target_dir, filename)
    
    # 4. Save to JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    return filepath

def truncate_for_llm(text: str, max_chars: int = 4000) -> str:
    """Truncate text to max_chars for LLM context. TODO: Implement if needed."""
    # TODO: Optionally add "..." at end
    return text[:max_chars] if len(text) > max_chars else text
