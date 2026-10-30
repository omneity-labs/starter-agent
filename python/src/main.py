import sys
from agent import run_agent

if __name__ == "__main__":
    print(run_agent(" ".join(sys.argv[1:]) or "What time is it in UTC?"))
