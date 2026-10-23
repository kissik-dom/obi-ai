"""Verify FreeCAD / OpenSCAD ISO 4762 M3/M4 Screw Torque & NASA BPP Propulsion FEM Endpoints."""

from fastapi.testclient import TestClient

from backend.main import app


def test_freecad_iso4762_screw_and_propulsion_fem() -> None:
    with TestClient(app) as client:
        m3 = client.post(
            "/api/engineering/freecad/screw",
            json={"thread_spec": "M3x10mm ISO 4762", "material": "Al 7075-T6", "boss_count": 8},
        )
        assert m3.status_code == 200
        assert m3.json()["recommended_torque_nm"] == 1.2
        assert "iso4762_boss" in m3.json()["openscad_script"]

        m4 = client.post(
            "/api/engineering/freecad/screw",
            json={"thread_spec": "M4x12mm ISO 4762", "material": "Ti-6Al-4V", "boss_count": 12},
        )
        assert m4.status_code == 200
        assert m4.json()["recommended_torque_nm"] == 2.9

        fem = client.post(
            "/api/engineering/anti-gravity",
            json={"mode": "mach_effect_piezo_resonator", "drive_freq_khz": 36.4},
        )
        assert fem.status_code == 200
        assert fem.json()["status"] == "fem_converged_verified"
