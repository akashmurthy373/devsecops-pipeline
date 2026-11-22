# app/main.py
# DevSecOps Pipeline — Application Fixture
# This file is scanned by Bandit (SAST) on every push.


def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to the DevSecOps demo."


def add(a: int, b: int) -> int:
    """Return the sum of two numbers."""
    return a + b


def run_system_command(args: list) -> str:
    """
    Run a system command — SECURE version.

    FIX applied (Bandit B602):
      BEFORE (insecure): subprocess.run(cmd, shell=True)
        → shell=True lets attackers inject shell commands via user input.

      AFTER  (secure):   subprocess.run(args, shell=False)
        → args is a list like ["ls", "-la"], no shell interpretation happens.
    """
    import subprocess
    result = subprocess.run(args, shell=False, capture_output=True, text=True)
    return result.stdout


if __name__ == "__main__":
    print(greet("World"))
    print(f"2 + 3 = {add(2, 3)}")
