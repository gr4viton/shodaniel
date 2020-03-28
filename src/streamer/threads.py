import threading
from time import sleep
from structlog import get_logger
from src.stream_thread import StreamThread


log = get_logger(__name__)


class StreamerMixinThreads:
    """Streamer methods which handles threads."""

    def threads_append(self, sources):
        for index, src in enumerate(sources):
            if not src:
                continue
            thread = self.get_stream_thread(index, src)
            self.threads.append(thread)

    def get_stream_thread(self, index, source):
        name = "stream{index}".format(index=index)
        thread = StreamThread(stream_store=self.stream_store, name=name, source=source)
        return thread

    def threads_wait_for_started_thread(self):

        while threading.activeCount() < 2:
            log.info("streamer.waiting_for_threads")
            sleep(1)

    def threads_start_all(self):
        log.info("streamer.threads.starting_all")
        for thread in self.threads:
            thread.start()
            count = threading.activeCount()
            log.info("streamer.threads.started", active_count=count)

    def threads_kill_all(self):
        log.info("streamer.threads.killing_all")
        for thread in self.threads:
            stream_data = self.stream_store[thread.name]
            if not stream_data:
                self.warning("streamer.cannot_kill_stream", thread_name=thread.name)
                continue
            stream_data["control"]["stop"] = True

        i_thread = -1
        while self.threads:
            count = threading.activeCount()
            log.info("streamer.threads.active", count=count)
            i_thread += 1
            if i_thread > len(self.threads) - 1:
                i_thread = 0

            thread = self.threads[i_thread]
            stream_data = self.stream_store[thread.name]
            if not stream_data:
                self.warning("streamer.cannot_kill_stream", thread_name=thread.name)
                continue

            else:
                killed = stream_data["control"].get("killed")
                if killed:
                    thread.join()
                    self.threads.remove(thread)
                    log.info("streamer.thread", is_alive=thread.isAlive())
                    continue
                log.warning("streamer.waiting_for_tread_finishing_as_killed", thread_name=thread.name)
                sleep(0.3)

        count = threading.activeCount()
        log.info("streamer.threads.active", count=count)
