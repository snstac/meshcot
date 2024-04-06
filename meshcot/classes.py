#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright Sensors & Signals LLC https://www.snstac.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""MeshCOT Class Definitions."""

import asyncio

import json
import platform
from typing import Optional

import asyncio_mqtt as aiomqtt

import pytak
import meshcot

from pubsub import pub

import pytak

import meshtastic
import meshtastic.serial_interface
from meshtastic.util import (
    Timeout,
    camel_to_snake,
    fromPSK,
    our_exit,
    pskToString,
    stripnl,
    message_to_json,
)

from dotmap import DotMap
from pubsub import pub

import json

__author__ = "Greg Albrecht <gba@snstac.com>"
__copyright__ = "Copyright Sensors & Signals LLC https://www.snstac.com"
__license__ = "Apache License, Version 2.0"


class MQTTWorker(pytak.QueueWorker):
    """Queue Worker for MQTT."""

    async def run(self, _=-1) -> None:
        """Run this Thread, Reads from Pollers."""
        self._logger.info("Run: MQTTWorker")

        client_id = self.config.get("MQTT_CLIENT_ID", "meshcot")
        topic = self.config.get("MQTT_TOPIC", meshcot.DEFAULT_MQTT_TOPIC)
        broker = self.config.get("MQTT_BROKER", meshcot.DEFAULT_MQTT_BROKER)
        port = self.config.get("MQTT_PORT", meshcot.DEFAULT_MQTT_PORT)
        mqtt_username = self.config.get("MQTT_USERNAME")
        mqtt_password = self.config.get("MQTT_PASSWORD")

        self._logger.info("Using MQTT Broker: %s:%d/%s", broker, port, topic)

        async with aiomqtt.Client(
            hostname=broker,
            port=port,
            username=mqtt_username,
            password=mqtt_password,
            client_id=client_id,
        ) as client:
            self._logger.info("Connected to MQTT Broker %s:%d/%s", broker, port, topic)
            while 1:
                data = await self.queue.get()
                if not data:
                    await asyncio.sleep(0.01)
                j_data = json.dumps(data)
                self._logger.debug("Publishing %s", j_data)
                await client.publish("meshcot", payload=j_data)


class MeshWorker(pytak.QueueWorker):
    """Queue Worker for Mesh."""

    def __init__(self, queue, net_queue, config):
        """Initialize this class."""
        super().__init__(queue, config)
        self.net_queue = net_queue
        self.config = config
        self.interface = None
        self.mesh_iface = self.config.get("MESH_IFACE", meshcot.DEFAULT_MESH_IFACE)

    def on_receive(self, packet, interface):  # called when a packet arrives
        payload = {
            "meta": {
                "node_id": platform.node(),
                "interface": str(interface),
                "mesh_iface": self.mesh_iface,
                "packet_len": len(packet),
            }
        }

        raw = packet.get("raw")
        if raw:
            pl = json.loads(message_to_json(raw))
            payload = pl | payload

        decoded = packet.get("decoded")
        if decoded:
            payload["meta"]["decoded_len"] = len(decoded)
            for d_key, d_val in decoded.items():
                if d_key not in ["payload", "requestId", "portnum"]:
                    if not isinstance(d_val, dict):
                        continue
                    if d_val.get("raw"):
                        del d_val["raw"]
                    payload["decoded"] = payload["decoded"] | d_val
            payload["decoded"]["requestId"] = decoded.get("requestId")
            payload["decoded"]["portnum"] = decoded.get("portnum")

        self._logger.debug("payload=%s", payload)
        self.net_queue.put_nowait(payload)

    def on_connection(self, interface, topic=pub.AUTO_TOPIC):
        self._logger.info("Connected to %s/%s", interface, topic)

    async def run(self, _=-1) -> None:
        """Run the main process loop."""
        self._logger.info("Run: MeshWorker")
        self._logger.info("Using MESH_IFACE=%s", self.mesh_iface)
        pub.subscribe(self.on_receive, "meshtastic.receive")
        pub.subscribe(self.on_connection, "meshtastic.connection.established")
        self.interface = meshtastic.serial_interface.SerialInterface(self.mesh_iface)
        while 1:
            await asyncio.sleep(0.01)
