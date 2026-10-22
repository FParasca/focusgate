import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='focusgate.log', 
)

def main():
    if "--worker" in sys.argv:
        from focusgate.block import run_blocker
        run_blocker()
    else:
        from focusgate.launcher import run_launcher
        run_launcher()

if __name__ == "__main__":
    main()