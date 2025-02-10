import time

class TimeChecker:
    def start(self):
        self.init_time = time.time()
    def stop(self):
        self.end_time = time.time()
        self.time_elapsed = self.end_time - self.init_time
        return self._print()
    def _print(self):
        if not self.time_elapsed:
            print("Time not calculated")
            return
        return_time = f"Time elapsed: {int(self.time_elapsed/60/60)}:{'' if self.time_elapsed/60 > 10 else '0'}{int(self.time_elapsed/60)}:{int(self.time_elapsed%60)}"
        print(return_time)
        return return_time
