from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_status_operacional():
    resp = client.get("/status")
    assert resp.status_code == 200
    assert resp.json()["estado"] == "Operacional"


def test_health_responde():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert "status" in resp.json()


class TestEvaluacionRiesgo:
    def test_menor_de_edad_rechazado(self):
        resp = client.post("/evaluar-riesgo", json={"edad": 16, "ingresos": 2000, "deudas": 100})
        assert resp.status_code == 200
        assert resp.json()["resultado"].startswith("Rechazado")

    def test_score_alto_aprobado(self):
        resp = client.post("/evaluar-riesgo", json={"edad": 25, "ingresos": 3000, "deudas": 500})
        assert resp.status_code == 200
        assert resp.json()["resultado"] == "Aprobado"

    def test_score_bajo_en_revision(self):
        resp = client.post("/evaluar-riesgo", json={"edad": 30, "ingresos": 1000, "deudas": 500})
        assert resp.status_code == 200
        assert resp.json()["resultado"] == "En Revision"


class TestDatosFinancieros:
    def test_obtener_historial_cliente(self):
        resp = client.get("/datos-financieros/42")
        assert resp.status_code == 200
        assert resp.json()["cliente_id"] == 42
