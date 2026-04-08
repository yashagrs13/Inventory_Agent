# src/stream_capture.py
import sys
import io
import json
import queue
import threading
import re
from datetime import datetime


class CrewOutputCapture:
    """
    Captures CrewAI verbose output by redirecting stdout.
    Parses the output into structured SSE events.
    """

    def __init__(self):
        self.event_queue = queue.Queue()
        self._original_stdout = None
        self._capture_buffer = io.StringIO()
        self._lock = threading.Lock()

    def start_capture(self):
        """Start capturing stdout."""
        self._original_stdout = sys.stdout
        sys.stdout = self

    def stop_capture(self):
        """Restore original stdout."""
        if self._original_stdout:
            sys.stdout = self._original_stdout
            self._original_stdout = None

    def write(self, text):
        """Intercept stdout writes, parse and queue as events."""
        # Always write to original stdout too (for server logs)
        if self._original_stdout:
            self._original_stdout.write(text)

        if not text or text.strip() == '':
            return

        with self._lock:
            event = self._parse_output(text.strip())
            if event:
                self.event_queue.put(event)

    def flush(self):
        """Required for stdout compatibility."""
        if self._original_stdout:
            self._original_stdout.flush()

    def _parse_output(self, text):
        """Parse CrewAI verbose output into structured events."""
        timestamp = datetime.now().isoformat()

        # Skip empty or whitespace-only
        if not text:
            return None

        # Agent starting work
        if 'Working Agent:' in text or 'starting work' in text.lower():
            agent_name = text.split(':')[-1].strip() if ':' in text else text
            return {
                'type': 'agent_start',
                'agent': agent_name,
                'content': text,
                'timestamp': timestamp
            }

        # Tool usage
        if 'Using tool:' in text or 'Tool:' in text:
            return {
                'type': 'tool_call',
                'content': text,
                'timestamp': timestamp
            }

        # Tool output/result
        if 'Tool Output:' in text or 'tool output' in text.lower():
            return {
                'type': 'tool_result',
                'content': text,
                'timestamp': timestamp
            }

        # Agent thinking / reasoning
        if 'Thought:' in text or 'thinking' in text.lower():
            return {
                'type': 'thought',
                'content': text,
                'timestamp': timestamp
            }

        # Task completion
        if 'Final Answer:' in text or 'finished' in text.lower():
            return {
                'type': 'agent_complete',
                'content': text,
                'timestamp': timestamp
            }

        # Agent delegation
        if 'Action:' in text:
            return {
                'type': 'action',
                'content': text,
                'timestamp': timestamp
            }

        # Action input
        if 'Action Input:' in text:
            return {
                'type': 'action_input',
                'content': text,
                'timestamp': timestamp
            }

        # Default: general log
        return {
            'type': 'log',
            'content': text,
            'timestamp': timestamp
        }

    def get_events(self):
        """Generator that yields events as SSE-formatted strings."""
        while True:
            try:
                event = self.event_queue.get(timeout=0.5)
                yield f"data: {json.dumps(event)}\n\n"
            except queue.Empty:
                # Send keepalive to prevent connection timeout
                yield f"data: {json.dumps({'type': 'keepalive', 'timestamp': datetime.now().isoformat()})}\n\n"

    def drain_events(self):
        """Get all queued events without blocking."""
        events = []
        while not self.event_queue.empty():
            try:
                events.append(self.event_queue.get_nowait())
            except queue.Empty:
                break
        return events
