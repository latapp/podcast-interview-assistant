import time

class TimeChecker:
    def start(self):
        self.init_time = time.time()
    def stop(self):
        self.end_time = time.time()
        self.time_elapsed = self.end_time - self.init_time
        self._print()
    def _print(self):
        if not self.time_elapsed:
            print("Time not calculated")
            return
        print(f"Time elapsed: {int(self.time_elapsed/60/60)}:{'' if self.time_elapsed/60 > 10 else '0'}{int(self.time_elapsed/60)}:{int(self.time_elapsed%60)}")