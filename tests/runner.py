import os
import json
import subprocess

VENUS_PATH = "../utils/venus.jar"

class TestCase:
    def __init__(self, name, test_file, args=[], stdout="", stderr="", exitcode=0, cwd=None, timeout=80):
        self.name = name
        self.test_file = test_file
        self.args = args
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode
        self.cwd = cwd
        self.timeout = timeout

    def run(self, test_file_path: str):
        try:
            print("*" * 40)
            print(f"Running {self.name}...")
            print("*" * 40)
            filepath = os.path.join(test_file_path, self.test_file)
            p = subprocess.Popen(["java", "-jar", VENUS_PATH, filepath] + self.args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.cwd, universal_newlines = True, bufsize=100)
            try:
                out, err = p.communicate(timeout = self.timeout)
            except subprocess.TimeoutExpired:
                p.kill()
                print("The test timed out testing your RISC-V function!")
                self.print_end("TIMEOUT")
                return False
            passing = True
            if out != self.stdout:
                print("~" * 20)
                print("STDOUT MISMATCH")
                print("~" * 20)
                print("Expected:")
                print("-" * 20)
                print(self.stdout)
                print("-" * 20)
                print("Actual:")
                print("-" * 20)
                print(out)
                print("-" * 20)
                passing = False
            if err != self.stderr:
                print("~" * 20)
                print("STDERR MISMATCH")
                print("~" * 20)
                print("Expected:")
                print("-" * 20)
                print(self.stderr)
                print("-" * 20)
                print("Actual:")
                print("-" * 20)
                print(err)
                print("-" * 20)
                passing = False
            if p.returncode != self.exitcode:
                print("~" * 20)
                print("Return code MISMATCH")
                print("~" * 20)
                print(f"Expected: {self.exitcode}, Actual: {p.returncode}")
                passing = False
            if passing:
                self.print_end("PASSED")
                return True
            else:   
                self.print_end("FAILED")
                return False
        except Exception as e:
            print(e)
            self.print_end("ERRORED")
            return False
    @staticmethod
    def print_end(msg):
        print("-" * 40)
        print(msg)
        print("-" * 40)
        print()

    @staticmethod
    def loadTestFromList(l: list) -> ["TestCase"]:
        tests = []
        for t in l:
            tests.append(TestCase.loadTest(t))
        return tests

    @staticmethod
    def loadTest(d: dict) -> "TestCase":
        return TestCase(**d)

def load_tests(path):
    tests = []
    files = os.listdir(path)
    for file in files:
        if file.endswith(".json"):
            try:
                with open(os.path.join(path, file), "r") as f:
                    t = json.load(f)
                    if isinstance(t, list):
                        tests.append(TestCase.loadTestFromList(t))
                    elif isinstance(t, dict):
                        tests.append(TestCase.loadTest(t))
                    else:
                        print(f"Unknown test input from {file}!")

            except Exception:
                print(f"Could not load tests in {file}!")
                import traceback
                traceback.print_exc()
    return tests

def main():
    tests = load_tests("test_cases")
    passed = 0
    for test in tests:
        if test.run("assembly"):
            passed += 1
    print("\n" + ("=" * 40))
    print(f"Passed {passed} / {len(tests)} tests!")
    print("=" * 40)

if __name__ == "__main__":
    main()