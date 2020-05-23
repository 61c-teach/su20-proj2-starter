import os
import json
import subprocess

VENUS_PATH = "../tools/venus.jar"

class FileCompare:
    def __init__(self, reference, student):
        self.reference = reference
        self.student = student
    
    def compare(self) -> bool:
        if not os.path.isfile(self.reference):
            print(f"Could not find the reference file {self.reference}!")
            return False
        if not os.path.isfile(self.student):
            print(f"Could not find the student output file {self.student}!")
            return False
        with open(self.reference, "rb") as r:
            with open(self.student, "rb") as s:
                ref = r.read()
                std = s.read()
                if ref == std:
                    return True
                else:
                    print("~" * 20)
                    print(f"The student and reference files differed!")
                    print("~" * 20)
                    print(f"Reference ({self.reference}):")
                    print(ref.hex())
                    print(f"Actual ({self.student}):")
                    print(std.hex())
                    return False
TEST_COUNTER = 1
class TestCase:
    def __init__(self, name, test_file, id, args=[], stdout="", stderr="", exitcode=0, cwd=None, timeout=10, compare_files=[]):
        self.name = name
        self.test_file = test_file
        self.id = id
        self.args = args
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode
        self.cwd = cwd
        self.timeout = timeout
        self.compare_files = [FileCompare(**cf) for cf in compare_files]

    def run(self, test_file_path: str):
        try:
            print("*" * 40)
            global TEST_COUNTER
            print(f"[{TEST_COUNTER}] Running {self.name}...")
            TEST_COUNTER += 1
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
            for cf in self.compare_files:
                passing = cf.compare() and passing
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
                        tests += TestCase.loadTestFromList(t)
                    elif isinstance(t, dict):
                        tests.append(TestCase.loadTest(t))
                    else:
                        print(f"Unknown test input from {file}!")

            except Exception:
                print(f"Could not load tests in {file}!")
                import traceback
                traceback.print_exc()
    return tests

def main(args):
    tests = sorted(load_tests("test_cases"), key=lambda tc: tc.id)
    passed = 0
    ran = 0
    for test in tests:
        if len(args) > 1 and test.id not in args:
            continue
        ran += 1
        if test.run("assembly"):
            passed += 1
    print("\n" + ("=" * 40))
    print(f"Passed {passed} / {ran} tests!")
    print("=" * 40)

if __name__ == "__main__":
    import sys
    main(sys.argv)