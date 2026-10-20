"""Compile a separate Java consumer against only the candidate JAR and JDK."""

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
JAR = ROOT / "dotj-core/dotj-core-01/build/idisposable-candidate/idisposable-candidate.jar"
SOURCE = ROOT / "tools/oracle/dotj-core/java-probes/consumer/IndependentDisposableConsumer.java"
CLASSES = ROOT / "dotj-core/dotj-core-01/build/idisposable-consumer"


def main():
    CLASSES.mkdir(parents=True, exist_ok=True)
    subprocess.run(["python", str(ROOT / "tools/oracle/dotj-core/build-idisposable-candidate.py")],
                   cwd=ROOT, check=True)
    subprocess.run(["javac", "--release", "21", "-cp", str(JAR), "-d", str(CLASSES), str(SOURCE)],
                   cwd=ROOT, check=True)
    output = subprocess.run(["java", "-cp", os.pathsep.join((str(CLASSES), str(JAR))),
                             "consumer.IndependentDisposableConsumer"],
                            cwd=ROOT, capture_output=True, text=True, check=True).stdout
    assert "PASS: independent IDisposable candidate consumer" in output
    print(output.strip())


if __name__ == "__main__":
    main()
