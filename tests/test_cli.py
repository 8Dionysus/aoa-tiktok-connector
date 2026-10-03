from __future__ import annotations

import json

from aoa_tiktok_connector.cli import doctor_packet, main


def test_doctor_packet_is_fail_closed() -> None:
    packet = doctor_packet()
    assert packet["connector_id"] == "aoa-tiktok-connector"
    assert packet["provider"] == "tiktok"
    assert packet["phase"] == "experimental"
    assert packet["network_touched"] is False
    assert packet["write_effects_enabled"] is False
    assert packet["runtime_deployed"] is False
    assert packet["ready"] is False


def test_doctor_json(capsys) -> None:
    assert main(["doctor", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["connector_id"] == "aoa-tiktok-connector"
    assert payload["source_adapter"] == "implemented_unadmitted"
    assert payload["publication_adapter"] == "not_implemented"
