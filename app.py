import time

from datetime import datetime
from flask import Flask, Response

app = Flask(__name__)

HTML = """
<body>
<pre id="contents"></pre>
<script>
    let contents = document.querySelector("#contents");
    let sse = new EventSource("/sse");

    const println = (string) => {
        const text = document.createTextNode(`${string}\\n`);
        contents.appendChild(text);
    };

    sse.onopen = () => {
        println("SSE connection open");
    };

    sse.onmessage = (event) => {
        println(`SSE: ${event.data}`);
    };

    sse.onerror = () => {
        println("SSE connection error");
    };
</script>
</body>
"""


@app.route('/')
def root():
    return Response(HTML, mimetype='text/html')


@app.route('/sse')
def sse():
    def generate():
        while True:
            now = datetime.now().ctime()

            yield ': this is a comment\n'
            yield f'data: {now}\n'
            yield '\n'

            time.sleep(3)

    return Response(generate(), mimetype='text/event-stream')
