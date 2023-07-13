# Sample Path
import os
from pathlib import Path

ir_path = Path(__file__).parent.parent.absolute()
SAMPLES_PATH = os.path.join(ir_path, "samples")

SAMPLE_BRONZE_US_LEGISLATOR = os.path.join(SAMPLES_PATH, 'lake', 'bronze', 'us-legislators', 'person.json')
