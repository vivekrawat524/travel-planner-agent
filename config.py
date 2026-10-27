"""Central configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

MAX_CRITIC_ITERATIONS = int(os.getenv("MAX_CRITIC_ITERATIONS", "2"))
