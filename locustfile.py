#!/usr/bin/python
# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/python
#

#!/usr/bin/python
#


import json
import random
import uuid
from locust import HttpUser, task, between

from opentelemetry import context, baggage, trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

# Instrumenting manually to avoid error with locust gevent monkey
RequestsInstrumentor().instrument()
URLLib3Instrumentor().instrument()

class WebsiteUser(HttpUser):
    wait_time = between(1, 10)

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def browse_owner(self):
        self.client.get(f"/owners/{random.randint(1, 10)}")

    @task(2)
    def edit_pet(self):
        self.client.get(f"/owners/{random.randint(1, 10)}/pets/{random.randint(1, 5)}/edit")
